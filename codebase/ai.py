"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

URL_OPENAI = "https://api.openai.com/v1/chat/completions"
URL_CLAUDE = "https://api.anthropic.com/v1/messages"
URL_OLLAMA = "http://localhost:11434/api/chat"
URL_GEMINI_TMPL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
API_BASE_URL = (os.environ.get("API_BASE_URL") or "").strip()


def post_json(url: str, headers: dict, body: dict, timeout: int = 90) -> dict:
    """Gửi POST JSON bằng thư viện chuẩn urllib và trả về dict JSON."""
    req = urllib.request.Request(
        url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers),
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:400]
        raise RuntimeError(f"HTTP {e.code} từ API model: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Lỗi kết nối API model: {e.reason}") from e
    except TimeoutError as e:
        raise RuntimeError("Hết thời gian chờ phản hồi từ API model.") from e

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Phản hồi API không phải JSON hợp lệ: {raw[:200]}") from e
    if not isinstance(data, dict):
        raise RuntimeError("Phản hồi API phải là JSON object.")
    return data


def _require_nonempty(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"Thiếu cấu hình {name} trong .env.")
    return value.strip()


def _int_usage(value, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RuntimeError(f"Thiếu hoặc sai trường usage '{field_name}' trong phản hồi API.")
    return value


def _call_openai_compatible(system: str, user: str, model_name: str, api_key: str, base_url: str = "") -> dict:
    _require_nonempty(api_key, "API_KEY")
    _require_nonempty(model_name, "MODEL_NAME")
    url = (base_url.rstrip("/") + "/chat/completions") if base_url else URL_OPENAI
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(
        url,
        {"Authorization": f"Bearer {api_key}"},
        {"model": model_name, "messages": messages, "temperature": 0.2},
    )
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        raise RuntimeError("Phản hồi OpenAI-compatible thiếu choices.")
    message = choices[0].get("message") or {}
    text = message.get("content")
    if not isinstance(text, str):
        raise RuntimeError("Phản hồi OpenAI-compatible thiếu message.content.")
    usage = data.get("usage") or {}
    tokens_in = _int_usage(usage.get("prompt_tokens"), "prompt_tokens")
    tokens_out = _int_usage(usage.get("completion_tokens"), "completion_tokens")
    return {"text": text, "model": data.get("model") or model_name, "tokens_in": tokens_in, "tokens_out": tokens_out}


def _call_gemini(system: str, user: str, model_name: str, api_key: str) -> dict:
    _require_nonempty(api_key, "API_KEY")
    _require_nonempty(model_name, "MODEL_NAME")
    clean_model = model_name.removeprefix("models/")
    base = API_BASE_URL.rstrip("/") if API_BASE_URL else ""
    if base:
        url = f"{base}/models/{urllib.parse.quote(clean_model)}:generateContent"
    else:
        url = URL_GEMINI_TMPL.format(model=urllib.parse.quote(clean_model))
    body = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"temperature": 0.2},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(url, {"x-goog-api-key": api_key}, body)
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise RuntimeError(f"Phản hồi Gemini thiếu candidates: {json.dumps(data, ensure_ascii=False)[:300]}")
    parts = ((candidates[0].get("content") or {}).get("parts")) or []
    text = "".join(p.get("text", "") for p in parts if isinstance(p, dict) and isinstance(p.get("text"), str))
    if not text:
        raise RuntimeError("Phản hồi Gemini không có nội dung text.")
    usage = data.get("usageMetadata") or {}
    tokens_in = _int_usage(usage.get("promptTokenCount"), "promptTokenCount")
    cand_tokens = _int_usage(usage.get("candidatesTokenCount"), "candidatesTokenCount")
    thoughts_tokens = usage.get("thoughtsTokenCount") or 0
    if isinstance(thoughts_tokens, bool) or not isinstance(thoughts_tokens, int) or thoughts_tokens < 0:
        thoughts_tokens = 0
    return {
        "text": text,
        "model": data.get("modelVersion") or clean_model,
        "tokens_in": tokens_in,
        "tokens_out": cand_tokens + thoughts_tokens,
    }


def _call_anthropic(system: str, user: str, model_name: str, api_key: str) -> dict:
    _require_nonempty(api_key, "API_KEY")
    _require_nonempty(model_name, "MODEL_NAME")
    url = (API_BASE_URL.rstrip("/") + "/messages") if API_BASE_URL else URL_CLAUDE
    data = post_json(
        url,
        {"x-api-key": api_key, "anthropic-version": "2023-06-01"},
        {
            "model": model_name,
            "max_tokens": 4096,
            "temperature": 0.2,
            "system": system or "",
            "messages": [{"role": "user", "content": user}],
        },
    )
    blocks = data.get("content") or []
    text = "".join(b.get("text", "") for b in blocks if isinstance(b, dict) and b.get("type") == "text")
    if not text:
        raise RuntimeError("Phản hồi Anthropic không có nội dung text.")
    usage = data.get("usage") or {}
    tokens_in = _int_usage(usage.get("input_tokens"), "input_tokens")
    tokens_out = _int_usage(usage.get("output_tokens"), "output_tokens")
    return {"text": text, "model": data.get("model") or model_name, "tokens_in": tokens_in, "tokens_out": tokens_out}


def _call_ollama(system: str, user: str, model_name: str) -> dict:
    _require_nonempty(model_name, "MODEL_NAME")
    url = (API_BASE_URL.rstrip("/") + "/api/chat") if API_BASE_URL else URL_OLLAMA
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {}, {"model": model_name, "messages": messages, "stream": False}, timeout=300)
    message = data.get("message") or {}
    text = message.get("content")
    if not isinstance(text, str):
        raise RuntimeError("Phản hồi Ollama thiếu message.content.")
    tokens_in = _int_usage(data.get("prompt_eval_count"), "prompt_eval_count")
    tokens_out = _int_usage(data.get("eval_count"), "eval_count")
    return {"text": text, "model": data.get("model") or model_name, "tokens_in": tokens_in, "tokens_out": tokens_out}


@model_call
def call_model(system: str, user: str) -> dict:
    provider = (MODEL_PROVIDER or "fake").strip().lower()
    if provider == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if provider in ("openai", "openrouter", "deepseek", "groq", "openai_compatible"):
        return _call_openai_compatible(system, user, MODEL_NAME, API_KEY, API_BASE_URL)
    if provider == "gemini":
        return _call_gemini(system, user, MODEL_NAME, API_KEY)
    if provider in ("anthropic", "claude"):
        return _call_anthropic(system, user, MODEL_NAME, API_KEY)
    if provider == "ollama":
        return _call_ollama(system, user, MODEL_NAME)
    raise RuntimeError(f"MODEL_PROVIDER không được hỗ trợ: {provider}")
