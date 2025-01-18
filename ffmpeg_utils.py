import os, platform, subprocess, requests, zipfile, tempfile
from tqdm import tqdm
from utils import clear_console


def check_ffmpeg():
    clear_console()
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def install_ffmpeg():
    clear_console()
    if platform.system() == "Windows":
        url = "https://github.com/barankrky/ytd-cli/raw/refs/heads/master/ffmpeg.zip"
        output_path = os.path.join(tempfile.gettempdir(), "ffmpeg.zip")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_length = int(response.headers.get('content-length', 0))
            with open(output_path, 'wb') as f:
                with tqdm(total=total_length, unit='B', unit_scale=True, desc="İndiriliyor") as pbar:
                    for data in response.iter_content(chunk_size=4096):
                        f.write(data)
                        pbar.update(len(data))
            print("\nİndirme tamamlandı.")

            with zipfile.ZipFile(output_path, 'r') as zip_ref:
                zip_ref.extractall("C:\\Program Files")

            ffmpeg_path = "C:\\Program Files\\ffmpeg\\bin"
            os.system(f'setx PATH "%PATH%;{ffmpeg_path}"')


        except requests.exceptions.RequestException as e:
            print(f"İndirme sırasında bir hata oluştu: {e}")