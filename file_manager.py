import os
import shutil
import json
from concurrent.futures import ThreadPoolExecutor

CONFIG_FILE = "file_types.json"

try:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f: 
        types = json.load(f)
except:
    # fallback
    types = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv"],
        "Audio": [".mp3", ".wav", ".flac"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Archives": [".zip", ".rar", ".7z", ".tar.gz"],
        "Executables": [".exe", ".msi"],
        "Code": [".py", ".js", ".java", ".html", ".css", ".json"],
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(types, f, indent=4)


def getSize(bytes):
    gb = bytes / (1024 * 1024 * 1024)
    if gb < 1:
        mb = bytes / (1024 * 1024)
        return f"{mb:.2f} MB"
    return f"{gb:.2f} GB"

def calc_folder_size(p):
    s = 0
    try:
        for entry in os.scandir(p):
            if entry.is_file():
                s += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                s += calc_folder_size(entry.path)
    except:
        return 0
    return s

def get_cat(ext):
    for k, v in types.items():
        if ext.lower() in v:
            return k
    return "Others"

def top_folders(path):
    print(f"Scanning folders in {path}...")
    if not os.path.exists(path):
        return

    res = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        try:
            for item in os.scandir(path):
                if item.is_dir():
                    futures.append((item.name, executor.submit(calc_folder_size, item.path)))
        except:
            return

        for name, future in futures:
            res.append((name, future.result()))

    res.sort(key=lambda x: x[1], reverse=True)

    print("\n--- Top Folders ---")
    count = 1
    for name, size in res[:10]:
        print(f"{count}. {name} - {getSize(size)}")
        count += 1

def top_files(path):
    files_found = []

    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                files_found.append((f, os.path.getsize(fp)))
            except:
                pass

    files_found.sort(key=lambda x: x[1], reverse=True)

    print("\n--- Top Files ---")
    i = 1
    for name, sz in files_found[:10]:
        print(f"{i}. {name} - {getSize(sz)}")
        i += 1

def organize(path):
    m = 0
    files = sorted([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))], reverse=True)

    for f in files:
        filename, ext = os.path.splitext(f)
        if not ext:
            continue

        cat = get_cat(ext)
        dest_folder = os.path.join(path, cat)

        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        src = os.path.join(path, f)
        dst = os.path.join(dest_folder, f)

        counter = 1
        while os.path.exists(dst):
            dst = os.path.join(dest_folder, f"{filename}_{counter}{ext}")
            counter += 1

        try:
            shutil.move(src, dst)
            m += 1
        except:
            print(f"failed on {f}")

    print(f"\nMoved {m} files.")


if __name__ == "__main__":
    p = input("Path: ").strip().strip('"').strip("'")

    while True:
        print("\n1. Top Folders")
        print("2. Top Files")
        print("3. Organize")
        print("4. Quit")

        op = input("> ")

        if op == "1":
            top_folders(p)
        elif op == "2":
            top_files(p)
        elif op == "3":
            if input("Sure? (y/n): ").lower() == "y":
                organize(p)
        elif op == "4":
            break