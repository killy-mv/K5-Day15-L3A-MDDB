import json
import os
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch
from urllib.request import Request, urlopen
from urllib.error import HTTPError
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"codebase"))
import agent, backend, tracing

class StudioTests(unittest.TestCase):
    def setUp(self):
        self.env=patch.dict(os.environ,{"TEACHFLOW_MODE":"mock"})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.request=json.loads((ROOT/"data/fixtures/lesson_request.json").read_text(encoding="utf8"))
        self.server=backend.make_server(0)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.url=f"http://127.0.0.1:{self.server.server_port}"

    def post(self,body,headers=None):
        return json.load(urlopen(Request(self.url+"/api/generate",data=json.dumps(body).encode(),
                   headers={"Content-Type":"application/json",**(headers or {})}),timeout=10))

    def test_health(self):
        self.assertEqual(json.load(urlopen(self.url+"/api/health"))["mode"],"mock")
    def test_studio(self):
        self.assertIn(b"/api/generate",urlopen(self.url+"/").read())
    def test_lessons(self):
        lessons=json.load(urlopen(self.url+"/api/lessons"))["lessons"]
        self.assertEqual(len(next(x for x in lessons if x["id"]=="oop_annotations")["segments"]),131)
    def test_generate(self):
        result=self.post(self.request)
        self.assertEqual(result["status"],"pending_review")
        self.assertEqual(result["generation_mode"],"mock")
        self.assertEqual(result["duration_minutes"],60)
        self.assertTrue(set(result["segments"][0]["slide_refs"])<=set(self.request["source_refs"]))
    def test_clarification(self):
        self.request["duration_minutes"]=None
        self.assertEqual(self.post(self.request)["status"],"needs_clarification")
    def test_bad_ref(self):
        self.request["source_refs"]=["A01"]
        self.assertEqual(self.post(self.request)["status"],"needs_clarification")
    def test_override(self):
        self.request["sources"]=[{"code":"X","text":"fake"}]
        self.assertEqual(self.post(self.request)["status"],"refused")
    def test_custom_permission(self):
        self.request.update(lesson_id="custom",sources=[{"code":"X","text":"source"}],permission=False)
        self.assertEqual(self.post(self.request)["status"],"needs_clarification")
    def test_cross_origin(self):
        with self.assertRaises(HTTPError) as err:self.post(self.request,{"Origin":"https://other.invalid"})
        self.assertEqual(err.exception.code,403)
    def test_bad_json(self):
        with self.assertRaises(HTTPError) as err:
            urlopen(Request(self.url+"/api/generate",data=b"{",headers={"Content-Type":"application/json"}))
        self.assertEqual(err.exception.code,400)
    def test_real_failure_no_fallback(self):
        with patch("agent.dependencies",side_effect=RuntimeError("secret-test")):
            with self.assertRaises(HTTPError) as err:self.post(self.request)
            self.assertEqual(err.exception.code,503)
            self.assertNotIn(b"secret-test",err.exception.read())
    def test_trace(self):
        tracing.begin("test")
        result=json.loads(agent.answer(json.dumps(self.request))["output"])
        summary,events=tracing.end()
        self.assertEqual(result["status"],"pending_review")
        self.assertEqual(summary["model_calls"],0)
        self.assertTrue(any("mode=mock" in x.get("text","") for x in events))
