"""Validator: kiểm kịch bản model trả về trước khi giảng viên xem (B3-04, B3-05, B3-06, B3-08). Người làm: Bảo.

Hàm chính là validate_script(script, context, sources), trả về {"ok", "errors", "warnings"}.

Các lỗi được kiểm:
- SCHEMA: thiếu trường, sai kiểu hoặc để trống.
- STATUS: trạng thái phải là pending_review, model không được tự gán approved.
- TIMELINE: số phút phải là số nguyên dương, bắt đầu từ phút 0, các hoạt động nối tiếp nhau
  và tổng bằng thời lượng buổi học.
- REF: mã nguồn phải nằm trong các đoạn đã gửi cho model.
- UNSAFE: không được có thẻ HTML hoặc script trong nội dung.

Lỗi ghi kèm vị trí, ví dụ segments[2].assessment.
Code chỉ kiểm được cấu trúc, không biết nội dung đúng hay sai, nên giảng viên vẫn phải đối chiếu với slide.
"""
import re

ROOT_FIELDS = ("lesson_title", "duration_minutes", "learning_objectives", "segments", "status")
TEXT_FIELDS = ("title", "activity_type", "teacher_script", "teacher_actions", "student_activity",
               "expected_outcome", "assessment", "fallback_strategy")
SEGMENT_FIELDS = ("title", "start_minute", "duration_minutes", "slide_refs") + TEXT_FIELDS[1:]
LONG_SEGMENT = 30   # hoạt động dài hơn 30 phút thì nhắc nên chia nhỏ

_UNSAFE = re.compile(r"<\s*/?\s*[a-zA-Z][\w-]*(\s[^<>]*)?/?\s*>|javascript\s*:|\bon(load|error|click)\s*=", re.I)
_APPROVED = re.compile(r"^\s*(approved|đã duyệt)\s*$", re.I)


def _is_text(v):
    return isinstance(v, str) and v.strip() != ""


def _is_pos_int(v):
    return type(v) is int and v > 0


def _words(text):
    return {w for w in re.findall(r"\w+", str(text).casefold()) if len(w) > 2}


