import requests
from app.core.config import GEMINI_API_KEY

def call_gemini(query: str, context: str, lang: str):
    prompt = f"""
You are a helpful assistant. Answer the following question in the user's language: {lang} 
If the context does not contain relevant information, reply with "Sorry, I don't have enough information."

Context:
{context}

Question:
{query}

Answer:
"""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    res = requests.post(url, headers=headers, params=params, json=payload)
    print(res.text)  # Debugging line to see the response

    try:
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Error generating response."
