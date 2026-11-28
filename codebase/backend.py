"""Loopback-only HTTP server; no external dependencies, no API key in browser."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json

import agent
import tracing
import contract_mock

BASE = Path(__file__).resolve().parent
MAX_BODY = 2_000_000


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload, content_type="application/json; charset=utf-8"):
        data = payload if isinstance(payload, bytes) else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
        self.end_headers()
        self.wfile.write(data)

    def _error(self, status, message, reason="BAD_REQUEST"):
        self._send(status, {"status": "error", "message": message, "reason_code": reason})

    def _local_host(self):
        host = self.headers.get("Host", "")
        return host in (f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}")

    def _same_origin(self):
        origin = self.headers.get("Origin")
        return origin is None or origin in (
            f"http://127.0.0.1:{self.server.server_port}",
            f"http://localhost:{self.server.server_port}")

    def do_GET(self):
        if not self._local_host():
            return self._error(403, "Chỉ truy cập từ máy local.")
        path = urlsplit(self.path).path
        if path == "/":
            return self._send(200, (BASE / "studio.html").read_bytes(), "text/html; charset=utf-8")
        if path == "/api/health":
            return self._send(200, {"status": "ok", "mode": agent.active_mode()})
        if path == "/api/lessons":
            # Deliberately expose only the curated shared dataset, never arbitrary paths.
            lessons = []
            for name in ("teachflow_examples.json", "oop_annotations.json"):
                lessons.extend(contract_mock._load(contract_mock.ROOT / "data" / "lessons" / name)["lessons"])
            return self._send(200, {"lessons": lessons})
        return self._error(404, "Không tìm thấy endpoint.")

    def do_POST(self):
        if not self._local_host() or not self._same_origin():
            return self._error(403, "Yêu cầu ngoài local origin.")
        if urlsplit(self.path).path != "/api/generate":
            return self._error(404, "Không tìm thấy endpoint.")
        if self.headers.get_content_type() != "application/json":
            return self._error(415, "Content-Type phải là application/json.")
        try:
            n = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self._error(400, "Content-Length không hợp lệ.")
        if not 0 < n <= MAX_BODY:
            return self._error(413, "Yêu cầu rỗng hoặc vượt 2 MB.")
        try:
            text = self.rfile.read(n).decode("utf-8")
            value = json.loads(text)
        except (ValueError, UnicodeDecodeError):
            return self._error(400, "JSON UTF-8 không hợp lệ.")
        if not isinstance(value, dict):
            return self._error(400, "Input phải là JSON object.")
        # Single-threaded server because starter tracing uses global per-case state.
        tracing.begin("web")
        try:
            result = json.loads(agent.answer(text)["output"])
        except Exception as exc:
            # Provider details may contain secrets; never echo them into the browser.
            print("Generate failed:", type(exc).__name__)
            return self._error(503, "Không thể sinh kịch bản. Kiểm tra cấu hình/module/model ở máy chủ.", "MODEL_ERROR")
        finally:
            tracing.end()
        result["generation_mode"] = agent.active_mode()
        return self._send(200, result)


def make_server(port=8765):
    return HTTPServer(("127.0.0.1", port), Handler)
