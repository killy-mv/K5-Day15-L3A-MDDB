"""Opt-in integration smoke after AI Core is merged. Not an official eval.

Run: python tests/smoke_real_studio.py --run-real
Consumes real model quota (two scripted cases, up to five calls per case).
Does not write eval results, expose keys, or substitute mock output.
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "codebase"))

def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--run-real", action="store_true", help="Explicitly authorize real model calls")
    args = cli.parse_args()
    if not args.run_real:
        cli.error("Use --run-real only when the AI Core and .env are configured.")
    os.environ["TEACHFLOW_MODE"] = "real"
    import agent
    import ai
    import tracing
    import validator
    try:
        agent.dependencies("real")
    except Exception as e:
        print("BLOCKED: real dependencies unavailable (" + type(e).__name__ + ")")
        return 2
    if ai.MODEL_PROVIDER == "fake":
        print("BLOCKED: fake provider")
        return 2
    with (ROOT / "eval/benchmark.csv").open(encoding="utf-8-sig", newline="") as f:
        cases = {r["id"]: r for r in csv.DictReader(f)}
    failures = []
    for case_id in ("B11", "B05"):
        case = cases[case_id]
        context = json.loads(case["input"])
        tracing.begin("smoke-" + case_id)
        result = None
        try:
            result = json.loads(agent.answer(case["input"])["output"])
        except Exception as exc:
            failures.append(case_id + ": " + type(exc).__name__)
        finally:
            trace, events = tracing.end()
        if result is not None:
            try:
                assert result["status"] == "pending_review"
                assert result["generation_mode"] == "real"
                assert validator.validate_script(result, context, result["sources"])["ok"]
                assert 1 <= trace["model_calls"] <= agent.MAX_STEPS
                assert trace["tokens_in"] > 0 and trace["tokens_out"] > 0
                assert trace["models"] and all("fake" not in m.lower() and "mock" not in m.lower() for m in trace["models"])
                assert trace["tool_calls"] > 0
                assert not trace["errors"]
            except (AssertionError, KeyError, TypeError, ValueError):
                failures.append(case_id + ": invalid script or real model trace")
        print(case_id, "model_calls=", trace["model_calls"], "tool_calls=", trace["tool_calls"],
              "tokens_in=", trace["tokens_in"], "tokens_out=", trace["tokens_out"])
    if failures:
        print("FAIL:", "; ".join(failures))
        return 1
    print("PASS: real normal/difficult structural smoke. Semantic quality and repair budget still require review.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
