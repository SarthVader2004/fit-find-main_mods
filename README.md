Thank u for viewing my project. Disclaimer: Certain parts have been avoided due to LFS constraints. 

The work is mainly based on knowledge graphs, encoding and computer vision, and a proper chatbot for making better fashion choices. Also, most of my contributions have been to the ml and backend parts. My problem statement was the fact 
# that I struggled with making fashion choices according to my body type, seasons and occasions. After all clothes are based on colours and similarity, and why they go together; fashion is data :))
I made this for a little better user experience but my work focused on knowledge graphs mostly. 

I also used an open-source vton model for it to try on clothes. 

FitFind combines Natural Language Processing, Computer Vision, and Knowledge Graph reasoning to generate personalized fashion recommendations. BERT was chosen to understand the semantic meaning of user queries and extract fashion-related entities such as clothing type, color, and occasion. MobileNetV2 was used for efficient visual feature extraction, enabling similarity-based image search through embedding comparison. A NetworkX-based Knowledge Graph models relationships between garments, colors, fabrics, seasons, and occasions, allowing the system to produce explainable, context-aware recommendations instead of relying solely on similarity scores. When the Knowledge Graph cannot confidently answer a query, the system falls back to Groq's Qwen3 LLM to provide conversational styling advice.
GroqCloud api is used as a fallback!

# Problems I've faced 
1. Switching between encoders
2. Getting my teammates to stop giving the **Mbappe Special** to the coding contributions
3. Juggling through api endpoints
4. API key failures ( too many to count)

# Improvements:
Honest opinion-> the machine learning parts are good; there needs to be better UI, it could be developed more. The project is more adaptable breadth-wise. Individual VTON could be implemented. 

Two datasets used: fashionmnist and indofashion dataset from kaggle. 


# Images 

<img width="424" height="556" alt="image" src="https://github.com/user-attachments/assets/2373c07c-a4b5-464e-b280-ba5bbdc6dcda" />
<img width="1600" height="703" alt="image" src="https://github.com/user-attachments/assets/b2f980ac-97df-4ae6-adb1-cac5c6d42db1" />
<img width="1600" height="690" alt="image" src="https://github.com/user-attachments/assets/9adc8ba4-6ae3-452d-b865-85c16ce70020" />
<img width="424" height="433" alt="image" src="https://github.com/user-attachments/assets/c275833a-6a5f-487e-ab01-a56a7ca574cf" />




# References I used to come up with the idea 
References
[1] A. K. Kushwaha, S. Singh, and B. Raman, “IndoFashion: A Fine-Grained Fashion Dataset for Categorizing
Indian Apparel,”arXiv preprint arXiv:2004.09954, Apr. 2020.
[2] H. Xiao, K. Rasul, and R. Vollgraf, “Fashion-MNIST: A Novel Image Dataset for Benchmarking Machine
Learning Algorithms,” arXiv preprint arXiv:1708.07747, Aug. 2017.
[3] Z. Cheng, W. Song, Y. Wang, and B. Wu,“IDM-VTON: Implicit Diffusion Models for Virtual Try-On,”arXiv
preprint arXiv:2303.16828, Mar. 2023.
[4] S. Han, H. Lee, and S. Choi,“Virtual Try-On: A Comprehensive Survey,”ACM Comput. Surv., vol. 55, no. 14,
pp. 1–39, Dec. 2022.
[5] W. Kang, J. Lee, and D. Kim,“FashionKGB: A Knowledge Graph Benchmark for Fashion
Recommendation,”
in Proc. ACM SIGKDD Workshop, 2021, pp. 1–8.
[6] Y. Zhao, Q. Xie, Y. Li, and L. Nie, “FashionKG: A Large-scale Knowledge Graph for Fashion
Recommendation,” IEEE Trans. Multimedia, vol. 24, pp. 3081–3093, 2022.
[7] A. Veit, S. Belongie, and T. Kovacs, “Learning Visual Clothing Style with Similarity Metrics,” in Proc. IEEE
Conf. Comput. Vis. Pattern Recognit. (CVPR), 2015, pp. 5410–5419.
[8] R. Lin, S. Wang, and X. He,“OutfitNet: Fashion Outfit Recommendation Using Attention Networks,” in Proc.
Eur. Conf. Comput. Vis. (ECCV) Workshops, 2020, pp. 1–11.



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
