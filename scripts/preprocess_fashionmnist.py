import os
import json
from torchvision import datasets, transforms #type: ignore
from tqdm import tqdm
from PIL import Image

def preprocess_fashionmnist(output_json_path="outputs/fashion_mnist_cleaned.json", image_dir="processed_images/fashion_mnist"):
    """
    Preprocess Fashion-MNIST dataset:
    - Loads data using torchvision
    - Converts grayscale images to RGB
    - Saves as PNGs for consistency
    - Creates JSON metadata for each image
    """
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    print("🧼 Preprocessing Fashion-MNIST dataset...")

    # Define transform (convert to tensor first)
    transform = transforms.Compose([
        transforms.ToTensor()
    ])

    # Load training dataset
    dataset = datasets.FashionMNIST(root="data/fashion_mnist", train=True, download=True, transform=transform)

    # Map label indices to human-readable categories
    LABELS = [
        "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
        "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
    ]

    data_records = []

    for idx, (img_tensor, label) in enumerate(tqdm(dataset, desc="Processing Fashion-MNIST images")):
        try:
            category = LABELS[label]
            # Convert tensor to PIL Image
            img = transforms.ToPILImage()(img_tensor).convert("RGB")
            img_filename = f"fashion_mnist_{idx}.png"
            img_path = os.path.join(image_dir, img_filename)
            img.save(img_path)

            record = {
                "id": idx,
                "dataset": "fashion_mnist",
                "category": category,
                "image_path": img_path.replace("\\", "/"),
                "attributes": []
            }
            data_records.append(record)

        except Exception as e:
            print(f"⚠️ Error processing index {idx}: {e}")

    # Save metadata as JSON
    with open(output_json_path, "w") as f:
        json.dump(data_records, f, indent=2)

    print(f"✅ Fashion-MNIST preprocessing complete! Saved {len(data_records)} items to {output_json_path}")

    return data_records


if __name__ == "__main__":
    preprocess_fashionmnist()
