import tkinter as tk
from tkinter import filedialog
import threading
from pathlib import Path
import shutil
from datetime import datetime

window = tk.Tk()
window.title("File Organiser")
window.geometry("500x400")
window.config(bg="#1e1e2e")
window.tk_setPalette(background="#1e1e2e")

selected_folder = tk.StringVar()
selected_folder.set("No folder selected")

FILE_CATEGORIES = {
    "Images":   [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".raw"],
    "Videos":   [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
    "Audio":    [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Documents":[".pdf", ".doc", ".docx", ".txt", ".rtf"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code":     [".py", ".js", ".html", ".css", ".json"],
}

label = tk.Label(window, text="File Organiser", font=("Arial", 20, "bold"), bg="#1e1e2e", fg="white")
label.pack(pady=20)

folder_label = tk.Label(window, textvariable=selected_folder, font=("Arial", 10), bg="#1e1e2e", fg="#888888")
folder_label.pack(pady=5)

log_area = tk.Text(window, height=10, width=55, state="disabled", bg="#2d2d3f", fg="white", relief="flat")
log_area.pack(pady=10)

def log(msg):
    log_area.config(state="normal")
    log_area.insert(tk.END, msg + "\n")
    log_area.see(tk.END)
    log_area.config(state="disabled")

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        selected_folder.set(folder)

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

def organise():
    folder = selected_folder.get()
    if folder == "No folder selected":
        log("Please choose a folder first!")
        return
    target = Path(folder)
    moved = 0
    for item in target.iterdir():
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
        dest_folder = target / category
        dest_folder.mkdir(exist_ok=True)
        dest_path = resolve_conflict(dest_folder / item.name)
        shutil.move(str(item), str(dest_path))
        log(f"Moved: {item.name} → {category}/")
        moved += 1
    log(f"Done! Moved {moved} files.")

btn_choose = tk.Button(window, text="Choose Folder", width=20, height=2, 
                       bg="#4a4af4", fg="white", relief="flat",
                       activebackground="#3333cc", activeforeground="white")
btn_choose.pack(pady=5)

btn_organise = tk.Button(window, text="Organise Now", width=20, height=2, 
                         bg="#22c55e", fg="white", relief="flat",
                         activebackground="#16a34a", activeforeground="white")
btn_organise.pack(pady=5)

window.mainloop()