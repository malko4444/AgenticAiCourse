import os
import shutil
import random

# Set paths
base_dir = 'PetImages'
output_base = 'PetImages_split'
categories = ['Cat', 'Dog']
split_ratio = 0.2  # 20% for validation

# Create output directories
for category in categories:
    for split in ['train', 'validation']:
        os.makedirs(os.path.join(output_base, split, category), exist_ok=True)

# Split and copy files
for category in categories:
    src_dir = os.path.join(base_dir, category)
    images = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]
    random.shuffle(images)
    split_idx = int(len(images) * (1 - split_ratio))
    train_imgs = images[:split_idx]
    val_imgs = images[split_idx:]

    for img in train_imgs:
        src = os.path.join(src_dir, img)
        dst = os.path.join(output_base, 'train', category, img)
        shutil.copy2(src, dst)
    for img in val_imgs:
        src = os.path.join(src_dir, img)
        dst = os.path.join(output_base, 'validation', category, img)
        shutil.copy2(src, dst)

print("Splitting complete. Check the 'PetImages_split' folder.")