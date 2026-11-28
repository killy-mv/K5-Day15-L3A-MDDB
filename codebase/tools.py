"""Công cụ tra cứu nguồn bài học và chiến lược giảng dạy (D3-05). Người làm: Đạt.

Mỗi công cụ có @tool để khung tracing.py ghi vào trace. Cả hai công cụ đều chỉ đọc,
không có tác động ra ngoài (không gửi tin, không sửa dữ liệu, không chấm điểm).
"""
from copy import deepcopy
import json
from pathlib import Path

from tracing import tool, TOOLS  # noqa: F401

ROOT = Path(__file__).resolve().parents[1]
STRATEGIES_PATH = ROOT / "data" / "teaching_strategies.json"


@tool
def get_slide_content(codes: list, documents: list) -> dict:
    """get_slide_content · Input: codes (list[str]), documents (list[SourceSegment]) · Output: {"segments": list, "not_found": list[str]} · Không tác động ra ngoài (chỉ đọc)."""
    if not isinstance(codes, list) or not isinstance(documents, list):
        return {"segments": [], "not_found": list(codes) if isinstance(codes, list) else []}

    lookup = {
        doc["code"]: doc
        for doc in documents
        if isinstance(doc, dict) and isinstance(doc.get("code"), str)
    }
    segments = []
    not_found = []
    seen = set()
    for code in codes:
        if not isinstance(code, str):
            continue
        if code in lookup:
            if code not in seen:
                segments.append(deepcopy(lookup[code]))
                seen.add(code)
        else:
            not_found.append(code)
    return {"segments": segments, "not_found": not_found}


@tool
def get_teaching_strategy(context: dict) -> list:
    """get_teaching_strategy · Input: context (LessonRequest dict) · Output: danh sách chiến lược giảng dạy phù hợp (list[dict]) · Không tác động ra ngoài (chỉ đọc)."""
    strategies = json.loads(STRATEGIES_PATH.read_text(encoding="utf-8"))
    if not isinstance(context, dict):
        return strategies

    duration = context.get("duration_minutes")
    equipment = str(context.get("equipment") or "").casefold()
    no_lab_env = any(kw in equipment for kw in ("không có máy", "không có laptop", "không máy chiếu", "bảng phấn", "giấy"))

    feasible = []
    for item in strategies:
        if not isinstance(item, dict):
            continue
        min_m = item.get("min_minutes") or 0
        if isinstance(duration, int) and duration > 0 and min_m > duration:
            continue
        if no_lab_env and item.get("id") == "TS04":
            continue
        feasible.append(deepcopy(item))

    return feasible if feasible else deepcopy(strategies)
