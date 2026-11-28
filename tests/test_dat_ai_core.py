"""Unit tests cho phần AI Core của Đạt (D3-02..D3-09): ai, retrieval, tools, generator."""
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

import agent  # noqa: E402
import ai  # noqa: E402
import generator  # noqa: E402
import retrieval  # noqa: E402
import tools  # noqa: E402
import tracing  # noqa: E402


class _FakeHTTPResponse:
    def __init__(self, payload: dict):
        self._raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    def read(self):
        return self._raw

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _load_fixture(name: str):
    return json.loads((ROOT / "data" / "fixtures" / name).read_text(encoding="utf-8"))


def _load_oop_segments():
    data = json.loads((ROOT / "data" / "lessons" / "oop_annotations.json").read_text(encoding="utf-8"))
    return data["lessons"][0]["segments"]


class TestAIConnector(unittest.TestCase):
    def test_fake_mode_contract(self):
        with patch.object(ai, "MODEL_PROVIDER", "fake"):
            res = ai.call_model("sys", "hello world")
        self.assertEqual(res["model"], "fake")
        self.assertEqual(res["tokens_in"], 0)
        self.assertEqual(res["tokens_out"], 0)
        self.assertIn("hello world", res["text"])

    def test_openai_usage_extracted_and_traced(self):
        fake_resp = {
            "model": "gpt-4o-mini",
            "choices": [{"message": {"content": '{"ok": true}'}}],
            "usage": {"prompt_tokens": 120, "completion_tokens": 45},
        }
        tracing.begin("T-AI-OPENAI")
        try:
            with patch.object(ai, "MODEL_PROVIDER", "openai"), \
                 patch.object(ai, "MODEL_NAME", "gpt-4o-mini"), \
                 patch.object(ai, "API_KEY", "sk-test"), \
                 patch.object(ai, "API_BASE_URL", ""), \
                 patch("urllib.request.urlopen", return_value=_FakeHTTPResponse(fake_resp)):
                res = ai.call_model("system", "user")
        finally:
            summary, _ = tracing.end()

        self.assertEqual(res["tokens_in"], 120)
        self.assertEqual(res["tokens_out"], 45)
        self.assertEqual(summary["model_calls"], 1)
        self.assertEqual(summary["tokens_in"], 120)
        self.assertEqual(summary["tokens_out"], 45)

    def test_gemini_includes_thoughts_tokens(self):
        fake_resp = {
            "modelVersion": "gemini-2.5-flash",
            "candidates": [{"content": {"parts": [{"text": "{}"}]}}],
            "usageMetadata": {
                "promptTokenCount": 80,
                "candidatesTokenCount": 30,
                "thoughtsTokenCount": 20,
            },
        }
        with patch.object(ai, "MODEL_PROVIDER", "gemini"), \
             patch.object(ai, "MODEL_NAME", "gemini-2.5-flash"), \
             patch.object(ai, "API_KEY", "AIza-test"), \
             patch.object(ai, "API_BASE_URL", ""), \
             patch("urllib.request.urlopen", return_value=_FakeHTTPResponse(fake_resp)):
            res = ai.call_model("system", "user")
        self.assertEqual(res["tokens_in"], 80)
        self.assertEqual(res["tokens_out"], 50)

    def test_missing_api_key_raises_error(self):
        with patch.object(ai, "MODEL_PROVIDER", "openai"), \
             patch.object(ai, "MODEL_NAME", "gpt-4o-mini"), \
             patch.object(ai, "API_KEY", ""):
            with self.assertRaises(RuntimeError):
                ai.call_model("sys", "user")


