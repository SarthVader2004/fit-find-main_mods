import os
import json
from PIL import Image
from tqdm import tqdm

def process_images(json_path, output_dir, size=(224, 224)):
    """
    Resize IndoFashion images and update JSON metadata.
    Fashion-MNIST entries are skipped since they are synthetic.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(json_path, "r") as f:
        data = json.load(f)

    processed_data = []
    for item in tqdm(data, desc="🪄 Processing images"):
        if "image_path" in item and os.path.exists(item["image_path"]):
            try:
                img = Image.open(item["image_path"]).convert("RGB")
                img = img.resize(size)
                filename = os.path.basename(item["image_path"])
                save_path = os.path.join(output_dir, filename)
                img.save(save_path)
                item["processed_path"] = save_path
                processed_data.append(item)
            except Exception as e:
                print(f"⚠️ Error processing {item['image_path']}: {e}")
        else:
            # Fashion-MNIST samples have no raw image files
            processed_data.append(item)

    os.makedirs("outputs", exist_ok=True)
    output_json = "./outputs/combined_preprocessed.json"
    with open(output_json, "w") as f:
        json.dump(processed_data, f, indent=2)

    print(f"✅ Saved preprocessed dataset → {output_json}")

if __name__ == "__main__":
    process_images("./processed/fitfind_combined.json", "./processed_images/indofashion")
