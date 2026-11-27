"""TeachFlow orchestration shared by app, eval and cost. Mock is explicit in traces."""
import importlib
import json
import os
from types import SimpleNamespace
from copy import deepcopy

import contract_mock as mock
from tracing import note

MAX_STEPS = 5
MAX_REPAIRS = 2


def active_mode():
    # ai.py loads local .env. Never fall back to mock after choosing real.
    configured = os.environ.get("TEACHFLOW_MODE", "").strip().lower()
    if not configured:
        import ai
        configured = os.environ.get("TEACHFLOW_MODE", "").strip().lower()
        if not configured:
            configured = "mock" if ai.MODEL_PROVIDER == "fake" else "real"
    if configured not in ("mock", "real"):
        raise ValueError("TEACHFLOW_MODE must be mock or real.")
    return configured


def dependencies(mode):
    if mode == "mock":
        return mock
    if mode != "real":
        raise ValueError("Unknown agent mode.")
    import ai
    if ai.MODEL_PROVIDER == "fake":
        raise RuntimeError("Real mode requires a non-fake MODEL_PROVIDER.")
    names = {"parse_document": "parser", "check_request": "guardrails",
             "retrieve": "retrieval", "get_slide_content": "tools",
             "get_teaching_strategy": "tools", "generate_script": "generator",
             "validate_script": "validator"}
    return SimpleNamespace(**{fn: getattr(importlib.import_module(module), fn)
                              for fn, module in names.items()})


def _response(status, message, **extra):
    note("dung: " + status)
    return {"status": status, "message": message, **extra}


def _context_errors(context):
    missing = []
    for field in ("duration_minutes", "class_size"):
        value = context.get(field)
        if type(value) is not int or value <= 0:
            missing.append(field)
    for field in ("lesson_id", "level", "mode", "equipment"):
        value = context.get(field)
        if not isinstance(value, str) or not value.strip():
            missing.append(field)
    if context.get("level") and context["level"] not in ("beginner", "intermediate", "advanced", "mixed"):
        missing.append("level")
    if context.get("mode") and context["mode"] not in ("offline", "online", "hybrid"):
        missing.append("mode")
    objectives = context.get("objectives")
    if not isinstance(objectives, list) or not objectives or any(
        not isinstance(x, str) or not x.strip() for x in objectives
    ):
        missing.append("objectives")
    return list(dict.fromkeys(missing))


def _source_map(documents):
    if not isinstance(documents, list) or not documents:
        raise ValueError("No usable source.")
    result = {}
    for doc in documents:
        if (not isinstance(doc, dict) or not isinstance(doc.get("code"), str)
                or not doc["code"].strip() or not isinstance(doc.get("text"), str)
                or not doc["text"].strip() or doc["code"] in result):
            raise ValueError("Invalid or duplicate source code/text.")
        result[doc["code"]] = doc
    return result


def _canonical_subset(candidate, allowed):
    if not isinstance(candidate, list):
        raise TypeError("Source tool must return a list.")
    result = []
    seen = set()
    for doc in candidate:
        code = doc.get("code") if isinstance(doc, dict) else None
        if not isinstance(code, str) or code not in allowed:
            raise ValueError("Source tool returned an out-of-scope reference.")
        if code not in seen:
            result.append(deepcopy(allowed[code]))
            seen.add(code)
    return result


