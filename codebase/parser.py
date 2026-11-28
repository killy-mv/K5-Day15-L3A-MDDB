"""Parser nguồn bài giảng (interface-contract §5, owner: Bảo). B3-01, B3-02.

parse_document(request) -> list[SourceSegment]

- lesson_id đã đăng ký: tra theo id trong data/lessons/*.json (id là khóa tra, KHÔNG dùng làm đường dẫn).
- lesson_id == "custom" (cần permission=true), một trong hai:
    sources:     list[{code, text, page?, title?}] đã chuẩn hóa sẵn
    source_text: text / Markdown / text trích từ PDF (trang ngăn bởi \\f) → tự chia đoạn, mã U001, U002…
- source_refs (tùy chọn): giới hạn đúng các mã đó, mã lạ → lỗi (không bịa mã).
Mọi lỗi là ValueError có thông điệp tiếng Việt; agent đổi thành needs_clarification.

Ngoài luồng agent (không nhận path từ request): pdf_to_segments(path) đọc PDF có lớp text
bằng pypdf nếu đã cài, dùng ở dòng lệnh để giảng viên chuẩn bị nguồn custom. Không OCR.
Chỉ dùng thư viện chuẩn (pypdf là tùy chọn).
"""
from copy import deepcopy
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = ROOT / "data" / "lessons"

MAX_SEGMENTS = 300          # giới hạn số đoạn một bài custom
MAX_SEGMENT_CHARS = 2500    # đoạn dài hơn thì cắt tiếp theo câu
MAX_TOTAL_CHARS = 400_000   # ~ giới hạn body 2 MB của backend, chừa chỗ JSON
_CODE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,39}$")
_OPTIONAL_KEYS = ("page", "title", "section", "content_kind", "review_required")


