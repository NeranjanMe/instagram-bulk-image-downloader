import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import re
import requests
from PIL import Image
import instaloader

# Helper Functions
def extract_shortcode(url):
    match = re.search(r"instagram\.com/p/([A-Za-z0-9_-]+)/?", url)
    return match.group(1) if match else None

def crop_center_square(img):
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    return img.crop((left, top, right, bottom))

def process_links():
    output_console.delete("1.0", tk.END)

    folder_name_raw = folder_name_entry.get().strip()
    folder_name = folder_name_raw.title()  # Convert to Proper Case
    links_text = links_textbox.get("1.0", tk.END).strip()
    convert_format = format_var.get().lower()
    compress_quality = int(compress_scale.get())
    crop_ratio = crop_ratio_var.get()
    save_path = save_dir.get().strip()

    if not folder_name or not links_text or not save_path:
        messagebox.showerror("Missing Info", "Please fill all required fields.")
        return

    export_base = os.path.join(save_path, folder_name)
    folders = {
        "original": os.path.join(export_base, "Original"),
        "crop": os.path.join(export_base, "Crop"),
        "convert": os.path.join(export_base, "Convert"),
    }
    for path in folders.values():
        os.makedirs(path, exist_ok=True)

    loader = instaloader.Instaloader(
        download_video_thumbnails=False,
        download_comments=False,
        save_metadata=False,
        post_metadata_txt_pattern="",
        dirname_pattern=folders["original"]
    )

    links = [line.strip() for line in links_text.splitlines() if line.strip()]
    not_downloaded = []
    export_urls = []
    count = 1

    for link in links:
        shortcode = extract_shortcode(link)
        if not shortcode:
            not_downloaded.append(link)
            output_console.insert(tk.END, f"[{count}] ❌ Invalid link: {link}\n")
            continue

        try:
            output_console.insert(tk.END, f"[{count}] 🔽 Downloading: {shortcode}\n")
            output_console.see(tk.END)
            output_console.update_idletasks()
            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            if post.typename == "GraphSidecar":
                first_image_url = list(post.get_sidecar_nodes())[0].display_url
            else:
                first_image_url = post.url

            export_urls.append(link)  # Add original IG post link, not the image CDN

            response = requests.get(first_image_url)
            response.raise_for_status()
            original_path = os.path.join(folders["original"], f"{count}.jpg")
            with open(original_path, "wb") as f:
                f.write(response.content)
            output_console.insert(tk.END, f"[{count}] ✅ Original saved as {original_path}\n")

            with Image.open(original_path) as img:
                cropped = crop_center_square(img)
                crop_path = os.path.join(folders["crop"], f"{count}.jpg")
                cropped.save(crop_path)
                output_console.insert(tk.END, f"[{count}] 📐 Cropped saved as {crop_path}\n")

                convert_path = os.path.join(folders["convert"], f"{count}.{convert_format}")
                cropped.save(convert_path, convert_format.upper(), quality=compress_quality)
                output_console.insert(tk.END, f"[{count}] 🗜️ Compressed saved as {convert_path}\n")

            count += 1

        except Exception as e:
            not_downloaded.append(link)
            output_console.insert(tk.END, f"[{count}] ❌ Failed to download {shortcode}: {e}\n")

    if not_downloaded:
        with open(os.path.join(export_base, "not_downloaded.txt"), "w") as f:
            f.write("\n".join(not_downloaded))
        output_console.insert(tk.END, f"📄 Exported not downloaded links.\n")

    if export_urls:
        with open(os.path.join(export_base, "image_export_urls.txt"), "w") as f:
            f.write("\n".join(export_urls))
        output_console.insert(tk.END, f"🌐 Exported image IG URLs list.\n")

    messagebox.showinfo("Done", "Process completed successfully.")

# GUI Setup
root = tk.Tk()
root.title("Instagram Bulk Image Downloader")

tk.Label(root, text="Export Folder Name:").grid(row=0, column=0, sticky="e")
folder_name_entry = tk.Entry(root, width=40)
folder_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Instagram Post Links:").grid(row=1, column=0, sticky="ne")
links_textbox = tk.Text(root, width=50, height=10)
links_textbox.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="File Format:").grid(row=2, column=0, sticky="e")
format_var = tk.StringVar(value="webp")
format_entry = tk.Entry(root, textvariable=format_var, width=10)
format_entry.grid(row=2, column=1, sticky="w", padx=5)

tk.Label(root, text="Crop Ratio:").grid(row=3, column=0, sticky="e")
crop_ratio_var = tk.StringVar(value="1:1")
crop_menu = ttk.Combobox(root, textvariable=crop_ratio_var, values=["1:1"], state="readonly", width=10)
crop_menu.grid(row=3, column=1, sticky="w", padx=5)

tk.Label(root, text="Compress Quality (%):").grid(row=4, column=0, sticky="e")
compress_scale = tk.Scale(root, from_=10, to=100, orient="horizontal")
compress_scale.set(50)
compress_scale.grid(row=4, column=1, sticky="w", padx=5)

tk.Label(root, text="Saving Directory:").grid(row=5, column=0, sticky="e")
save_dir = tk.StringVar()
save_entry = tk.Entry(root, textvariable=save_dir, width=30)
save_entry.grid(row=5, column=1, sticky="w", padx=5)
tk.Button(root, text="Browse", command=lambda: save_dir.set(filedialog.askdirectory())).grid(row=5, column=1, sticky="e")

tk.Button(root, text="Start Download", command=process_links, bg="#4CAF50", fg="white").grid(row=6, column=0, columnspan=2, pady=10)

output_console = tk.Text(root, width=75, height=20, bg="black", fg="lime", font=("Courier", 9))
output_console.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
