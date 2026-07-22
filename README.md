Thank u for viewing my project. Disclaimer: Certain parts have been avoided due to LFS constraints. 

The work is majorly based on knowledge graphs and encoding and computer visison and a proper chatbot for making better fashion choices. 
GroqCloud api is used as a fallback!

Two datasets used: fashionmnist and indofashion dataset from kaggle. 


# 👗 FitFind – AI Fashion Recommendation & Styling Assistant

FitFind is a multimodal AI-powered fashion assistant that combines **Natural Language Processing, Computer Vision, and Knowledge Graph reasoning** to deliver personalized, explainable outfit recommendations for both Indian and Western fashion. It features a React frontend with a FastAPI backend for a seamless user experience. :contentReference[oaicite:0]{index=0}

## 🚀 Features

- 🤖 AI-powered fashion chatbot
- 🧠 BERT-based natural language understanding
- 🖼️ MobileNetV2 visual similarity search
- 🌐 Knowledge Graph-based explainable recommendations
- 👗 Virtual Try-On prototype (IDM-VTON)
- 📏 Body Shape Analyzer
- 💬 Groq (Qwen3) fallback stylist for open-ended fashion advice

## 🛠️ Tech Stack

- **Frontend:** React.js, Vite, Tailwind CSS
- **Backend:** FastAPI, Python
- **ML:** BERT, MobileNetV2, OpenCV, NetworkX, Transformers
- **AI:** Groq (Qwen3), IDM-VTON

## 🧠 How It Works

1. User enters a text query or uploads an image.
2. **BERT** extracts semantic information from the query.
3. **MobileNetV2** generates image embeddings for visual search.
4. A **Knowledge Graph** built using NetworkX reasons over clothing categories, colors, occasions, and styles to produce explainable recommendations.
5. If no suitable KG match is found, the system falls back to **Groq's Qwen3 LLM** for conversational styling advice.

## 📂 Note

To keep the repository lightweight, large datasets, processed images, trained models, generated outputs, and virtual environments have been excluded from this repository.
