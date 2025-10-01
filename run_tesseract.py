import pytesseract
from PIL import Image
import os
import json
import argparse
import random

#I have added another argument mode to select between single document processing and batch processing.

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, required=True,
                    help="Path to the parent dataset folder (e.g. ./images)")
parser.add_argument("--mode", type=int, choices=[1, 2], required=True,
                    help="1 = process only document1, 2 = process all document1..document20")
parser.add_argument("--sample-size", type=int, default=0)
parser.add_argument("--seed", type=int, default=0)

args = parser.parse_args()
print(args)

if args.dataset:
    img_folder = args.dataset
else:
    raise ValueError("Please provide a dataset path using --dataset")
results = []

def run_ocr_on_folder(folder_path, doc_name):
    """Run OCR on all images inside a given folder and return results list"""
    all_images = [name for name in os.listdir(folder_path)
                  if name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff'))]

    if not all_images:
        print(f"⚠️ No images found in {folder_path}")
        return []

    # sampling
    if args.sample_size > 0:
        rng = random.Random(args.seed)
        sample_count = min(args.sample_size, len(all_images))
        images = rng.sample(all_images, sample_count)
    else:
        images = all_images

    folder_results = []
    for img_name in images:
        try:
            img_path = os.path.join(folder_path, img_name)
            text = pytesseract.image_to_string(Image.open(img_path))
            folder_results.append({'document': doc_name,
                                   'image': img_name,
                                   'pred': text})
        except Exception as e:
            print("❌ Error with", img_name, ":", e)
            folder_results.append({'document': doc_name,
                                   'image': img_name,
                                   'pred': ""})
    return folder_results

# ---- Main Logic ----
if args.mode == 1:
    # only document1
    doc_folder = os.path.join(args.dataset, "document1")
    results.extend(run_ocr_on_folder(doc_folder, "document1"))

elif args.mode == 2:
    # all document1..document20
    for i in range(1, 21):
        doc_name = f"document{i}"
        doc_folder = os.path.join(args.dataset, doc_name)
        if os.path.isdir(doc_folder):
            print(f"📂 Processing {doc_name}...")
            results.extend(run_ocr_on_folder(doc_folder, doc_name))
        else:
            print(f"⚠️ Folder not found: {doc_folder}")

# save results
with open('tesseract_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"✅ Saved results for {len(results)} images")
