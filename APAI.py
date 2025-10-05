#Bearer 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


from fastapi import FastAPI, Query
import requests

app = FastAPI(title="Multi-Model AI API")

API_KEY = "Bearer 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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "qwen/qwen2.5-coder-32b-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "qwen/qwen2.5-72b-instruct:free",
    "mistralai/mistral-nemo:free",
    "google/gemma-2-9b:free",
    "mistralai/mistral-7b-instruct:free"
]

model_index = 0

def ask_ai(question):
    global model_index
    headers = {
        "Authorization": API_KEY,
        "HTTP-Referer": "https://deta.space",
        "X-Title": "MultiModelAI",
        "Content-Type": "application/json"
    }

    model = MODELS[model_index % len(MODELS)]
    model_index += 1

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": question}]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()
    return {
        "model_used": model,
        "answer": data['choices'][0]['message']['content']
    }

@app.get("/")
def root():
    return {"status": "✅ API is running!"}

@app.get("/ask")
def ask(question: str = Query(...)):
    return ask_ai(question)