class TestRetrievalAndTools(unittest.TestCase):
    def test_retrieve_short_lesson_keeps_all(self):
        docs = [{"code": "A01", "text": "Intro"}, {"code": "A02", "text": "Summary"}]
        out = retrieval.retrieve("Intro", docs, limit=12)
        self.assertEqual([d["code"] for d in out], ["A01", "A02"])

    def test_retrieve_oop_finds_relevant_segments_in_order(self):
        docs = _load_oop_segments()
        out = retrieval.retrieve("Customer domain constraint Mutator Observer OOP-P041", docs, limit=8)
        codes = [d["code"] for d in out]
        self.assertEqual(len(codes), 8)
        self.assertIn("OOP-P041", codes)
        # Kiểm tra thứ tự gốc được giữ nguyên
        indices = [next(i for i, d in enumerate(docs) if d["code"] == c) for c in codes]
        self.assertEqual(indices, sorted(indices))
        # Không tự bịa mã ngoài docs
        all_codes = {d["code"] for d in docs}
        self.assertTrue(set(codes).issubset(all_codes))

    def test_tools_registered_and_read_only(self):
        self.assertIn("get_slide_content", tracing.TOOLS)
        self.assertIn("get_teaching_strategy", tracing.TOOLS)
        docs = [{"code": "L01", "text": "Slide 1"}, {"code": "L02", "text": "Slide 2"}]
        found = tools.get_slide_content(["L02", "MISSING"], docs)
        self.assertEqual([s["code"] for s in found["segments"]], ["L02"])
        self.assertEqual(found["not_found"], ["MISSING"])

        strategies = tools.get_teaching_strategy({"duration_minutes": 15, "equipment": "Chỉ có bảng phấn, không có máy"})
        ids = {s["id"] for s in strategies}
        self.assertNotIn("TS04", ids)
        self.assertTrue(len(strategies) >= 1)


