import customtkinter as ctk
import os
import subprocess
import threading
from PIL import Image  # Importar Pillow para carregar imagens
from customtkinter import CTkImage
from downloader import download_video
from tkinter import messagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")  # Modes: "dark", "light", "system"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

        self.title("Clipster")
        self.geometry("450x400")
        self.iconbitmap("./assets/Clipster.ico")
        self.resizable(False, False)

        # Video URL input
        ctk.CTkLabel(self, text="Video URL:", font=("Arial", 14)).pack(pady=(20, 5))
        self.url_entry = ctk.CTkEntry(self, width=300)
        self.url_entry.pack()

        # Platform selection with icons
        ctk.CTkLabel(self, text="Platform:", font=("Arial", 14)).pack(pady=(10, 5))

        # Load icons using Pillow and CTkImage
        self.youtube_icon = CTkImage(Image.open("./assets/icons/youtube.png"), size=(30, 30))
        self.tiktok_icon = CTkImage(Image.open("./assets/icons/tiktok.png"), size=(30, 30))
        self.x_icon = CTkImage(Image.open("./assets/icons/x.png"), size=(30, 30))

        # Create a frame for platform buttons
        platform_frame = ctk.CTkFrame(self)
        platform_frame.pack(pady=(5, 10))

        # Add buttons with icons
        ctk.CTkButton(platform_frame, text="YouTube", image=self.youtube_icon, compound="left", command=lambda: self.select_platform("YouTube")).pack(side="left", padx=5)
        ctk.CTkButton(platform_frame, text="TikTok", image=self.tiktok_icon, compound="left", command=lambda: self.select_platform("TikTok")).pack(side="left", padx=5)
        ctk.CTkButton(platform_frame, text="X", image=self.x_icon, compound="left", command=lambda: self.select_platform("X")).pack(side="left", padx=5)

        # Format selection
        ctk.CTkLabel(self, text="Format:", font=("Arial", 14)).pack(pady=(10, 5))
        formats = ["MP4 (OPUS/VIDEO)", "MP4 (COMPATIBLE)", "MP3"]
        self.formato_combo = ctk.CTkComboBox(self, values=formats)
        self.formato_combo.set("MP4 (OPUS/VIDEO)")
        self.formato_combo.pack()

        # Download button
        ctk.CTkButton(self, text="Download", command=self.start_download).pack(pady=20)

        # Status label
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=(5, 0))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self, width=300)
        self.progress_bar.pack(pady=(10, 0))
        self.progress_bar.set(0.0)  # Certifique-se de que o valor inicial seja 0.0

        self.selected_platform = "YouTube"  # Default platform

    def select_platform(self, platform):
        self.selected_platform = platform
        self.status_label.configure(text=f"Selected Platform: {platform}")

    def start_download(self):
        url = self.url_entry.get()
        platform = self.selected_platform
        format = self.formato_combo.get()

        # Validate URL
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return
        if platform not in ["YouTube", "TikTok", "X"]:
            messagebox.showerror("Error", "Please select a valid platform.")
            return
        if format not in ["MP4 (OPUS/VIDEO)", "MP4 (COMPATIBLE)", "MP3"]:
            messagebox.showerror("Error", "Please select a valid format.")
            return

        # Start the download in a separate thread
        threading.Thread(target=self.download_thread, args=(url, platform, format), daemon=True).start()

    def download_thread(self, url, platform, format):
        # Reset progress bar and update status
        self.progress_bar.set(0)
        self.status_label.configure(text="Downloading...")
        self.update_idletasks()

        # Define the progress hook
        def progress_hook(d):
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 1)
                progress = downloaded / total * 0.8  # 80% do progresso para o download
                self.progress_bar.set(progress)
                self.update_idletasks()

        # Call the downloader with a progress hook
        success, message, file_path = download_video(url, platform, format, progress_hook)
        if not success:
            self.status_label.configure(text="Error")
            messagebox.showerror("Error", message)
            return

        # Simulate processing progress (20% restante)
        self.status_label.configure(text="Processing File...")
        for i in range(81, 101):  # De 80% a 100%
            self.progress_bar.set(i / 100)
            self.update_idletasks()
            self.after(100)  # Simula o tempo de processamento

        # Show completion message
        self.progress_bar.set(1)
        self.status_label.configure(text="Done")
        self.update_idletasks()

        # Clear the URL entry field
        self.url_entry.delete(0, 'end')

        if success and file_path:
            if messagebox.askyesno("Success", f"Download completed!\n\nFile saved at:\n{file_path}\n\nDo you want to open the folder?"):
                self.open_folder(file_path)

    def open_folder(self, file_path):
        folder_path = os.path.dirname(file_path)
        subprocess.Popen(f'explorer "{folder_path}"')

if __name__ == "__main__":
    app = App()
    app.mainloop()






