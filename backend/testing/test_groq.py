"""
Simple Groq API test - run this to verify your API key works
"""

from dotenv import load_dotenv
load_dotenv()

from groq import Groq
import os

api_key = os.getenv("GROQ_API_KEY")
print(f"Key loaded: {api_key[:10]}...{api_key[-4:]} (length: {len(api_key)})")

client = Groq(api_key=api_key)

print("Sending test request to Groq...")

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Say hello in one sentence."}
    ],
    temperature=1,
    max_completion_tokens=50,
    top_p=1,
    stream=False,
    stop=None
)

print("✅ Response:", completion.choices[0].message.content)
