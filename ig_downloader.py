import instaloader
import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
from datetime import datetime

# Initialize Instaloader with the right parameters
loader = instaloader.Instaloader(
    download_pictures=True,  # Download images by default
    download_videos=True,    # Download videos by default
    download_video_thumbnails=True,  # Download video thumbnails (optional)
    save_metadata=False,     # Do not save metadata (including captions)
    download_comments=False  # Do not download comments
)

# Set the post metadata txt pattern to an empty string to avoid creating metadata files
loader.post_metadata_txt_pattern = ''

# Ensure the 'downloads' folder exists
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Function to download posts
def download_posts():
    urls = text_box.get("1.0", tk.END).strip().split("\n")
    if not urls:
        messagebox.showerror("Erro", "Por favor, insira pelo menos uma URL do Instagram.")
        return

    for url in urls:
        try:
            shortcode = url.split("/")[-2]  # Extract shortcode from URL
            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            # Format date in Brazilian style (DD-MM-YYYY_HH-MM-SS)
            post_date = post.date_utc.strftime("%d-%m-%Y_%H-%M-%S")

            # Define the filename pattern: username_date_shortcode
            loader.filename_pattern = f"{post.owner_username}_{post_date}_{shortcode}"

            # Download post into 'downloads' folder
            loader.download_post(post, target=DOWNLOAD_DIR)

            status_label.config(text=f"Baixado: {url}")

        except Exception as e:
            status_label.config(text=f"Falhou: {url} ({e})")

    messagebox.showinfo("Concluído", "Download completo!")

# Function to clear the URL text area
def clear_text():
    text_box.delete("1.0", tk.END)

# GUI setup
root = tk.Tk()
root.title("Instagram Video Downloader")
root.geometry("850x500")
root.config(bg="#f0f0f0")

# Instructions
instruction_label = tk.Label(root, text="Cole as URLs do Instagram (uma por linha):", font=("Arial", 12), bg="#f0f0f0")
instruction_label.pack(pady=10)

# Text box for URLs
text_box = scrolledtext.ScrolledText(root, width=70, height=12, font=("Arial", 12), wrap=tk.WORD, padx=10, pady=10)
text_box.pack(padx=20, pady=10)

# Buttons
download_button = tk.Button(root, text="Baixar", command=download_posts, font=("Arial", 12), bg="#4CAF50", fg="white", width=20, height=2)
download_button.pack(pady=10)

clear_button = tk.Button(root, text="Limpar", command=clear_text, font=("Arial", 12), bg="#f44336", fg="white", width=20, height=2)
clear_button.pack(pady=10)

# Status label
status_label = tk.Label(root, text="", font=("Arial", 12), fg="blue", bg="#f0f0f0")
status_label.pack(pady=10)

# Run GUI
try:
    root.mainloop()
except Exception as e:
    print(f"Erro inesperado: {e}")
    input("Pressione Enter para fechar...")
