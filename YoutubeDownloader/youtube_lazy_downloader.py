import os
import yt_dlp
from tqdm import tqdm
from colorama import init, Fore, Style

from urllib.parse import urlparse
from YoutubeDownloader.definitions import PROJECT_ROOT_DIR

class YoutubeLazyDownloader:
    def __init__(
            self, 
            downloads_folder=f"{PROJECT_ROOT_DIR}/downloads", 
            format_preference="720p",
        ):
        self.downloads_folder = downloads_folder
        self.format_preference = format_preference
        os.makedirs(self.downloads_folder, exist_ok=True)
        # Get all file names in the downloads folder that start with "youtube_"
        self.downloaded_files = [f for f in os.listdir(self.downloads_folder) if f.startswith("youtube_")]
        self.videoids = [f.split(".")[0].split("VIDEOID")[-1] for f in self.downloaded_files]

    def get_video_id(self, url):
        parsed_url = urlparse(url)
        try:
            v = parsed_url.query.split("=")[1]
            return v
        except:
            # print(f"Error parsing url: {url}")
            return None

    def get_formats(self, url: str):
        """List all available formats for a video"""
        results = list()
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        height = f.get('height', 'N/A')
                        ext = f.get('ext', 'N/A')
                        filesize = f.get('filesize', 'N/A')
                        if filesize != 'N/A':
                            filesize = f"{filesize / (1024*1024):.1f}MB"
                        results.append({
                            "format_id": f['format_id'],
                            "height": height,
                            "ext": ext,
                            "filesize": filesize
                        })

        except Exception as e:
            print(f"{Fore.RED}Error getting formats: {e}{Style.RESET_ALL}")

        return results

    def _progress_hook(self, d):
        """Progress hook for download progress"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                speed = d.get('speed', 0)
                if speed:
                    speed_mb = speed / (1024*1024)
                    print(f"\r{Fore.BLUE}Downloading: {percent:.1f}% | Speed: {speed_mb:.1f} MB/s{Style.RESET_ALL}", end='', flush=True)
            else:
                print(f"\r{Fore.BLUE}Downloading...{Style.RESET_ALL}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n{Fore.GREEN}Download finished, processing...{Style.RESET_ALL}")


    def download_video(self, url, format_id, video_id):
        """
        Download a single video
        
        Args:
            url: YouTube URL
            format_id: Specific format ID to download (optional)
        
        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            # Configure yt-dlp options
            format_spec = format_id if format_id else self.format_options.get(
                self.format_preference, self.format_options["best"]
            )
            
            ydl_opts = {
                'format': format_spec,
                'outtmpl': f"{self.downloads_folder}/youtube_%(title)s_VIDEOID{video_id}.%(ext)s",
                'progress_hooks': [self._progress_hook],
                'ignoreerrors': False,
                'no_warnings': False,
                'extractaudio': False,
                'audioformat': 'mp3',
                'audioquality': '0',
                'writethumbnail': False,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'embed_subs': True,
            }
            
            print(f"\n{Fore.GREEN}Downloading: {url}{Style.RESET_ALL}")
            print(f"Format: {format_spec}")
            print(f"Output directory: {self.downloads_folder}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"{Fore.GREEN}✓ Download completed successfully!{Style.RESET_ALL}")
            return True

        except Exception as e:
            print(f"{Fore.RED}✗ Download failed: {e}{Style.RESET_ALL}")
            return False


    def download_url(self, url):
        # process url completely
        video_id = self.get_video_id(url)
        if video_id in self.videoids:
            print(f"Video {video_id} already downloaded")
            return
        print(f"Downloading video {video_id}")
        formats = self.get_formats(url)
        print(f"Available formats: {formats}")
        # if format_preference is not in formats, then use the best format
        if self.format_preference not in [f["height"] for f in formats]:
            self.format_preference = formats[0]["format_id"]
        # download video
        self.download_video(url=url, format_id=self.format_preference,video_id=video_id)
        # add video_id to downloaded_files
        self.downloaded_files.append(video_id)


if __name__ == "__main__":
    youtube_lazy_downloader = YoutubeLazyDownloader()
    youtube_lazy_downloader.download_url("https://www.youtube.com/watch?v=yfDduYQj_Wc")