def _registered_lessons() -> dict:
    lessons = {}
    for path in sorted(LESSON_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for lesson in data.get("lessons", []):
            if isinstance(lesson, dict) and isinstance(lesson.get("id"), str):
                lessons.setdefault(lesson["id"], lesson)
    return lessons


def _normalize(seg, where: str) -> dict:
    """Một SourceSegment hợp lệ: code (mã an toàn, duy nhất) + text không rỗng; giữ trường phụ đúng kiểu."""
    if not isinstance(seg, dict):
        raise ValueError("%s: đoạn nguồn phải là object {code, text}." % where)
    code, text = seg.get("code"), seg.get("text")
    if not isinstance(code, str) or not _CODE.match(code.strip()):
        raise ValueError("%s: mã đoạn không hợp lệ (chỉ chữ, số, . _ -; tối đa 40 ký tự)." % where)
    if not isinstance(text, str) or not text.strip():
        raise ValueError("%s (%s): nội dung đoạn rỗng." % (where, code))
    out = {"code": code.strip(), "text": text.strip()}
    page = seg.get("page")
    if page is not None:
        if type(page) is not int or page < 1:
            raise ValueError("%s (%s): page phải là số nguyên từ 1." % (where, code))
        out["page"] = page
    for key in _OPTIONAL_KEYS[1:]:
        if key in seg and seg[key] is not None:
            out[key] = seg[key] if key == "review_required" else str(seg[key])
    return out


def _check_unique(docs: list) -> list:
    if not docs:
        raise ValueError("Không có đoạn nguồn nào. Hãy nạp slide/tài liệu trước khi soạn kịch bản.")
    seen = set()
    for d in docs:
        if d["code"] in seen:
            raise ValueError("Mã đoạn bị trùng: %s." % d["code"])
        seen.add(d["code"])
    return docs


def _split_long(text: str, limit: int = MAX_SEGMENT_CHARS) -> list:
    if len(text) <= limit:
        return [text]
    parts, cur = [], ""
    for sentence in re.split(r"(?<=[.!?。])\s+|\n", text):
        if cur and len(cur) + len(sentence) + 1 > limit:
            parts.append(cur.strip())
            cur = ""
        while len(sentence) > limit:   # câu quá dài: cắt cứng
            parts.append(sentence[:limit])
            sentence = sentence[limit:]
        cur += sentence + " "
    if cur.strip():
        parts.append(cur.strip())
    return parts


def chunk_text(text: str, prefix: str = "U") -> list:
    """Chia text/Markdown/text-PDF thành đoạn có mã ổn định (B3-02).

    - Có ký tự \\f (pdftotext, pypdf): mỗi trang một đoạn, giữ số trang.
    - Có heading Markdown (#): mỗi mục một đoạn, title = heading.
    - Còn lại: mỗi khối ngăn bởi dòng trống một đoạn.
    Đoạn quá dài được cắt theo câu; mã U001, U002… theo thứ tự xuất hiện (không random).
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("source_text rỗng.")
    if len(text) > MAX_TOTAL_CHARS:
        raise ValueError("Tài liệu quá dài (> %d ký tự). Hãy chọn phần bài cần dạy." % MAX_TOTAL_CHARS)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks = []  # (page, title, body)
    if "\f" in text:
        for i, page in enumerate(text.split("\f"), 1):
            if page.strip():
                blocks.append((i, None, page.strip()))
    elif re.search(r"(?m)^#{1,6}\s+\S", text):
        title, body = None, []
        for line in text.split("\n"):
            m = re.match(r"^#{1,6}\s+(.*\S)\s*$", line)
            if m:
                if title or "".join(body).strip():
                    blocks.append((None, title, "\n".join(body).strip() or title))
                title, body = m.group(1), []
            else:
                body.append(line)
        if title or "".join(body).strip():
            blocks.append((None, title, "\n".join(body).strip() or title))
    else:
        blocks = [(None, None, b.strip()) for b in re.split(r"\n\s*\n", text) if b.strip()]

    docs = []
    for page, title, body in blocks:
        for part in _split_long(re.sub(r"[ \t]+", " ", body)):
            seg = {"code": "%s%03d" % (prefix, len(docs) + 1), "text": part}
            if page:
                seg["page"] = page
            if title:
                seg["title"] = title
            docs.append(seg)
    if len(docs) > MAX_SEGMENTS:
        raise ValueError("Tài liệu có %d đoạn (> %d). Hãy chọn phần bài cần dạy." % (len(docs), MAX_SEGMENTS))
    return docs


def _apply_refs(docs: list, refs) -> list:
    if refs is None:
        return docs
    if not isinstance(refs, list) or not refs or any(not isinstance(r, str) for r in refs):
        raise ValueError("source_refs phải là danh sách mã đoạn không rỗng.")
    lookup = {d["code"]: d for d in docs}
    missing = [r for r in refs if r not in lookup]
    if missing:
        raise ValueError("Mã nguồn không có trong bài: %s." % ", ".join(missing))
    return [lookup[r] for r in dict.fromkeys(refs)]


def parse_document(request: dict) -> list:
    """LessonRequest -> list[SourceSegment] (bản sao, thứ tự như bài). Lỗi: ValueError."""
    if not isinstance(request, dict):
        raise ValueError("Input phải là LessonRequest JSON object.")
    lesson_id = request.get("lesson_id")
    if not isinstance(lesson_id, str) or not lesson_id.strip():
        raise ValueError("Thiếu lesson_id: chọn bài đã nạp hoặc dùng 'custom' kèm tài liệu nguồn.")

    if lesson_id == "custom":
        if request.get("permission") is not True:
            raise ValueError("Xác nhận quyền sử dụng tài liệu custom (permission=true).")
        if "sources" in request and "source_text" in request:
            raise ValueError("Chỉ gửi một trong sources hoặc source_text.")
        if "source_text" in request:
            docs = chunk_text(request["source_text"])
        else:
            raw = request.get("sources")
            if not isinstance(raw, list):
                raise ValueError("Thiếu tài liệu nguồn custom (sources hoặc source_text).")
            if len(raw) > MAX_SEGMENTS:
                raise ValueError("Quá nhiều đoạn nguồn (> %d)." % MAX_SEGMENTS)
            docs = [_normalize(s, "sources[%d]" % i) for i, s in enumerate(raw)]
    else:
        if "sources" in request or "source_text" in request:
            raise ValueError("Không ghi đè nguồn của bài đã đăng ký; dùng lesson_id='custom'.")
        lesson = _registered_lessons().get(lesson_id)
        if lesson is None:
            raise ValueError("Không có bài '%s' trong dữ liệu đã nạp." % lesson_id[:60])
        docs = [_normalize(s, "%s[%d]" % (lesson_id, i)) for i, s in enumerate(lesson.get("segments", []))]

    return deepcopy(_apply_refs(_check_unique(docs), request.get("source_refs")))


def pdf_to_segments(path, prefix: str = "P") -> list:
    """(Dòng lệnh, ngoài luồng agent) PDF có lớp text -> một đoạn mỗi trang. Cần `pip install pypdf`.
    Trang không có text (ảnh scan) bị bỏ qua và được liệt kê ở cảnh báo stderr; không OCR."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # thư viện tùy chọn
        raise ValueError("Cần cài pypdf để đọc PDF: pip install pypdf") from exc
    reader = PdfReader(str(path))
    pages = [(p.extract_text() or "").strip() for p in reader.pages]
    docs = [{"code": "%s%03d" % (prefix, i), "page": i, "text": t}
            for i, t in enumerate(pages, 1) if t]
    if not docs:
        raise ValueError("PDF không có lớp text (có thể là ảnh scan); MVP chưa hỗ trợ OCR.")
    return docs


if __name__ == "__main__":
    # python codebase/parser.py bai.pdf|bai.md > nguon.json   → dán vào sources của request custom
    import sys
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if len(sys.argv) != 2:
        print("Cách dùng: python codebase/parser.py <file.pdf|.md|.txt>", file=sys.stderr)
        sys.exit(2)
    src = Path(sys.argv[1])
    segs = pdf_to_segments(src) if src.suffix.lower() == ".pdf" else chunk_text(src.read_text(encoding="utf-8"))
    print(json.dumps(segs, ensure_ascii=False, indent=1))
    print("%d đoạn từ %s" % (len(segs), src.name), file=sys.stderr)
