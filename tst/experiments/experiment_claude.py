import yt_dlp
import os
from pathlib import Path

class YouTubeDownloader:
    def __init__(self, download_path="./downloads"):
        """
        Initialize the YouTube downloader.
        
        Args:
            download_path (str): Directory where videos will be saved
        """
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        
    def download_video(self, url, quality="best"):
        """
        Download a YouTube video.
        
        Args:
            url (str): YouTube video URL
            quality (str): Video quality preference ("best", "worst", "720p", etc.)
        
        Returns:
            str: Path to downloaded file if successful, None if failed
        """
        try:
            # Configure yt-dlp options
            ydl_opts = {
                'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
                'format': quality,
            }
            
            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                print(f"Successfully downloaded: {info['title']}")
                return filename
                
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return None
    
    def get_video_info(self, url):
        """
        Get information about a YouTube video without downloading.
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            dict: Video information or None if failed
        """
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'view_count': info.get('view_count'),
                    'upload_date': info.get('upload_date')
                }
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    # Create downloader instance
    downloader = YouTubeDownloader("./my_downloads")
    
    # Example YouTube URL (replace with actual URL)
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Get video info first
    info = downloader.get_video_info(video_url)
    print(info)
    if info:
        print(f"Title: {info['title']}")
        print(f"Duration: {info['duration']} seconds")
        print(f"Uploader: {info['uploader']}")
    
    # Download the video
    downloaded_file = downloader.download_video(video_url, quality="best")
    if downloaded_file:
        print(f"Video saved to: {downloaded_file}")