import os
import sys
import yt_dlp

def download_video(url: str, platform: str, format: str, progress_hook=None):
    base_dir = os.path.join("downloads", platform.lower())

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Define o nome do arquivo com base na plataforma e no formato
    if platform == "TikTok":
        if format == "MP3":
            filename_template = "TikTok_Sound.%(ext)s"
        else:
            filename_template = "TikTok_Video.%(ext)s"
    elif platform == "X":
        if format == "MP3":
            filename_template = "X_Sound.%(ext)s"
        else:
            filename_template = "X_Video.%(ext)s"
    else:
        filename_template = "%(title)s.%(ext)s"  # Nome padrão para outras plataformas

    options = {
        'outtmpl': os.path.join(base_dir, filename_template),
        'ffmpeg_location': os.path.join(sys._MEIPASS, 'ffmpeg') if hasattr(sys, '_MEIPASS') else os.path.abspath('./ffmpeg'),
        'quiet': True,
        'progress_hooks': [progress_hook] if progress_hook else [],
    }

    # Configurações específicas para cada formato
    if format == "MP3":
        options.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif format == "MP4 (OPUS/VIDEO)":
        options.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        })
    elif format == "MP4 (COMPATIBLE)":
        options.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoRemuxer',
                'preferedformat': 'mp4',
            }],
            'postprocessor_args': [
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-strict', 'experimental'
            ],
        })

    # Download do vídeo
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        return True, "Download completed successfully.", file_path
    except Exception as e:
        return False, f"An error occurred: {str(e)}", None
