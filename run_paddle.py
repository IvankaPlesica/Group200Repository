# run_paddle.py
import os
import json
import argparse
import random
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR

#I have added another argument mode to select between single document processing and batch processing.

parser = argparse.ArgumentParser(description="Run PaddleOCR on document folders.")
parser.add_argument("--dataset", type=str, required=True,
                    help="Path to parent dataset folder containing document1..document20")
parser.add_argument("--mode", type=int, choices=[1, 2], required=True,
                    help="1 = process only document1, 2 = process all document1..document20")
parser.add_argument("--sample-size", type=int, default=0)
parser.add_argument("--seed", type=int, default=0)
args = parser.parse_args()
print("Args:", args)



if not os.path.isdir(args.dataset):
    raise ValueError(f"Dataset path does not exist or is not a directory: {args.dataset}")


IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp')

# initialize PaddleOCR once
ocr = PaddleOCR(use_textline_orientation=True, lang='en')
#ocr = PaddleOCR(use_textline_orientation=True, lang='ch') # For Chinese
#ocr = PaddleOCR(use_textline_orientation=True, lang='ar') # For Arabic

def list_images_in_folder(folder_path):
    """Return list of image filenames in a folder."""
    if not os.path.isdir(folder_path):
        return []
    return [f for f in sorted(os.listdir(folder_path))
            if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(IMAGE_EXTS)]


def run_ocr_on_folder(folder_path, doc_name):
    """Run PaddleOCR on all (or sampled) images in folder_path. Returns list of results dicts."""
    all_images = list_images_in_folder(folder_path)
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
        img_path = os.path.join(folder_path, img_name)
        try:
            pil_img = Image.open(img_path).convert("RGB")
            img_np = np.array(pil_img)
            # modern API: predict; fallback to ocr if needed
            ocr_res = ocr.predict(img_np)
            text_lines = ocr_res[0]['rec_texts']  # This gets the list of recognized text strings
            text = "\n".join(text_lines).strip()
            folder_results.append({'document': doc_name, 'image': img_name, 'pred': text})
        except Exception as e:
            print("❌ Error with", img_name, ":", e)
            folder_results.append({'document': doc_name, 'image': img_name, 'pred': ""})
    return folder_results

# ----------------- Main logic -----------------
results = []

if args.mode == 1:
    # Only process document1
    doc_folder = os.path.join(args.dataset, "document1")
    if not os.path.isdir(doc_folder):
        raise ValueError(f"Expected to find {doc_folder} but it does not exist.")
    print(f"Processing single document: {doc_folder}")
    results.extend(run_ocr_on_folder(doc_folder, "document1"))

elif args.mode == 2:
    # Batch processing: document1..document20
    for i in range(1, 21):
        doc_name = f"document{i}"
        doc_folder = os.path.join(args.dataset, doc_name)
        if os.path.isdir(doc_folder):
            print(f"Processing {doc_name} ...")
            results.extend(run_ocr_on_folder(doc_folder, doc_name))
        else:
            print(f"⚠️ Folder not found, skipping: {doc_folder}")

# Save results
out_file = 'paddleocr_results.json'
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"✅ Saved {len(results)} results to {out_file}")

