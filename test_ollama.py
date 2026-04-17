import requests

payload = {
    "model": "qwen2.5:3b",
    "prompt": "Return only this word: WORKING",
    "stream": False
}

response = requests.post(
    "http://localhost:11434/api/generate",
    json=payload,
    timeout=60
)

print(response.json()["response"])