def build_response(context, deps=None, mode=None):
    """Return ScriptResponse. Exceptions from real providers propagate to eval."""
    if not isinstance(context, dict):
        return _response("needs_clarification", "Input must be a JSON object.")
    mode = mode or active_mode()
    note("TeachFlow mode=" + mode + "; fixed orchestration, one generator invocation.")
    missing = _context_errors(context)
    if missing:
        return _response("needs_clarification", "Bổ sung hoặc sửa: " + ", ".join(missing),
                         missing_fields=missing, source_refs=[])
    if context["lesson_id"] == "custom" and context.get("permission") is not True:
        return _response("needs_clarification", "Xác nhận quyền sử dụng nguồn custom.",
                         missing_fields=["permission"])
    if context["lesson_id"] != "custom" and "sources" in context:
        return _response("refused", "Không ghi đè nguồn bài đã đăng ký.",
                         reason_code="SOURCE_OVERRIDE")
    deps = deps or dependencies(mode)
    try:
        documents = deps.parse_document(deepcopy(context))
        allowed = _source_map(documents)
        refs = context.get("source_refs")
        if refs is not None:
            if (not isinstance(refs, list) or not refs
                    or any(not isinstance(r, str) or r not in allowed for r in refs)):
                raise ValueError("Invalid source_refs.")
            allowed = {r: allowed[r] for r in dict.fromkeys(refs)}
            documents = list(allowed.values())
    except ValueError:
        return _response("needs_clarification", "Nguồn không tồn tại hoặc không hợp lệ.",
                         missing_fields=["sources"])
    note("parser: %d source segments" % len(documents))
    guard = deps.check_request(deepcopy(context), deepcopy(documents))
    if not guard["ok"]:
        status = guard.get("status")
        if status not in ("needs_clarification", "refused"):
            status = "refused"
        return _response(status, "; ".join(map(str, guard.get("errors", []))) or "Yêu cầu bị chặn.",
                         reason_code="REQUEST_CHECK")
    # Context sent to generator has no raw custom-source override.
    clean = {k: deepcopy(context[k]) for k in
             ("lesson_id", "duration_minutes", "level", "class_size", "mode",
              "equipment", "objectives", "request", "source_refs") if k in context}
    query = " ".join(clean["objectives"]) + " " + str(clean.get("request", ""))
    candidates = documents if len(documents) <= 12 or refs is not None else deps.retrieve(query, deepcopy(documents), limit=12)
    selected = _canonical_subset(candidates, allowed)
    if not selected:
        return _response("needs_clarification", "Không tìm thấy đoạn nguồn liên quan.")
    found = deps.get_slide_content([d["code"] for d in selected], deepcopy(documents))
    chosen = _canonical_subset(found["segments"], {d["code"]: d for d in selected})
    if found.get("not_found") or len(chosen) != len(selected):
        return _response("needs_clarification", "Không truy xuất đủ mã nguồn.")
    # Catalog call is read-only; real generator owns strategy/model decisions.
    strategies = deps.get_teaching_strategy(deepcopy(clean))
    note("retrieval: %d/%d sources; strategy catalog consulted" % (len(chosen), len(documents)))
    clean["source_refs"] = [d["code"] for d in chosen]
    clean["teaching_strategies"] = strategies
    script = deps.generate_script(clean, deepcopy(chosen))
    if not isinstance(script, dict):
        raise TypeError("generate_script must return a dict.")
    status = script.get("status")
    if status in ("needs_clarification", "refused"):
        return _response(status, str(script.get("message") or "Cần kiểm tra lại yêu cầu."),
                         **{k: script[k] for k in ("missing_fields", "source_refs", "reason_code") if k in script})
    if status != "pending_review":
        raise ValueError("Generator returned an invalid status (no automatic approval).")
    # Compatibility adapter for the old array-shaped teacher_actions.
    for seg in script.get("segments", []):
        if isinstance(seg, dict) and isinstance(seg.get("teacher_actions"), list):
            actions = seg["teacher_actions"]
            if all(isinstance(x, str) for x in actions):
                seg["teacher_actions"] = "\n".join(actions)
    # Independent structural checks stay enabled, even if production validator is permissive.

    baseline = mock.validate_script(script, context, chosen)
    result = deps.validate_script(script, deepcopy(context), deepcopy(chosen))
    if not baseline["ok"] or not result["ok"]:
        errors = list(dict.fromkeys(baseline["errors"] + result.get("errors", [])))
        return _response("needs_clarification", "Kịch bản chưa hợp lệ: " + "; ".join(errors),
                         reason_code="INVALID_SCRIPT")
    script["sources"] = deepcopy(chosen)
    script["context"] = {k: deepcopy(context[k]) for k in
                         ("level", "class_size", "mode", "equipment")}
    script["warnings"] = list(dict.fromkeys(
        list(script.get("warnings") or []) + baseline["warnings"] + result.get("warnings", [])))
    script["generation_mode"] = mode
    if mode == "mock":
        script["model"] = "mock-contract"
        script["warnings"].append("MOCK: không gọi LLM, không dùng để chấm benchmark thật.")
    note("dung: pending_review; one generation, no repair; generator owns internal model-call budget.")
    return script


def answer(text: str) -> dict:
    try:
        context = json.loads(text)
    except (TypeError, json.JSONDecodeError):
        response = _response("needs_clarification", "Input phải là LessonRequest JSON.")
    else:
        response = build_response(context)
    return {"output": json.dumps(response, ensure_ascii=False)}
