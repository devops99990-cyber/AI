import os
import streamlit as st
import requests
import threading
from fastapi import FastAPI, Query
import uvicorn

# ============ CONFIGURATION ============
API_KEY = os.getenv("API_KEY")  # <-- Reads from environment variable
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
        "HTTP-Referer": "http://localhost",
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
        return f"⚠️ Error {response.status_code}: {response.text}"

    data = response.json()
    return f"🤖 **Model Used:** {model}\n\n{data['choices'][0]['message']['content']}"


# ============ FASTAPI ENDPOINT ============
app = FastAPI(title="Multi-Model AI API")

@app.get("/")
def root():
    return {"status": "✅ API is running!"}

@app.get("/ask")
def ask_endpoint(question: str = Query(..., description="Your question for the AI")):
    """Responds with AI-generated text from rotating models."""
    result = ask_ai(question)
    return {"answer": result}


# ============ STREAMLIT UI ============
def run_streamlit():
    st.set_page_config(page_title="AI Multi-Model Assistant", page_icon="🤖", layout="wide")

    st.markdown(
        """
        <h1 style='text-align:center; color:#00BFFF;'>💬 Multi-Model Local AI Assistant</h1>
        <p style='text-align:center;'>Ask anything — your assistant will use multiple AI models in rotation!</p>
        """,
        unsafe_allow_html=True,
    )

    user_input = st.text_input("🧠 Type your question:", placeholder="e.g. Explain computers briefly...")
    if st.button("Ask AI"):
        if user_input.strip():
            with st.spinner("Thinking... 🤔"):
                answer = ask_ai(user_input)
                st.markdown(answer)
        else:
            st.warning("Please enter a question before asking!")


if __name__ == "__main__":
    threading.Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error"), daemon=True).start()
    import os
    os.system("streamlit run APAI.py --server.port 8501")
