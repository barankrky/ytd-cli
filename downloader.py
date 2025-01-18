import os
from tqdm import tqdm
import yt_dlp

def print_video_info(info_dict):
    title = info_dict.get('title', 'Bilinmiyor')
    uploader = info_dict.get('uploader', 'Bilinmiyor')
    height = info_dict.get('height', 'Bilinmiyor')
    filesize = info_dict.get('filesize', info_dict.get('approximate_filesize', 0))

    quality = f"{height}p" if height != 'Bilinmiyor' else "Bilinmiyor"

    print("\n" + "="*50)
    print(f"Video Başlığı: {title}")
    print(f"Yükleyen: {uploader}")
    print(f"Kalite: {quality}")
    print(f"Yaklaşık Boyut: {filesize / (1024*1024):.2f} MB" if filesize > 0 else "Yaklaşık Boyut: Bilinmiyor")
    print("="*50 + "\n")

def download_video(url, output_path, playlist=False):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'logger': None,
    }

    def progress_hook(d):
        if d['status'] == 'downloading':
            pbar.update(d['downloaded_bytes'] - pbar.n)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if playlist:
                playlist_info = ydl.extract_info(url, download=False)
                videos = playlist_info.get('entries', [])
                
                for video in videos:
                    video_url = video['url']
                    info_dict = ydl.extract_info(video_url, download=False)
                    print_video_info(info_dict)

                    print(f"İndiriliyor: {info_dict['title']}")
                    with tqdm(total=info_dict.get('filesize', 0), unit='B', unit_scale=True) as pbar:
                        ydl_opts['progress_hooks'] = [progress_hook]
                        ydl.download([video_url])
                    print("İndirme tamamlandı.")
            else:
                info_dict = ydl.extract_info(url, download=False)
                print_video_info(info_dict)

                print(f"İndiriliyor: {info_dict['title']}")
                with tqdm(total=info_dict.get('filesize', 0), unit='B', unit_scale=True) as pbar:
                    ydl_opts['progress_hooks'] = [progress_hook]
                    ydl.download([url])
                print("İndirme tamamlandı.")

    except Exception as e:
        print(f"Video indirilirken bir hata oluştu: {str(e)}")

def download_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'logger': None,
    }

    def progress_hook(d):
        if d['status'] == 'downloading':
            pbar.update(d['downloaded_bytes'] - pbar.n)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            print_video_info(info_dict)

            print(f"İndiriliyor: {info_dict['title']}")
            with tqdm(total=info_dict.get('filesize', 0), unit='B', unit_scale=True) as pbar:
                ydl_opts['progress_hooks'] = [progress_hook]
                ydl.download([url])
            print("Müzik indirme işlemi tamamlandı.")

    except Exception as e:
        print(f"Müzik indirilirken bir hata oluştu: {str(e)}")