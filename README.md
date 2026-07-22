Thank u for viewing my project. Disclaimer: Certain parts have been avoided due to LFS constraints. 

The work is majorly based on knowledge graphs, encoding and computer vision, and a proper chatbot for making better fashion choices. Also, most of my contributions have been to the ml and backend parts. My problem statement was the fact 
# that I struggled with making fashion choices according to my body type, seasons and occasions. Aftter all clothes are based on colors and similarity and why they go together fashion is data :))
I made this for a little better user experience but my work focused on knowledge graphs mostly. 

I also used an open source vton model for it to try on clothes. 

FitFind combines Natural Language Processing, Computer Vision, and Knowledge Graph reasoning to generate personalized fashion recommendations. BERT was chosen to understand the semantic meaning of user queries and extract fashion-related entities such as clothing type, color, and occasion. MobileNetV2 was used for efficient visual feature extraction, enabling similarity-based image search through embedding comparison. A NetworkX-based Knowledge Graph models relationships between garments, colors, fabrics, seasons, and occasions, allowing the system to produce explainable, context-aware recommendations instead of relying solely on similarity scores. When the Knowledge Graph cannot confidently answer a query, the system falls back to Groq's Qwen3 LLM to provide conversational styling advice.
GroqCloud api is used as a fallback!

Two datasets used: fashionmnist and indofashion dataset from kaggle. 


# 👗 FitFind – AI Fashion Recommendation & Styling Assistant

FitFind is a multimodal AI-powered fashion assistant that combines **Natural Language Processing, Computer Vision, and Knowledge Graph reasoning** to deliver personalized, explainable outfit recommendations for both Indian and Western fashion. It features a React frontend with a FastAPI backend for a seamless user experience

My choices for the 

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
