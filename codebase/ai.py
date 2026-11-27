"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI.
Hỗ trợ chế độ giả (fake) cho CP2 và API Anthropic (Claude Haiku 5.5) / OpenAI / Ollama cho CP3+.
"""
import json
import os
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW_RAW = False


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có."""
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


def post_json(url, headers, body, timeout=60):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib)."""
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers),
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def call_claude(system, user):
    url = "https://api.anthropic.com/v1/messages"
    data = post_json(
        url,
        {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
        {
            "model": MODEL_NAME,
            "max_tokens": 1024,
            "system": system or "",
            "messages": [{"role": "user", "content": user}],
        },
    )
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data["usage"]
    return {"text": text, "tokens_in": u["input_tokens"], "tokens_out": u["output_tokens"]}


def call_openai(system, user):
    url = "https://api.openai.com/v1/chat/completions"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {"Authorization": "Bearer " + API_KEY}, {"model": MODEL_NAME, "messages": messages})
    u = data["usage"]
    return {
        "text": data["choices"][0]["message"]["content"],
        "tokens_in": u["prompt_tokens"],
        "tokens_out": u["completion_tokens"],
    }


def call_ollama(system, user):
    url = "http://localhost:11434/api/chat"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {
        "text": data["message"]["content"],
        "tokens_in": data.get("prompt_eval_count", 0),
        "tokens_out": data.get("eval_count", 0),
    }


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {
            "text": "[câu trả lời giả — chưa nối model] " + last[:80],
            "model": "fake",
            "tokens_in": 0,
            "tokens_out": 0,
        }
    if MODEL_PROVIDER == "anthropic":
        r = call_claude(system, user)
    elif MODEL_PROVIDER == "openai":
        r = call_openai(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = call_ollama(system, user)
    else:
        raise NotImplementedError(
            "MODEL_PROVIDER=%s chưa được hỗ trợ trong codebase/ai.py — xem docs/connect-model.md" % MODEL_PROVIDER
        )
    return {
        "text": r["text"],
        "model": MODEL_NAME,
        "tokens_in": int(r["tokens_in"]),
        "tokens_out": int(r["tokens_out"]),
    }
