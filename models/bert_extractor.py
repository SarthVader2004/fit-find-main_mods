from transformers import AutoTokenizer, AutoModel
import torch #type: ignore 
import numpy as np
import json
from tqdm import tqdm
import os


class BERTFeatureExtractor:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
    
    def extract(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
        return embeddings.tolist()


def extract_text_embeddings():
    print("💬 Extracting text embeddings using BERT...")
    extractor = BERTFeatureExtractor()
    
    with open("./outputs/combined_preprocessed.json", "r") as f:
        data = json.load(f)
    
    text_embeddings = {}
    for item in tqdm(data, desc="Extracting text features"):
        text_desc = ""
        if "category" in item:
            text_desc += item["category"] + " "
        if "attributes" in item and isinstance(item["attributes"], list):
            text_desc += " ".join(item["attributes"])
        if text_desc.strip():
            emb = extractor.extract(text_desc)
            text_embeddings[text_desc] = emb
    
    np.save("./outputs/text_embeddings.npy", text_embeddings)
    print("✅ Saved text embeddings to outputs/text_embeddings.npy")
    print(f"📊 Total text embeddings extracted: {len(text_embeddings)}")


if __name__ == "__main__":
    extract_text_embeddings()
