from PIL import Image
import os

# Set your dataset directory
dataset_dir = 'PetImages_split'  # or 'PetImages' if you haven't split yet

bad_files = []

for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        file_path = os.path.join(root, file)
        try:
            img = Image.open(file_path)
            img.verify()  # Verify that it is, in fact, an image
        except Exception as e:
            print(f"Bad image: {file_path} ({e})")
            bad_files.append(file_path)

print(f"Found {len(bad_files)} bad images.")

# Optional: Remove bad images
for file_path in bad_files:
    os.remove(file_path)
    print(f"Removed: {file_path}")