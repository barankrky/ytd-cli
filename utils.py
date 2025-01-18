import os
import re
import winreg
import sys

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def validate_url(url):
    youtube_video_regex = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})(&list=[a-zA-Z0-9_-]+)?(&start_radio=\d+)?$'
    )
    youtube_playlist_regex = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com/playlist\?list=|youtu\.be/playlist\?list=)([a-zA-Z0-9_-]+)$'
    )
    
    if not (youtube_video_regex.match(url) or youtube_playlist_regex.match(url)):
        raise ValueError("Geçersiz URL. Lütfen geçerli bir YouTube video veya oynatma listesi URL'si girin.")

def validate_output_path(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"{output_path} dizini oluşturuldu.")

def get_download_path():
    if os.name == 'nt':
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

def restart_program():
    if sys.argv[0].endswith('.py'):
        python = sys.executable
        os.execl(python, python, *sys.argv)
    elif sys.argv[0].endswith('.exe'):
        os.startfile(sys.argv[0])
