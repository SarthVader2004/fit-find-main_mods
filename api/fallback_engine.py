import os
from groq import Groq

def fallback_response(user_query: str):
    """
    Handles fallback using Groq SDK (Qwen3-32B model).
    Generates short, stylish, and natural outfit advice (1–2 short paragraphs max).
    Focuses on colors, fabrics, and gender-appropriate outfit ideas.
    """
    api_key = os.getenv("GROQCLOUD_API_KEY")

    if not api_key:
        print("ℹ️ No GroqCloud API key found — using static fallback.")
        return {
            "intent": "fallback",
            "response": (
                f"Sorry, I couldn’t find specific advice for '{user_query}'. "
                "Try something like 'red kurta for wedding' or 'casual college outfit'."
            ),
            "explanation": "Used local fallback message."
        }

    try:
        client = Groq(api_key=api_key)
        print("⚙️ Using GroqCloud (Qwen3-32B) fallback...")

        completion = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are FitFind Stylist — a professional multicultural fashion expert. "
                        "Give natural, confident advice in 1–2 short paragraphs (max 5–6 lines total). "
                        "Mention key fabrics, color pairings, and outfit ideas for men and women if relevant. "
                        "Avoid long explanations, lists, or over-detailing — keep it crisp, elegant, and user-focused."
                    )
                },
                {"role": "user", "content": user_query},
            ],
            temperature=0.7,
            max_completion_tokens=250,
            top_p=0.9,
        )

        message = completion.choices[0].message.content.strip()

        return {
            "intent": "fallback",
            "response": f"👗 Stylist:\n{message}",
            "explanation": "Response generated using GroqCloud (Qwen3-32B) stylist model."
        }

    except Exception as e:
        print(f"⚠️ Groq fallback error: {e}")
        return {
            "intent": "fallback",
            "response": f"Groq API error: {e}",
            "explanation": "Local fallback triggered after Groq failure."
        }