class TestGeneratorAndRealAgent(unittest.TestCase):
    def test_generator_repairs_invalid_timeline_then_succeeds(self):
        req = _load_fixture("lesson_request.json")
        valid_script = _load_fixture("script_response.json")
        bad_script = json.loads(json.dumps(valid_script))
        bad_script["segments"][0]["duration_minutes"] = 99  # Lỗi timeline

        calls = [
            {"text": json.dumps(bad_script, ensure_ascii=False), "model": "test-model", "tokens_in": 100, "tokens_out": 50},
            {"text": "```json\n" + json.dumps(valid_script, ensure_ascii=False) + "\n```", "model": "test-model", "tokens_in": 120, "tokens_out": 60},
        ]
        sources = [d for d in _load_oop_segments() if d["code"] in req["source_refs"]]

        with patch.object(ai, "call_model", side_effect=calls) as mock_call:
            out = generator.generate_script(req, sources)

        self.assertEqual(mock_call.call_count, 2)
        self.assertEqual(out["status"], "pending_review")
        self.assertEqual(out["model"], "test-model")

    def test_generator_stops_after_max_repairs(self):
        req = _load_fixture("lesson_request.json")
        bad_script = _load_fixture("script_response.json")
        bad_script["status"] = "approved"  # Bị cấm
        sources = [d for d in _load_oop_segments() if d["code"] in req["source_refs"]]

        resp = {"text": json.dumps(bad_script, ensure_ascii=False), "model": "test-model", "tokens_in": 50, "tokens_out": 20}
        with patch.object(ai, "call_model", return_value=resp) as mock_call:
            out = generator.generate_script(req, sources)

        # 1 lần gọi đầu + tối đa 2 lượt sửa = 3 lần gọi
        self.assertEqual(mock_call.call_count, 3)
        self.assertEqual(out["status"], "needs_clarification")
        self.assertEqual(out["reason_code"], "INVALID_SCRIPT")

    def test_agent_real_mode_end_to_end_with_trace(self):
        req = _load_fixture("lesson_request.json")
        valid_script = _load_fixture("script_response.json")
        resp = {"text": json.dumps(valid_script, ensure_ascii=False), "model": "gemini-2.5-flash", "tokens_in": 200, "tokens_out": 150}

        tracing.begin("T-REAL-E2E")
        try:
            with patch.object(ai, "MODEL_PROVIDER", "gemini"), \
                 patch.object(ai, "MODEL_NAME", "gemini-2.5-flash"), \
                 patch.object(ai, "call_model", return_value=resp):
                out = agent.build_response(req, mode="real")
        finally:
            summary, events = tracing.end()

        self.assertEqual(out["status"], "pending_review")
        self.assertEqual(out["generation_mode"], "real")
        self.assertGreaterEqual(summary["tool_calls"], 2)
        self.assertTrue(any(e["kind"] == "note" for e in events))

    def test_post_json_retries_on_503_and_429_then_succeeds(self):
        err_503 = urllib.error.HTTPError(
            url="https://example.com", code=503, msg="Unavailable", hdrs=None, fp=io.BytesIO(b"overload")
        )
        err_429 = urllib.error.HTTPError(
            url="https://example.com", code=429, msg="Too Many Requests", hdrs={"Retry-After": "1"}, fp=io.BytesIO(b"quota")
        )
        calls = [err_503, err_429, _FakeHTTPResponse({"ok": True})]

        with patch("urllib.request.urlopen", side_effect=calls) as mock_open, \
             patch("time.sleep") as mock_sleep:
            try:
                out = ai.post_json("https://example.com", {}, {"ping": 1}, max_retries=3, backoff_base=0.5)
            finally:
                err_503.close()
                err_429.close()

        self.assertEqual(out, {"ok": True})
        self.assertEqual(mock_open.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    def test_post_json_does_not_retry_on_400(self):
        err_400 = urllib.error.HTTPError(
            url="https://example.com", code=400, msg="Bad Request", hdrs=None, fp=io.BytesIO(b"bad payload")
        )
        with patch("urllib.request.urlopen", side_effect=[err_400]) as mock_open, \
             patch("time.sleep") as mock_sleep:
            try:
                with self.assertRaises(RuntimeError) as ctx:
                    ai.post_json("https://example.com", {}, {"ping": 1}, max_retries=3, backoff_base=0.5)
            finally:
                err_400.close()

        self.assertIn("HTTP 400", str(ctx.exception))
        self.assertEqual(mock_open.call_count, 1)
        self.assertEqual(mock_sleep.call_count, 0)

    def test_post_json_exhausts_max_retries(self):
        errors = [
            urllib.error.HTTPError(
                url="https://example.com", code=503, msg="Unavailable", hdrs=None, fp=io.BytesIO(b"overload")
            )
            for _ in range(3)
        ]
        with patch("urllib.request.urlopen", side_effect=errors) as mock_open, \
             patch("time.sleep") as mock_sleep:
            try:
                with self.assertRaises(RuntimeError) as ctx:
                    ai.post_json("https://example.com", {}, {"ping": 1}, max_retries=2, backoff_base=0.1)
            finally:
                for err in errors:
                    err.close()

        self.assertIn("HTTP 503", str(ctx.exception))
        self.assertEqual(mock_open.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    def test_repair_prompt_includes_sources_and_user_request(self):
        req = _load_fixture("lesson_request.json")
        sources = [d for d in _load_oop_segments() if d["code"] in req["source_refs"]]
        prompt = generator._build_repair_prompt(req, sources, '{"bad": true}', ["duration mismatch"])
        self.assertIn("<sources_data>", prompt)
        self.assertIn("<user_request>", prompt)
        self.assertIn(sources[0]["code"], prompt)

    def test_system_prompt_enforces_sequence_and_storytelling(self):
        self.assertIn("TUÂN THỦ CẤU TRÚC & THỨ TỰ", generator.SYSTEM_PROMPT)
        self.assertIn("kể chuyện đảo ngược", generator.SYSTEM_PROMPT)
        self.assertIn("theo thứ tự từ đầu đến cuối", generator.SYSTEM_PROMPT)


if __name__ == "__main__":
    unittest.main()
