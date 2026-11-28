"""Opt-in real Gemini UI smoke, not official evaluation. Requires Playwright + Edge."""
import argparse
import json
import os
import sys
import threading
import time
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "codebase"))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-real", action="store_true")
    args = parser.parse_args()
    if not args.run_real:
        parser.error("--run-real is required (consumes API quota)")
    os.environ["TEACHFLOW_MODE"] = "real"
    import ai
    import agent
    import backend
    import tracing
    from playwright.sync_api import sync_playwright, expect
    if ai.MODEL_PROVIDER == "fake":
        raise RuntimeError("Real provider required")
    agent.dependencies("real")
    traces = []
    original_end = tracing.end
    def capture_end():
        summary, events = original_end()
        traces.append(summary)
        return summary, events
    server = backend.make_server(0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with patch.object(tracing, "end", side_effect=capture_end), sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=True)
            page = browser.new_page(accept_downloads=True)
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(f"http://127.0.0.1:{server.server_port}/")
            expect(page.locator("#modeBadge")).to_contain_text("AI THẬT")
            page.locator("#lesson").select_option("lab_tools")
            page.locator("#duration").fill("60")
            page.locator("#request").fill("Tạo kịch bản cầm tay khi hướng dẫn lab, gồm lời dẫn từng bước và cách hỗ trợ khi học viên bị kẹt.")
            page.locator("#permission").check()
            start = time.monotonic()
            with page.expect_response("**/api/generate", timeout=310000) as received:
                page.locator("#generate").click()
                expect(page.locator("#generate")).to_be_disabled()
            response = received.value
            result = response.json()
            assert response.ok and result.get("generation_mode") == "real", ("response status", response.status)
            assert result.get("status") == "pending_review", ("script status", result.get("status"))
            expect(page.locator("#status")).to_have_text("Chờ duyệt")
            expect(page.locator(".segment")).to_have_count(len(result["segments"]))
            expect(page.locator("#validationNotice")).to_contain_text("đạt")
            assert len(result["sources"]) > 0 and result["warnings"]
            assert result["duration_minutes"] == 60
            expect(page.locator("#teach")).to_be_disabled()
            expect(page.locator("#approve")).to_be_disabled()
            page.locator("#reviewed").check()
            page.locator("#approve").click()
            expect(page.locator("#status")).to_have_text("Đã duyệt")
            with page.expect_popup() as popup:
                page.locator("#teach").click()
            reader = popup.value
            expect(reader.locator("#current")).to_contain_text("Slide gốc:")
            expect(reader.locator("#nav button")).to_have_count(len(result["segments"]))
            with page.expect_download() as download:
                page.locator("#exportJson").click()
            exported = json.loads(Path(download.value.path()).read_text(encoding="utf8"))
            assert exported["status"] == "approved" and exported["segments"] == result["segments"]
            page.locator("textarea[data-k=teacher_script]").first.fill("Lời dẫn đã sửa để kiểm tra hủy duyệt.")
            expect(page.locator("#teach")).to_be_disabled()
            assert reader.is_closed()
            page.locator("#duration").fill("")
            page.locator("#generate").click()
            expect(page.locator("#inputNotice")).to_contain_text("duration_minutes")
            assert not errors, errors
            assert traces and 1 <= traces[0]["model_calls"] <= agent.MAX_STEPS
            assert traces[0]["tokens_in"] > 0 and traces[0]["tokens_out"] > 0
            assert traces[0]["tool_calls"] >= 2 and not traces[0]["errors"]
            assert traces[-1]["model_calls"] == 0
            print(json.dumps({"result":"PASS","configured_model":ai.MODEL_NAME,
                "models":traces[0]["models"],"segments":len(result["segments"]),
                "duration_minutes":result["duration_minutes"],"sources":len(result["sources"]),
                "warnings":len(result["warnings"]),"model_calls":traces[0]["model_calls"],
                "tool_calls":traces[0]["tool_calls"],"tokens_in":traces[0]["tokens_in"],
                "tokens_out":traces[0]["tokens_out"],"missing_context_model_calls":traces[-1]["model_calls"],
                "elapsed_seconds":round(time.monotonic()-start,2)},ensure_ascii=False),flush=True)
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    main()
