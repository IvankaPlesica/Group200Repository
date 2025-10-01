import os, json
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
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

ocr = PaddleOCR(use_textline_orientation=True, lang='en')
#ocr = PaddleOCR(use_textline_orientation=True, lang='ch') # For Chinese
#ocr = PaddleOCR(use_textline_orientation=True, lang='ar') # For Arabic

for img_name in images:
    img_path = os.path.join(img_folder, img_name)
    try:
        pil_img = Image.open(img_path).convert("RGB")
        img_np = np.array(pil_img)
        ocr_result = ocr.predict(img_np)
        text_lines = ocr_result[0]['rec_texts']  # This gets the list of recognized text strings
        results.append({'image': img_name, 'pred': "\n".join(text_lines)})
    except Exception as e:
        print("Error with", img_name, ":", e)
        # Save empty prediction if error occurs for robust batching
        results.append({'image': img_name, 'pred': ""})    

with open('paddleocr_results.json', 'w', encoding='utf-8') as f: #will save in current directory
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved", len(results), "results")
