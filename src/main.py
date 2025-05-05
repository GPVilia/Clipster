import customtkinter as ctk
import os
import subprocess
import threading
import sys
from PIL import Image
from customtkinter import CTkImage
from downloader import download_video
from tkinter import messagebox

def resource_path(relative_path):
    """
    Returns the absolute path to a resource, whether in development or in the PyInstaller executable.

    Args:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    if hasattr(sys, '_MEIPASS'):
        # Temporary path used by PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class App(ctk.CTk):
    """
    Main application class for Clipster, responsible for creating the graphical user interface
    and managing user interactions.
    """
    def __init__(self):
        """
        Initializes the graphical user interface and configures the main elements.
        """
        super().__init__()
        ctk.set_appearance_mode("dark")  # Sets the appearance mode (dark, light, system)
        ctk.set_default_color_theme("blue")  # Sets the default color theme

        # Main window configuration
        self.title("Clipster")
        self.geometry("400x458")
        self.iconbitmap(resource_path("assets/Clipster.ico"))
        self.resizable(False, False)

        # Header with logo and title
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(10, 3), padx=20, anchor="w")

        # Application logo
        logo_image = CTkImage(Image.open(resource_path("assets/Clipster_Banner.png")), size=(150, 80))
        ctk.CTkLabel(header_frame, image=logo_image, text="").pack(side="left", padx=(0,0))

        # Input field for video URL
        ctk.CTkLabel(self, text="Video URL:", font=("Poppins", 14, "bold"), anchor="w").pack(pady=(0, 5), padx=20, anchor="w")
        self.url_entry = ctk.CTkEntry(self, width=360, placeholder_text="Enter URL...", font=("Poppins", 12))
        self.url_entry.pack(padx=20)

        # Platform selection with icons
        ctk.CTkLabel(self, text="Platform:", font=("Poppins", 14, "bold"), anchor="w").pack(pady=(10, 5), padx=20, anchor="w")

        # Load platform icons
        self.youtube_icon = CTkImage(Image.open(resource_path("assets/icons/youtube.png")), size=(40, 40))
        self.tiktok_icon = CTkImage(Image.open(resource_path("assets/icons/tiktok.png")), size=(40, 40))
        self.x_icon = CTkImage(Image.open(resource_path("assets/icons/x.png")), size=(40, 40))

        # Buttons for platform selection
        platform_frame = ctk.CTkFrame(self, fg_color="transparent")
        platform_frame.pack(pady=(5, 10), padx=20, anchor="center")  # Center the platform buttons

        # Buttons equally spaced horizontally with custom styles
        ctk.CTkButton(
            platform_frame,
            text="",
            image=self.youtube_icon,
            width=100,
            height=60,
            fg_color="#1c1c1c",  # Darker gray background
            hover_color="#333333",  # Slightly lighter gray for hover
            command=lambda: self.select_platform("YouTube")
        ).pack(side="left", padx=5, fill="x", expand=True)

        ctk.CTkButton(
            platform_frame,
            text="",
            image=self.x_icon,
            width=100,
            height=60,
            fg_color="#1c1c1c",  # Darker gray background
            hover_color="#333333",  # Slightly lighter gray for hover
            command=lambda: self.select_platform("X")
        ).pack(side="left", padx=5, fill="x", expand=True)

        ctk.CTkButton(
            platform_frame,
            text="",
            image=self.tiktok_icon,
            width=100,
            height=60,
            fg_color="#1c1c1c",  # Darker gray background
            hover_color="#333333",  # Slightly lighter gray for hover
            command=lambda: self.select_platform("TikTok")
        ).pack(side="left", padx=5, fill="x", expand=True)

        # Format selection
        ctk.CTkLabel(self, text="Format:", font=("Poppins", 14, "bold"), anchor="w").pack(pady=(10, 5), padx=20, anchor="w")
        formats = ["MP4 (OPUS/VIDEO)", "MP4 (COMPATIBLE)", "MP3"]
        self.formato_combo = ctk.CTkComboBox(self, values=formats, width=360, font=("Poppins", 12))
        self.formato_combo.set("MP4 (OPUS/VIDEO)")
        self.formato_combo.pack(padx=20)

        # Download button
        ctk.CTkButton(self, text="Download", font=("Poppins", 14, "bold"), width=360, height=40, fg_color="#007BFF", hover_color="#0056b3", command=self.start_download).pack(pady=20, padx=20)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self, width=360, height=7, corner_radius=3, progress_color="#007BFF", mode="determinate")
        self.progress_bar.set(0.0)
        self.progress_bar.pack(pady=(0, 0), padx=20)


        # Status label
        self.status_label = ctk.CTkLabel(self, text="", font=("Poppins", 12, "bold"), anchor="w")
        self.status_label.pack(pady=(5, 0), padx=20, anchor="w")

        # Default platform
        self.selected_platform = "YouTube"

    def select_platform(self, platform):
        """
        Updates the selected platform based on user input.

        Args:
            platform (str): The name of the selected platform.
        """
        self.selected_platform = platform
        self.status_label.configure(text=f"Selected Platform: {platform}")

    def start_download(self):
        """
        Starts the download process in a separate thread.
        """
        url = self.url_entry.get()
        platform = self.selected_platform
        format = self.formato_combo.get()

        # Validate user input
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
        """
        Handles the video download process and updates the UI with progress.

        Args:
            url (str): The video URL.
            platform (str): The selected platform.
            format (str): The selected format.
        """
        self.progress_bar.set(0)
        self.status_label.configure(text="Downloading...")
        self.update_idletasks()

        def progress_hook(d):
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 1)
                progress = downloaded / total * 0.8
                self.progress_bar.set(progress)
                self.update_idletasks()

        success, message, file_path = download_video(url, platform, format, progress_hook)
        if not success:
            self.status_label.configure(text="Error")
            messagebox.showerror("Error", message)
            return

        self.status_label.configure(text="Processing File...")
        for i in range(81, 101):
            self.progress_bar.set(i / 100)
            self.update_idletasks()
            self.after(100)

        self.progress_bar.set(1)
        self.status_label.configure(text="Done")
        self.url_entry.delete(0, 'end')

        if success and file_path:
            if messagebox.askyesno("Success", f"Download completed!\n\nFile saved at:\n{file_path}\n\nDo you want to open the folder?"):
                self.open_folder(file_path)

    def open_folder(self, file_path):
        """
        Opens the folder where the downloaded file is saved.

        Args:
            file_path (str): The path to the saved file.
        """
        folder_path = os.path.dirname(file_path)
        subprocess.Popen(f'explorer "{folder_path}"')

if __name__ == "__main__":
    app = App()
    app.mainloop()






