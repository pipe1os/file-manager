import os
import shutil

# from time import sleep

# TODO: add more file types later (maybe read from a json config?)
types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".wav", ".flac", ".ogg"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".dmg"],
    "Code": [".py", ".js", ".java", ".html", ".css", ".cpp"],
}


def getSize(bytes):
    # returns size in string format
    gb = bytes / (1024 * 1024 * 1024)
    if gb < 1:
        mb = bytes / (1024 * 1024)
        return f"{mb:.2f} MB"
    return f"{gb:.2f} GB"


def calc_folder_size(p):
    s = 0
    try:
        # print(f"DEBUG: Scanning {p}")
        for entry in os.scandir(p):
            if entry.is_file():
                s += entry.stat().st_size
                # print(f"  Found file: {entry.name} - {entry.stat().st_size}")
            elif entry.is_dir(follow_symlinks=False):
                s += calc_folder_size(entry.path)
    except PermissionError:
        # print(f"DEBUG: Permission denied at {p}")
        return 0
    except Exception as e:
        # print(f"Unknown error: {e}")
        return 0
    return s


def get_cat(ext):
    for k, v in types.items():
        if ext.lower() in v:
            return k
    return "Others"


# --- Main Stuff ---


def top_folders(path):
    print(f"Scanning folders in {path}...")

    if not os.path.exists(path):
        print("Path doesnt exist")
        return

    res = []

    try:
        for item in os.scandir(path):
            if item.is_dir():
                # TODO: this might be slow for huge directories, look into threading?
                sz = calc_folder_size(item.path)
                res.append((item.name, sz))
    except Exception as e:
        print(f"Error scanning: {e}")
        return

    res.sort(key=lambda x: x[1], reverse=True)

    print("\n--- Top 10 Folders ---")
    count = 1
    for name, size in res[:10]:
        print(f"{count}. {name} - {getSize(size)}")
        count += 1


def top_files(path):
    print("Looking for large files...")
    files_found = []

    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                sz = os.path.getsize(fp)
                files_found.append((f, sz))
            except Exception:
                # print(f"Skipping locked file: {f}")
                pass

    files_found.sort(key=lambda x: x[1], reverse=True)

    print("\n--- Top 10 Files ---")
    i = 1
    for name, sz in files_found[:10]:
        print(f"{i}. {name} - {getSize(sz)}")
        i += 1


def organize(path):
    print(f"Organizing {path}")
    m = 0

    # TODO: handle duplicate filenames (currently it might overwrite or crash?)
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in files:
        filename, ext = os.path.splitext(f)
        if not ext:
            continue

        cat = get_cat(ext)

        if cat != "Others":
            dest = os.path.join(path, cat)
            if not os.path.exists(dest):
                os.makedirs(dest)

            try:
                src = os.path.join(path, f)
                dst = os.path.join(dest, f)
                shutil.move(src, dst)
                print(f"Moved {f} -> {cat}")
                m += 1
            except Exception as e:
                print(f"Error moving file {f}: {e}")

    print(f"\nFinished. Moved {m} files.")


if __name__ == "__main__":
    p = input("Path: ").strip()

    while True:
        print("\n1. Top Folders")
        print("2. Top Files")
        print("3. Organize")
        print("4. Quit")

        op = input("Choice: ")

        if op == "1":
            top_folders(p)
        elif op == "2":
            top_files(p)
        elif op == "3":
            sure = input("Are you sure? (y/n): ")
            if sure == "y":
                organize(p)
        elif op == "4":
            break
        else:
            print("Invalid")
