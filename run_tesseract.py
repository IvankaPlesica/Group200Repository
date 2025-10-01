import pytesseract
from PIL import Image
import os
import json
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("--sample-size", type=int, default=0)
parser.add_argument("--seed", type=int, default=0)
parser.add_argument("--dataset", type=str)

args = parser.parse_args()
print(args)

if args.dataset:
    img_folder = args.dataset
else:
    raise ValueError("Please provide a dataset path using --dataset")
results = []

all_images = [
    name for name in os.listdir(img_folder)
    if name.endswith(('.png', '.jpg', '.jpeg', '.tiff'))
]

if not all_images or len(all_images) == 0:
    raise ValueError("No images found in the specified folder.")

if args.sample_size > 0:
    rng = random.Random(args.seed)
    sample_count = min(args.sample_size, len(all_images))
    images = rng.sample(all_images, sample_count)
else:
    images = all_images

for img_name in images:
    if not img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')):
        continue
    try:    
        img_path = os.path.join(img_folder, img_name)
        text = pytesseract.image_to_string(Image.open(img_path))
        results.append({'image': img_name, 'pred': text})
    except Exception as e:
        print("❌ Error with", img_name, ":", e)
        # Save empty prediction if error occurs for robust batching
        results.append({'image': img_name, 'pred': ""})

with open('tesseract_results.json', 'w', encoding='utf-8') as f:  #will save in current directory
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ Saved", len(results), "results")
