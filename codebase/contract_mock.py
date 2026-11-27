"""CP3 shared contract stubs. Not the production agent or an LLM evaluation."""
from copy import deepcopy
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "data" / "fixtures"
FIELDS = ("title", "activity_type", "teacher_script", "teacher_actions",
          "student_activity", "expected_outcome", "assessment", "fallback_strategy")


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_document(request):
    lesson_id = request.get("lesson_id")
    if lesson_id == "custom":
        if request.get("permission") is not True:
            raise ValueError("Confirm permission for custom source.")
        docs = request.get("sources", [])
    else:
        lessons = []
        for path in (ROOT / "data" / "lessons").glob("*.json"):
            lessons.extend(_load(path)["lessons"])
        match = next((x for x in lessons if x["id"] == lesson_id), None)
        if match is None:
            raise ValueError("Unknown lesson_id.")
        docs = match["segments"]
    if not isinstance(docs, list) or not docs or any(
        not isinstance(d, dict) or not isinstance(d.get("code"), str)
        or not d["code"].strip() or not isinstance(d.get("text"), str)
        or not d["text"].strip() for d in docs
    ):
        raise ValueError("Missing or invalid source segments.")
    if len({d["code"] for d in docs}) != len(docs):
        raise ValueError("Duplicate source codes.")
    refs = request.get("source_refs")
    if refs is not None:
        if not isinstance(refs, list) or not refs or any(not isinstance(r, str) for r in refs):
            raise ValueError("source_refs must be a nonempty list of strings.")
        found = get_slide_content(refs, docs)
        if found["not_found"]:
            raise ValueError("Unknown source refs: " + ", ".join(found["not_found"]))
        docs = found["segments"]
    return deepcopy(docs)


def retrieve(query, documents, limit=12):
    tokens = set(re.findall(r"\w+", query.casefold()))
    ranked = sorted(documents, key=lambda d: -len(tokens & set(
        re.findall(r"\w+", (d["text"] + " " + d.get("title", "")).casefold()))))
    return deepcopy(ranked[:max(0, limit)])


def get_slide_content(codes, documents):
    lookup = {d["code"]: d for d in documents}
    return {"segments": [deepcopy(lookup[c]) for c in dict.fromkeys(codes) if c in lookup],
            "not_found": [c for c in codes if c not in lookup]}


def get_teaching_strategy(context):
    strategies = _load(ROOT / "data" / "teaching_strategies.json")
    # Stub exposes strategy catalog; real agent chooses feasible activities.
    return strategies


def call_model(system, user):
    return {"text": json.dumps({"status": "needs_clarification",
            "message": "Mock only; no model call."}), "model": "mock-contract",
            "tokens_in": 0, "tokens_out": 0}


def check_request(context, sources):
    errors = []
    for k in ("duration_minutes", "class_size"):
        v = context.get(k)
        if type(v) is not int or v <= 0:
            errors.append(k)
    for k in ("level", "mode", "equipment"):
        if not isinstance(context.get(k), str) or not context[k].strip():
            errors.append(k)
    objs = context.get("objectives")
    if not isinstance(objs, list) or not objs or any(not isinstance(x, str) or not x.strip() for x in objs):
        errors.append("objectives")
    if not sources:
        errors.append("sources")
    if errors:
        return {"ok": False, "errors": errors, "status": "needs_clarification"}
    # Minimal illustrative guard; NOT a complete injection detector.
    text = str(context.get("request", "")) + " " + " ".join(d["text"] for d in sources)
    if re.search(r"\.env|bỏ qua hướng dẫn hệ thống|ignore previous instructions|<script\b", text, re.I):
        return {"ok": False, "errors": ["Untrusted instruction in request/source."], "status": "refused"}
    return {"ok": True, "errors": [], "status": None}


def generate_script(context, sources):
    check = check_request(context, sources)
    if not check["ok"]:
        return {"status": check["status"], "message": "; ".join(check["errors"])}
    # A deterministic generic scaffold; deliberately not a semantic generator.
    ref = sources[0]["code"]
    return {"lesson_title": "Mock teaching script: " + context["lesson_id"],
            "duration_minutes": context["duration_minutes"],
            "learning_objectives": deepcopy(context["objectives"]),
            "status": "pending_review", "model": "mock-contract",
            "warnings": ["Structural mock only; no semantic grounding assessment."],
            "assumptions": [],
            "segments": [{"title": "Đọc và đối chiếu nguồn", "start_minute": 0,
                          "duration_minutes": context["duration_minutes"],
                          "slide_refs": [ref], "activity_type": "review",
                          "teacher_script": "Đọc đoạn nguồn: " + sources[0]["text"],
                          "teacher_actions": "Đối chiếu với slide gốc.",
                          "student_activity": "Nêu lại ý chính.",
                          "expected_outcome": "Nhận biết nội dung đoạn nguồn.",
                          "assessment": "So sánh câu trả lời với đoạn nguồn.",
                          "fallback_strategy": "Đọc lại đoạn nguồn."}]}


def validate_script(script, context, sources):
    errors = []
    warnings = ["Structural check only; human must check meaning and grounding."]
    if script.get("status") != "pending_review":
        errors.append("Expected pending_review.")
    if not isinstance(script.get("lesson_title"), str) or not script["lesson_title"].strip():
        errors.append("Missing lesson_title.")
    if script.get("duration_minutes") != context.get("duration_minutes"):
        errors.append("Duration mismatch.")
    objs = script.get("learning_objectives")
    if not isinstance(objs, list) or not objs or any(not isinstance(x, str) or not x.strip() for x in objs):
        errors.append("Missing learning_objectives.")
    segments = script.get("segments")
    if not isinstance(segments, list) or not segments:
        return {"ok": False, "errors": errors + ["Missing segments."], "warnings": warnings}
    known = {d["code"] for d in sources}
    t = 0
    for i, seg in enumerate(segments):
        if not isinstance(seg, dict):
            errors.append(f"Invalid segment {i}.")
            continue
        n = seg.get("duration_minutes")
        if type(seg.get("start_minute")) is not int or seg["start_minute"] != t:
            errors.append(f"Invalid start_minute {i}.")
        if type(n) is not int or n <= 0:
            errors.append(f"Invalid duration {i}.")
        else:
            t += n
        refs = seg.get("slide_refs")
        if not isinstance(refs, list) or not refs or any(not isinstance(r, str) or r not in known for r in refs):
            errors.append(f"Unknown slide_refs {i}.")
        for field in FIELDS:
            if not isinstance(seg.get(field), str) or not seg[field].strip():
                errors.append(f"Missing {field} in segment {i}.")
    if t != context.get("duration_minutes"):
        errors.append("Timeline total mismatch.")
    return {"ok": not errors, "errors": errors, "warnings": warnings}


def answer(text):
    try:
        context = json.loads(text)
        sources = parse_document(context)
        response = generate_script(context, sources)
        if response["status"] == "pending_review":
            result = validate_script(response, context, sources)
            if not result["ok"]:
                response = {"status": "needs_clarification", "message": "; ".join(result["errors"])}
    except (ValueError, TypeError, AttributeError) as exc:
        response = {"status": "needs_clarification", "message": str(exc)}
    return {"output": json.dumps(response, ensure_ascii=False)}


if __name__ == "__main__":
    context = _load(FIXTURES / "lesson_request.json")
    print(answer(json.dumps(context, ensure_ascii=False))["output"])
