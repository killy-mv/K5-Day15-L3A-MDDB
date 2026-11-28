"""Browser integration with an explicitly synthetic long fixture; no LLM calls."""
import json
import os
import sys
import threading
import time
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "codebase"))
from backend import make_server

os.environ["TEACHFLOW_MODE"] = "mock"
fixture = json.loads((ROOT / "data/fixtures/script_response.json").read_text(encoding="utf8"))
dataset = json.loads((ROOT / "data/lessons/oop_annotations.json").read_text(encoding="utf8"))
codes = {ref for s in fixture["segments"] for ref in s["slide_refs"]}
fixture["sources"] = [s for s in dataset["lessons"][0]["segments"] if s["code"] in codes]
fixture["segments"][0]["teacher_script"] += "\n" + "Lời dẫn tiếng Việt — kiểm tra nội dung dài.\n" * 180
fixture["warnings"].append("FIXTURE: không phải kết quả AI thật.")
state = {"kind": "valid"}

def answer(text):
    result = deepcopy(fixture)
    kind = state["kind"]
    if kind == "slow":
        time.sleep(2)
    if kind == "invalid":
        result["segments"][0]["slide_refs"] = ["OUTSIDE"]
    if kind == "malformed":
        result["segments"] = None
    if kind == "optional":
        result.pop("warnings")
        result.pop("assumptions")
    if kind == "error":
        raise RuntimeError("private-test-secret")
    return {"output": json.dumps(result, ensure_ascii=False)}

server = make_server(0)
threading.Thread(target=server.serve_forever, daemon=True).start()
try:
    with patch("agent.answer", side_effect=answer), sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(accept_downloads=True)
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(f"http://127.0.0.1:{server.server_port}/")
        expect(page.locator("#modeBadge")).to_contain_text("MOCK")
        page.locator("#permission").check()
        page.locator("#generate").click()
        expect(page.locator("#status")).to_have_text("Chờ duyệt")
        expect(page.locator(".segment")).to_have_count(4)
        expect(page.locator("textarea[data-k=teacher_script]").first).to_have_value(fixture["segments"][0]["teacher_script"])
        page.locator("#reviewed").check()
        page.locator("#approve").click()
        expect(page.locator("#status")).to_have_text("Đã duyệt")
        with page.expect_popup() as popup:
            page.locator("#teach").click()
        reader = popup.value
        expect(reader.locator("#nav button")).to_have_count(4)
        expect(reader.locator("#clock")).to_have_text("05:00")
        reader.locator("#next").click()
        expect(reader.locator("#clock")).to_have_text("15:00")
        reader.locator("#nav button").last.click()
        expect(reader.locator("#clock")).to_have_text("20:00")
        expect(reader.locator("#next")).to_be_disabled()
        with page.expect_download() as download:
            page.locator("#exportJson").click()
        exported = json.loads(Path(download.value.path()).read_text(encoding="utf8"))
        assert len(exported["segments"]) == 4 and exported["status"] == "approved"
        edit = page.locator("textarea[data-k=teacher_script]").first
        edit.fill("<script>alert(1)</script>")
        expect(page.locator("#validationNotice")).to_contain_text("UNSAFE")
        expect(page.locator("#status")).to_have_text("Cần sửa")
        expect(page.locator("#teach")).to_be_disabled()
        assert reader.is_closed()
        page.locator("#reviewed").check()
        expect(page.locator("#approve")).to_be_disabled()
        edit.fill("Lời dẫn đã chỉnh an toàn")
        page.locator("#reviewed").check()
        expect(page.locator("#approve")).to_be_enabled()
        for kind in ("invalid", "malformed", "optional", "error"):
            state["kind"] = kind
            page.locator("#generate").click()
            expect(page.locator("#generate")).to_be_enabled()
            if kind == "optional":
                expect(page.locator("#status")).to_have_text("Chờ duyệt")
            else:
                expect(page.locator("#actions")).to_be_hidden()
                expect(page.locator("#teach")).to_be_disabled()
                expect(page.locator("#inputNotice")).to_be_visible()
                assert "private-test-secret" not in page.locator("#inputNotice").inner_text()
        state["kind"] = "slow"
        page.locator("#generate").click()
        expect(page.locator("#generate")).to_be_disabled()
        expect(page.locator("#status")).to_have_text("Đang sinh")
        expect(page.locator("#inputNotice")).to_contain_text("giây")
        page.locator("#request").fill("Context mới")
        expect(page.locator("#generate")).to_be_enabled(timeout=10000)
        expect(page.locator("#actions")).to_be_hidden()
        expect(page.locator("#inputNotice")).to_contain_text("Context đã thay đổi")
        assert not errors, errors
        browser.close()
        print("Complex browser smoke PASS: 4 segments, long script, reader navigation, JSON, unsafe edit, malformed responses, optional metadata, provider error, stale response.")
finally:
    server.shutdown()
    server.server_close()
