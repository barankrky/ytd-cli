import argparse, pyperclip
from downloader import download_video, download_audio
from utils import validate_url, validate_output_path, get_download_path
from ffmpeg_utils import check_ffmpeg, install_ffmpeg

def main():
    parser = argparse.ArgumentParser(description="ytd-cli - Youtube Downloader CLI")
    parser.add_argument('--output_path', default=get_download_path(), help="İndirme için dosya yolu (varsayılan: İndirilenler klasörü)")
    parser.add_argument('--audio', '-a', action='store_true', help="Müzik indirmek için bu seçeneği kullanın")
    parser.add_argument('--playlist', '-p', action='store_true', help="Tüm oynatma listesini indirmek için bu seçeneği kullanın")
    parser.add_argument('--url', '-u', help="İndirmek istediğiniz YouTube videosunun URL'si")
    
    args = parser.parse_args()
    url = args.url if args.url else pyperclip.paste()
    
    try:
        validate_url(url)
        validate_output_path(args.output_path)

        if args.playlist:
            download_video(url, args.output_path, playlist=True)
        else:
            download_audio(url, args.output_path) if args.audio else download_video(url, args.output_path)

    except ValueError as ve:
        print(f"Hata: {ve}")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    if not check_ffmpeg():
        install_ffmpeg()
    main()