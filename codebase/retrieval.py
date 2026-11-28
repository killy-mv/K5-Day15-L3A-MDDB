"""Retrieval / RAG theo nguồn bài học đã chọn (D3-04). Người làm: Đạt.

Chỉ đọc các đoạn trong `documents` được truyền vào, không tự bịa mã nguồn hay trộn bài khác.
Bài ngắn (<= limit đoạn) giữ nguyên toàn bộ ngữ cảnh; bài dài chấm điểm theo từ khóa và
mã nguồn xuất hiện trong truy vấn rồi giữ thứ tự tài liệu gốc.
"""
from copy import deepcopy
import re

_STOPWORDS = {
    "và", "của", "cho", "với", "trong", "khi", "các", "một", "những", "được",
    "này", "đó", "từ", "theo", "là", "có", "không", "về", "để", "phần", "bài",
    "kịch", "bản", "giảng", "dạy", "học", "viên", "sinh", "soạn", "lớp", "the",
    "and", "for", "with", "from", "that", "this",
}


def _tokenize(text: str) -> set[str]:
    tokens = {
        tok for tok in re.findall(r"[^\W_]+(?:-[^\W_]+)*", (text or "").casefold())
        if len(tok) > 1 and tok not in _STOPWORDS
    }
    return tokens


def _score_segment(query_lower: str, query_tokens: set[str], doc: dict) -> float:
    code = str(doc.get("code") or "")
    title = str(doc.get("title") or "")
    section = str(doc.get("section") or "")
    text = str(doc.get("text") or "")

    score = 0.0
    if code and code.casefold() in query_lower:
        score += 20.0

    title_tokens = _tokenize(title)
    section_tokens = _tokenize(section)
    text_tokens = _tokenize(text)

    score += 3.0 * len(query_tokens & title_tokens)
    score += 2.0 * len(query_tokens & section_tokens)
    score += 1.0 * len(query_tokens & text_tokens)

    if title and len(title) >= 4 and title.casefold() in query_lower:
        score += 5.0
    return score


def retrieve(query: str, documents: list, limit: int = 12) -> list:
    """Chọn tối đa `limit` đoạn liên quan nhất từ `documents` theo `query`.

    Input: query (str), documents (list[SourceSegment]), limit (int).
    Output: list[SourceSegment] là tập con của `documents`, không bịa ID.
    """
    if not isinstance(documents, list) or not documents or limit <= 0:
        return []
    if len(documents) <= limit:
        return deepcopy(documents)

    query_str = str(query or "")
    query_lower = query_str.casefold()
    query_tokens = _tokenize(query_str)

    scored = [
        (_score_segment(query_lower, query_tokens, doc), idx, doc)
        for idx, doc in enumerate(documents)
        if isinstance(doc, dict)
    ]
    top = sorted(scored, key=lambda item: (-item[0], item[1]))[:limit]
    # Giữ lại thứ tự xuất hiện trong tài liệu gốc để mạch bài giảng tự nhiên.
    top_in_order = sorted(top, key=lambda item: item[1])
    return deepcopy([item[2] for item in top_in_order])
