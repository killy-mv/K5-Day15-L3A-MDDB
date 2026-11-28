"""Thống kê tái lập từ data/preclass/ (AI20K K5 L3-4) để làm căn cứ `data_that` cho eval/benchmark.csv.

Chỉ dùng thư viện chuẩn Python; không xuất dữ liệu cá nhân hay nguyên văn file dữ liệu BTC cấp.
Chạy: python eval/preclass_stats.py
"""
import collections
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRECLASS_DIR = os.path.join(ROOT, "data", "preclass")


def compute_stats(preclass_dir=PRECLASS_DIR):
    answers_path = os.path.join(preclass_dir, "answers.csv")
    events_path = os.path.join(preclass_dir, "events.csv")

    kc_stats = collections.defaultdict(lambda: {"correct": 0, "total": 0})
    thuc_hanh_stats = collections.defaultdict(lambda: {"correct": 0, "wrong": 0, "total": 0})

    with open(answers_path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            lesson = row.get("lesson_id", "")
            nguon = row.get("nguon", "")
            was_correct = row.get("was_correct", "")
            if nguon == "pre_post_post" and row.get("lan_thu") == "1" and was_correct in ("True", "False"):
                key = (lesson, row.get("kc_code", ""))
                kc_stats[key]["total"] += 1
                if was_correct == "True":
                    kc_stats[key]["correct"] += 1
            elif nguon == "thuc_hanh":
                thuc_hanh_stats[lesson]["total"] += 1
                if was_correct == "True":
                    thuc_hanh_stats[lesson]["correct"] += 1
                elif was_correct == "False":
                    thuc_hanh_stats[lesson]["wrong"] += 1

    lab_opened_events = 0
    lab_completed_events = 0
    lab_skipped_events = 0
    opened_pairs = set()
    completed_pairs = set()
    completed_non_skip_pairs = set()

    with open(events_path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            etype = row.get("type", "")
            if etype not in ("lab_opened", "lab_completed"):
                continue
            payload = json.loads(row["data"]) if row.get("data") else {}
            pair = (row.get("hv", ""), row.get("lesson_id", ""), payload.get("lab_key", ""))
            if etype == "lab_opened":
                lab_opened_events += 1
                opened_pairs.add(pair)
            elif etype == "lab_completed":
                lab_completed_events += 1
                completed_pairs.add(pair)
                if payload.get("skipped"):
                    lab_skipped_events += 1
                else:
                    completed_non_skip_pairs.add(pair)

    uncompleted_pairs = opened_pairs - completed_pairs
    return {
        "kc_targets": {
            "agentic_fit_scoring_decision": kc_stats[
                ("program-day03:chatbot-to-agentic-agent", "agentic_fit_scoring_decision")
            ],
            "workflow_vs_agent_control": kc_stats[
                ("program-day08:from-workflows-to-agents", "workflow_vs_agent_control")
            ],
            "agent_loop_guardrails": kc_stats[
                ("program-day03:chatbot-to-agentic-agent", "agent_loop_guardrails")
            ],
            "tool_calling_flow": kc_stats[
                ("program-day04:prompt-engineering-tool-calling", "tool_calling_flow")
            ],
        },
        "day04_thuc_hanh": thuc_hanh_stats["program-day04:prompt-engineering-tool-calling"],
        "lab_events": {
            "opened_events": lab_opened_events,
            "completed_events": lab_completed_events,
            "skipped_events": lab_skipped_events,
            "opened_unique_learner_labs": len(opened_pairs),
            "completed_unique_learner_labs": len(completed_pairs & opened_pairs),
            "uncompleted_unique_learner_labs": len(uncompleted_pairs),
            "completed_non_skip_unique_learner_labs": len(completed_non_skip_pairs & opened_pairs),
        },
    }


def main():
    stats = compute_stats()
    print("=== Pre-class KC accuracy (answers.csv, pre_post_post, lan_thu=1) ===")
    for name, s in stats["kc_targets"].items():
        tot = s["total"]
        cor = s["correct"]
        wrong = tot - cor
        pct_c = 100.0 * cor / tot if tot else 0.0
        pct_w = 100.0 * wrong / tot if tot else 0.0
        print(f"  {name}: dung {cor}/{tot} ({pct_c:.1f}%), sai {wrong}/{tot} ({pct_w:.1f}%)")

    th = stats["day04_thuc_hanh"]
    print("\n=== Day04 mini-lab practice (answers.csv, nguon=thuc_hanh) ===")
    pct_w = 100.0 * th["wrong"] / th["total"] if th["total"] else 0.0
    print(f"  program-day04: sai {th['wrong']}/{th['total']} ({pct_w:.1f}%), dung {th['correct']}/{th['total']}")

    le = stats["lab_events"]
    skip_pct = 100.0 * le["skipped_events"] / le["completed_events"] if le["completed_events"] else 0.0
    uncomp_pct = (
        100.0 * le["uncompleted_unique_learner_labs"] / le["opened_unique_learner_labs"]
        if le["opened_unique_learner_labs"]
        else 0.0
    )
    print("\n=== Mini-lab events (events.csv) ===")
    print(
        f"  Su kien: lab_opened={le['opened_events']}, lab_completed={le['completed_events']}, "
        f"skipped={le['skipped_events']} ({skip_pct:.1f}% trong so lab_completed)"
    )
    print(
        f"  Theo cap (hv, lesson_id, lab_key): mo={le['opened_unique_learner_labs']}, "
        f"hoan_thanh={le['completed_unique_learner_labs']}, "
        f"chua_hoan_thanh={le['uncompleted_unique_learner_labs']} ({uncomp_pct:.1f}%), "
        f"hoan_thanh_khong_skip={le['completed_non_skip_unique_learner_labs']}"
    )


if __name__ == "__main__":
    main()
