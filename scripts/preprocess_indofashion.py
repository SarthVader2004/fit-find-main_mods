import json
import os

def preprocess_indofashion(input_json_path, images_dir, output_path):
    data = []
    
    # ✅ Handle both normal JSON and line-by-line JSON
    with open(input_json_path, "r") as f:
        try:
            # Try to load as full JSON array
            data = json.load(f)
        except json.JSONDecodeError:
            # If that fails, assume newline-delimited JSON
            f.seek(0)
            for line in f:
                line = line.strip()
                if line:
                    try:
                        item = json.loads(line)
                        data.append(item)
                    except json.JSONDecodeError:
                        continue

    processed = []
    for item in data:
        image_path = os.path.join(images_dir, item.get('image_path', ''))
        processed.append({
            "image_path": image_path,
            "category": item.get('category', 'unknown'),
            "gender": item.get('gender', 'unisex'),
            "attributes": item.get('attributes', []),
            "source": "indofashion"
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(processed, f, indent=2)

    print(f"✅ Processed {len(processed)} IndoFashion entries → {output_path}")
    return processed
