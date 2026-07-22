from fastapi import APIRouter, HTTPException
from api.fitfind_engine import generate_fitfind_response
from api.fallback_engine import fallback_response

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(payload: dict):
    """
    Combined chatbot endpoint:
    - Tries FitFind explainability first.
    - Then Groq fallback (always).
    - Returns both if possible.
    """
    query = payload.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Missing query text.")

    try:
        print(f"👗 User query: {query}")

        # Run both engines
        fitfind_result = generate_fitfind_response(query)
        groq_result = fallback_response(query)

        # Validate responses
        fitfind_valid = fitfind_result and fitfind_result.get("intent") != "fallback"

        # If FitFind worked → return both
        if fitfind_valid:
            print("🧠 FitFind success — combining with Groq fallback.")
            return {
                "intent": "combined",
                "fitfind_response": fitfind_result.get("response"),
                "fitfind_explanation": fitfind_result.get("explanation"),
                "groq_response": groq_result.get("response"),
                "groq_explanation": groq_result.get("explanation"),
                "note": "Showing both FitFind reasoning and Groq stylist insight."
            }

        # If FitFind failed → only Groq fallback
        else:
            print("🔁 FitFind failed — using Groq fallback only.")
            return groq_result

    except Exception as e:
        print(f"❌ Chatbot error: {e}")
        return {
            "intent": "fallback",
            "response": f"System error: {e}",
            "explanation": "Fallback triggered due to internal error."
        }
