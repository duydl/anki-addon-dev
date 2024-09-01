import os
import shutil
import zipfile

from config import *

source_dir = os.getcwd()

destination_dir = os.path.join(source_dir, 'addons21')
os.makedirs(destination_dir, exist_ok=True)

release_dir = os.path.join(source_dir, '_release')
os.makedirs(release_dir, exist_ok=True)

# Iterate over all items in source directory
for item_name in os.listdir(source_dir):
    item_path = os.path.join(source_dir, item_name)
    
    # Check if it's a directory and contains an __init__.py file
    if os.path.isdir(item_path) and '__init__.py' in os.listdir(item_path):
        # Define destination path
        new_item_name = f"_local-{item_name}"
        dest_path = os.path.join(destination_dir, new_item_name)
        
        # Remove existing directory
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
            print(f"Removed existing directory: {dest_path}")

        # Copy to destination directory
        shutil.copytree(item_path, dest_path)
        print(f"Copied {item_name} to {new_item_name} in {destination_dir}")

        # Zip the contents of the directory (not the directory itself)
        zip_file_path = os.path.join(release_dir, f"{item_name}.zip")
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(dest_path):
                for file in files:
                    if file not in ['meta.json', 'README.md']:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=dest_path)
                        zipf.write(file_path, arcname)
        print(f"Zipped contents of {item_name} into {zip_file_path}")
        
print("Complete!")
