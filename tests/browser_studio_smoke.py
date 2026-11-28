"""Optional browser smoke: pip install playwright; installed Edge required."""
import os
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"codebase"))
from backend import make_server

os.environ["TEACHFLOW_MODE"]="mock"
server=make_server(0)
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(channel="msedge",headless=True)
        context=browser.new_context(accept_downloads=True)
        errors=[]
        context.on("page",lambda page:page.on("pageerror",lambda e:errors.append(str(e))))
        page=context.new_page()
        page.goto(f"http://127.0.0.1:{server.server_port}/")
        page.wait_for_function("document.getElementById('modeBadge').textContent.includes('MOCK')")
        assert page.locator("#lesson").input_value()=="oop_annotations"
        page.locator("#permission").check()
        with page.expect_response("**/api/generate") as received:
            page.locator("#generate").click()
        assert received.value.json()["generation_mode"]=="mock"
        page.wait_for_function("document.getElementById('status').textContent==='Chờ duyệt'")
        assert page.locator("#teach").is_disabled()
        page.locator("#reviewed").check()
        page.locator("#approve").click()
        assert page.locator("#status").inner_text()=="Đã duyệt"
        with page.expect_popup() as popup:
            page.locator("#teach").click()
        reader=popup.value
        reader.wait_for_selector("#clock")
        assert "Slide gốc:" in reader.locator("#current").inner_text()
        assert "không trình chiếu" in reader.locator(".notice").first.inner_text()
        reader.locator("#mark").click()
        assert "1/1" in reader.locator("#teachStats").inner_text()
        reader.locator("#timerToggle").click()
        expect(reader.locator("#clock")).not_to_have_text("60:00",timeout=5000)
        reader.locator("#timerReset").click()
        assert reader.locator("#clock").inner_text()=="60:00"
        with page.expect_download() as downloaded:
            page.locator("#exportJson").click()
        assert downloaded.value.suggested_filename=="teaching-script.json"
        page.locator("textarea[data-k=teacher_script]").first.fill("Lời dẫn đã sửa")
        assert page.locator("#teach").is_disabled()
        assert reader.is_closed()
        page.locator("#duration").fill("")
        page.locator("#generate").click()
        expect(page.locator("#inputNotice")).to_contain_text("duration_minutes")
        assert page.locator("#teach").is_disabled()
        assert not errors,errors
        browser.close()
        print("Browser smoke PASS: API request, review, private popup, timer, progress, JSON export, edit invalidation, clarification.")
finally:
    server.shutdown()
    server.server_close()
