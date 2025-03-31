# 📷 Instagram Bulk Image Downloader

A powerful, GUI-based Python application to **download, crop, convert, and compress images from Instagram** posts in bulk.

---

## 🔧 Features

✅ **Download Images** from public Instagram post URLs  
✅ Automatically fetch **first image** from single or carousel posts  
✅ Save images in **numbered format (1.jpg, 2.jpg...)**  
✅ Organize files into 3 folders:
- `Original/` – Unedited full images
- `Crop/` – Center-cropped (1:1) images
- `Convert/` – Compressed `.webp` images  

✅ Live terminal-style progress display  
✅ Export useful logs:
- `not_downloaded.txt` – Failed post URLs
- `image_export_urls.txt` – Successfully processed IG post URLs  
✅ Set:
- Custom export folder name
- Output file format (`webp` default)
- Crop ratio (currently 1:1)
- Compression level (default 50%)
- Save location via file browser  

---

## 🖥️ How to Use

### 1. Install Requirements

```bash
pip install instaloader pillow requests

![GUI Preview]([https://i.imgur.com/yourImageID.png](https://github.com/NeranjanMe/instagram-bulk-image-downloader/blob/main/Screenshot.png))
