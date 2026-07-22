from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import uvicorn
import os

# ==========================================
# 🧩 Import Routers
# ==========================================
from api import chatbot_api, tryon_api  # ✅ Both backend modules

# ==========================================
# 🚀 Load Environment Variables
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_loaded = load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
print("📦 .env loaded:", dotenv_loaded)

# Read keys from .env
GROQ_KEY = os.getenv("GROQCLOUD_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

print(f" Groq Key Found: {bool(GROQ_KEY)}")
print(f" Hugging Face Token Found: {bool(HF_TOKEN)}")

# ==========================================
#  Initialize FastAPI App
# ==========================================
app = FastAPI(
    title="FitFind AI Fashion Assistant 👗",
    version="3.2",
    description=(
        "FitFind — A multimodal, explainable fashion recommendation system "
        "integrating NLP, Computer Vision, Knowledge Graph reasoning, and Virtual Try-On (IDM-VTON)."
    ),
)

# ==========================================
#  CORS Middleware (Frontend Integration)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Replace with your deployed frontend URL later (e.g. https://fitfind.vercel.app)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
#  Include API Routers
# ==========================================
app.include_router(chatbot_api.router, prefix="/api", tags=["Chatbot"])
app.include_router(tryon_api.router, prefix="/api", tags=["Virtual Try-On"])

# ==========================================
# Serve Static Files (Try-On Outputs)
# ==========================================
STATIC_DIR = os.path.join(BASE_DIR, "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ==========================================
#  Root Endpoint
# ==========================================
@app.get("/")
async def root():
    """Root endpoint to confirm API status and available routes."""
    return {
        "message": "✅ FitFind backend running successfully with Groq + IDM-VTON integration.",
        "available_routes": {
            "/api/chat": "💬 Chatbot with explainability + Groq fallback",
            "/api/tryon": "🧥 Virtual Try-On powered by IDM-VTON",
            "/api/tryon/gallery": "🖼️ Gallery endpoint for all try-on results",
            "/routes": "📜 List all routes for debugging",
        },
        "status": {
            "groq_key_loaded": bool(GROQ_KEY),
            "huggingface_token_loaded": bool(HF_TOKEN),
        },
    }

# ==========================================
# 🧭 Debug Route List
# ==========================================
@app.get("/routes")
async def list_routes():
    """List all registered routes (for quick debugging)."""
    return [{"path": route.path, "name": route.name} for route in app.router.routes]

# ==========================================
# ▶️ Run App
# ==========================================
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
