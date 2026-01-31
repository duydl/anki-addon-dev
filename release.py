import fnmatch
import os
import shutil
import subprocess
import zipfile
from config import *

source_dir = os.path.abspath(os.path.dirname(__file__))

destination_dir = os.path.join(BASE, "addons21")
os.makedirs(destination_dir, exist_ok=True)

release_dir = os.path.join(source_dir, "_release")
os.makedirs(release_dir, exist_ok=True)

def should_ignore(path):
    rel = os.path.normpath(path)
    parts = rel.split(os.sep)
    for pattern in IGNORE_PATTERNS:
        if fnmatch.fnmatch(rel, pattern):
            return True
        if any(fnmatch.fnmatch(part, pattern) for part in parts):
            return True
    return False

def release_folder(item_path, item_name):

    new_item_name = f"_local-{item_name}"
    dest_path = os.path.join(destination_dir, new_item_name)

    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
        print(f"Removed existing directory: {dest_path}")

    shutil.copytree(item_path, dest_path)
    print(f"Copied {item_name} to {new_item_name} in {destination_dir}")

    zip_file_path = os.path.join(release_dir, f"{item_name}.zip")
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dest_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=dest_path)
                if should_ignore(arcname):
                    continue
                zipf.write(file_path, arcname)

    print(f"Zipped contents of {item_name} into {zip_file_path}")

for addon in ADDONS:
    # Run pre-release scripts for this addon
    for command in addon.get("scripts", []):
        print(f"Running script for {addon['path']}: {command}")
        subprocess.run(command, shell=True, check=True, cwd=source_dir)

    rel = addon["path"]
    item_path = os.path.join(source_dir, rel)
    item_name = os.path.basename(os.path.normpath(rel))
    if os.path.isdir(item_path):
        release_folder(item_path, item_name)

print("Complete!")
