import os
from dotenv import load_dotenv
from api.fallback_engine import fallback_response

load_dotenv()  # ✅ Loads GROQCLOUD_API_KEY from .env

print("Testing Groq fallback...\n")
query = input("Enter your test query: ")
result = fallback_response(query)
print("\n🔍 Result:")
print(result)
