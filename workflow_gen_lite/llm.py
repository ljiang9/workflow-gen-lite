"""可选 LLM 解析：仅用 urllib 走 OpenAI 兼容接口；无 key 时返回 None。"""
from __future__ import annotations
import json, os, urllib.request

SYSTEM = ("你是工作流解析器。把用户的自然语言解析成 JSON："
          '{"name": str, "steps": [{"id":"step_1","action":str,"mode":"sequential|parallel"}]}。'
          "只输出 JSON，不要解释。")


def llm_parse(utterance):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key: return None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    payload = {"model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
               "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": utterance}],
               "temperature": 0.0}
    req = urllib.request.Request(f"{base}/chat/completions", data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"].strip()
        m = content[content.find("{"):content.rfind("}") + 1]
        return json.loads(m)
    except Exception:
        return None