def validate_script(script, context, sources) -> dict:
    errors, warnings = [], ["[REVIEW] Kiểm tra cấu trúc bằng code; giảng viên vẫn phải đối chiếu nội dung với slide gốc trước khi duyệt."]

    def err(code, where, msg):
        errors.append("[%s] %s: %s" % (code, where, msg))

    if not isinstance(script, dict):
        return {"ok": False, "errors": ["[SCHEMA] root: kịch bản phải là JSON object."], "warnings": warnings}
    context = context if isinstance(context, dict) else {}
    known = {s["code"]: s for s in sources or [] if isinstance(s, dict) and isinstance(s.get("code"), str)}

    # Kiểm các trường chung của kịch bản
    for f in ROOT_FIELDS:
        if f not in script:
            err("SCHEMA", f, "thiếu trường bắt buộc.")
    status = script.get("status")
    if status is not None and status != "pending_review":
        err("STATUS", "status", "phải là pending_review, nhận '%s'. AI không tự duyệt." % str(status)[:30])
    for key in ("approved", "approved_by", "approved_at"):
        if script.get(key):
            err("STATUS", key, "model không được gán trạng thái duyệt.")
    if "lesson_title" in script and not _is_text(script.get("lesson_title")):
        err("SCHEMA", "lesson_title", "phải là chuỗi không rỗng.")
    duration = context.get("duration_minutes")
    if "duration_minutes" in script and script.get("duration_minutes") != duration:
        err("TIMELINE", "duration_minutes", "%r khác thời lượng yêu cầu %r." % (script.get("duration_minutes"), duration))
    objs = script.get("learning_objectives")
    if "learning_objectives" in script and (not isinstance(objs, list) or not objs or not all(_is_text(o) for o in objs)):
        err("SCHEMA", "learning_objectives", "phải là danh sách chuỗi không rỗng.")
    for f in ("warnings", "assumptions"):
        if f in script and (not isinstance(script[f], list) or not all(isinstance(x, str) for x in script[f])):
            err("SCHEMA", f, "phải là danh sách chuỗi.")
    for f in ("lesson_title",):
        if _is_text(script.get(f)) and _UNSAFE.search(script[f]):
            err("UNSAFE", f, "chứa thẻ HTML/script.")

    # Kiểm từng hoạt động
    segments = script.get("segments")
    if "segments" in script and (not isinstance(segments, list) or not segments):
        err("SCHEMA", "segments", "phải là danh sách hoạt động không rỗng.")
        segments = []
    elif not isinstance(segments, list):
        segments = []

    expected_start = 0
    used_refs = set()
    for i, seg in enumerate(segments):
        at = "segments[%d]" % i
        if not isinstance(seg, dict):
            err("SCHEMA", at, "phải là object.")
            continue
        for f in SEGMENT_FIELDS:
            if f not in seg:
                err("SCHEMA", "%s.%s" % (at, f), "thiếu trường bắt buộc.")
        for f in TEXT_FIELDS:
            if f in seg:
                v = seg[f]
                if not _is_text(v):
                    err("SCHEMA", "%s.%s" % (at, f), "phải là chuỗi không rỗng.")
                elif _UNSAFE.search(v):
                    err("UNSAFE", "%s.%s" % (at, f), "chứa thẻ HTML/script hoặc javascript:.")

        start, n = seg.get("start_minute"), seg.get("duration_minutes")
        if type(start) is not int or start != expected_start:
            err("TIMELINE", at + ".start_minute", "phải là %d (liên tục, không chồng/hở), nhận %r." % (expected_start, start))
        if not _is_pos_int(n):
            err("TIMELINE", at + ".duration_minutes", "phải là số nguyên dương, nhận %r." % (n,))
        else:
            if n > LONG_SEGMENT:
                warnings.append("[PACING] %s kéo dài %d phút; cân nhắc chia nhỏ hoặc thêm điểm kiểm tra hiểu." % (at, n))
            expected_start = (start if type(start) is int else expected_start) + n

        refs = seg.get("slide_refs")
        if "slide_refs" in seg:
            if not isinstance(refs, list) or not refs or not all(isinstance(r, str) for r in refs):
                err("REF", at + ".slide_refs", "phải là danh sách mã nguồn không rỗng.")
            else:
                bad = [r for r in refs if r not in known]
                if bad:
                    err("REF", at + ".slide_refs", "mã không có trong nguồn được cung cấp: %s." % ", ".join(bad[:10]))
                used_refs.update(r for r in refs if r in known)

    if segments and type(duration) is int and expected_start != duration:
        err("TIMELINE", "segments", "tổng %d phút, cần đúng %d phút." % (expected_start, duration))

    # Cảnh báo cho giảng viên, không làm kịch bản bị loại
    review = sorted(r for r in used_refs if known[r].get("review_required"))
    if review:
        warnings.append("[SOURCE_REVIEW] Nguồn %s đánh dấu cần đối chiếu PDF gốc." % ", ".join(review[:15]))
    if segments and not errors:
        body = " ".join(" ".join(str(s.get(f, "")) for f in TEXT_FIELDS) for s in segments if isinstance(s, dict))
        body_words = _words(body) | _words(" ".join(script.get("warnings") or []) + " " + " ".join(script.get("assumptions") or []))
        for obj in context.get("objectives") or []:
            w = _words(obj)
            if w and len(w & body_words) / len(w) < 0.5:
                warnings.append("[COVERAGE] Mục tiêu '%s' ít được nhắc trong kịch bản; kiểm tra đã dạy hay đã ghi hoãn." % str(obj)[:80])
        if not any(_is_text(s.get("assessment")) and "?" in str(s.get("teacher_script", "")) + str(s.get("assessment", ""))
                   for s in segments if isinstance(s, dict)):
            warnings.append("[CHECK_UNDERSTANDING] Chưa thấy câu hỏi kiểm tra hiểu bài rõ ràng.")
    return {"ok": not errors, "errors": errors, "warnings": warnings}
