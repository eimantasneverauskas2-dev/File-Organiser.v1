from pathlib import Path
import shutil
import logging
from datetime import datetime

TARGET_DIR = Path.home() / "Downloads"


FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".raw"],
    "Videos":   [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
    "Audio":    [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Documents":[".pdf", ".doc", ".docx", ".txt", ".rtf"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code":     [".py", ".js", ".html", ".css", ".json"],
}

def resolve_conflict(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem = dest.stem
    suffix = dest.suffix
    counter = 1
    while dest.exists():
        dest = dest.parent / f"{stem} ({counter}){suffix}"
        counter += 1
    return dest

def setup_logging(log_dir: Path) -> None:
    log_file = log_dir / f"organiser_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
setup_logging(TARGET_DIR)
logging.info(f"Starting organiser on: {TARGET_DIR}")

for item in TARGET_DIR.iterdir():
    if item.is_dir():
        continue
    if item.suffix == ".log":
        continue
    if item.name.startswith("."):
        continue

    ext = item.suffix.lower()

    category = "Other"
    for folder_name, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            category = folder_name
            break
    
    dest_folder = TARGET_DIR / category
    dest_folder.mkdir(exist_ok=True)
    dest_path = resolve_conflict(dest_folder / item.name)
    shutil.move(str(item), str(dest_path))
    logging.info(f"Moved: {item.name} → {category}/")