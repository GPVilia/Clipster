<p align="center">
  <img src="https://github.com/GPVilia/Clipster/blob/main/src/assets/Clipster_Banner.png?raw=true" alt="Clipster Logo" width="500"/>
</p>

**Clipster** is a minimalist and user-friendly desktop application to download videos and audio from YouTube, TikTok, and X (formerly Twitter). Built with Python and a modern graphical interface, Clipster is designed for simplicity, speed, and offline use — no Python installation required for end users.

---

## 🚀 Features

- 📥 Download from **YouTube**, **TikTok**, and **X**
- 🎧 Choose between **MP4 (Fast)**, **MP4 (Compatible)** or **MP3**
- 📂 Files organized in platform-specific folders
- 🖼️ Clean and responsive interface with icons
- ⚙️ Works completely **offline** once built
- 🧾 No terminal or Python knowledge required to use the `.exe`

---

## 🖼️ Preview

<details>
<summary>Click to see the Clipster interface</summary>

<br/>

<p align="center">
  <img src="https://github.com/GPVilia/Clipster/blob/main/src/assets/preview/Preview.png?raw=true" alt="Clipster UI Preview" width="600"/>
</p>

</details>

---

## 📦 Requirements for Developers

To run or modify the project locally:

- Python 3.8+
- pip
- `yt-dlp`
- `customtkinter`
- `Pillow`
- `ffmpeg` (must be downloaded separately)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🧪 Run Locally

```bash
python src/main.py
```

Make sure `ffmpeg.exe` is placed in:

```
src/ffmpeg/ffmpeg.exe
```

---

## 🔧 Build the Executable

You can build the `.exe` using PyInstaller:

```bash
pyinstaller --noconfirm --onefile --windowed --icon="src/assets/Clipster.ico" --add-data "src/assets/Clipster.ico;assets" --add-binary "src/ffmpeg/ffmpeg.exe;ffmpeg" src/main.py
```

Output is saved to the `dist/` folder. Rename `main.exe` to `Clipster.exe`.

---

## 📁 Project Structure

```
src/
├── assets/
│   ├── icons/
│   │   └── *.png
│   └── Clipster.ico
├── downloads/
│   ├── youtube/
│   ├── tiktok/
│   └── x/
├── ffmpeg/
│   └── ffmpeg.exe
├── downloader.py
└── main.py
```

---

## 📜 License

This project is licensed under the MIT License.  
Feel free to use, modify, and distribute with attribution.

---

## ✨ Author

**Gustavo V.** – Student of Systems and Computing Management @ UATLA 👨‍💻  
Follow or contribute at: [https://github.com/GPVilia/Clipster](https://github.com/GPVilia/Clipster)
