# 📥 Clipster

**Clipster** is a minimalist desktop application that allows users to download videos and audio from YouTube, TikTok, and X. Built with Python and Tkinter, it runs locally, requires no technical knowledge, and is extremely easy to use.  

---

## 🚀 Features
- 📺 Support for **YouTube**, **TikTok**, and **X**
- 🎵 Download in **MP4 (Fast or Compatible)** and **MP3** formats
- 🖱️ Intuitive graphical interface
- 📂 Saves files organized by platform
- 🧩 Compatible with Windows (executable version available)

---

## 📦 Requirements

If you're a developer and want to run the project locally, you'll need:

- Python 3.8+
- Pip
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- `ffmpeg` (already included locally in the project)

### Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🖥️ How to run the application

```bash
python src/main.py
```

Or open the included `Clipster.exe` (compiled version for Windows).

---

## 🔧 How to build the executable

```bash
pyinstaller --onefile --windowed --add-binary "src/ffmpeg/ffmpeg.exe;ffmpeg" src/main.py
```

---

## 📁 Project structure

```
project/
├── src/
│   ├── assets/
│   │   └── icons/
│   │       └── Clipster.ico
│   ├── downloads/
│   │   ├── youtube/
│   │   ├── tiktok/
│   │   └── x/
│   ├── ffmpeg/
│   │   └── ffmpeg.exe
│   ├── downloader.py
│   └── main.py
├── Clipster.exe (optional)
```

---

## ⚖️ License

This project is licensed under the **MIT License**.  
You are free to use, modify, and share the code, but must retain the copyright notice.

🔗 See more in [LICENSE](./LICENSE)

---

## 🤝 Contributions

Pull requests are welcome! Feel free to suggest new features or improvements.

---

## ✨ Created by

**Gustavo** – Systems and Computing Management student 👨‍💻  
