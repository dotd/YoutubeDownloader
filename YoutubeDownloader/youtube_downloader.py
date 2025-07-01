#!/usr/bin/env python3
"""
YouTube Downloader - Download multiple YouTube videos in specific formats
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
import yt_dlp
from tqdm import tqdm
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class YouTubeDownloader:
    def __init__(self, output_dir: str = "downloads", format_preference: str = "best"):
        """
        Initialize the YouTube downloader
        
        Args:
            output_dir: Directory to save downloaded videos
            format_preference: Preferred format (best, worst, mp4, webm, etc.)
        """
        self.output_dir = Path(output_dir)
        self.format_preference = format_preference
        self.output_dir.mkdir(exist_ok=True)
        
        # Common format options
        self.format_options = {
            "best": "bestvideo+bestaudio/best",
            "worst": "worstvideo+worstaudio/worst",
            "mp4": "best[ext=mp4]/best",
            "webm": "best[ext=webm]/best",
            "720p": "best[height<=720]/best",
            "1080p": "best[height<=1080]/best",
            "audio_only": "bestaudio[ext=m4a]/bestaudio",
            "audio_mp3": "bestaudio[ext=mp3]/bestaudio",
        }
    
    def get_available_formats(self, url: str) -> List[Dict]:
        """Get available formats for a YouTube video"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get('formats', [])
        except Exception as e:
            print(f"{Fore.RED}Error getting formats for {url}: {e}{Style.RESET_ALL}")
            return []
    
    def list_formats(self, url: str):
        """List all available formats for a video"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                print(f"\n{Fore.CYAN}Available formats for: {url}{Style.RESET_ALL}")
                print("-" * 60)
                
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        height = f.get('height', 'N/A')
                        ext = f.get('ext', 'N/A')
                        filesize = f.get('filesize', 'N/A')
                        if filesize != 'N/A':
                            filesize = f"{filesize / (1024*1024):.1f}MB"
                        print(f"  {f['format_id']} | {height}p | {ext} | {filesize}")
        except Exception as e:
            print(f"{Fore.RED}Error getting formats: {e}{Style.RESET_ALL}")
    
    def download_video(self, url: str, format_id: Optional[str] = None) -> bool:
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
                'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'ignoreerrors': False,
                'no_warnings': False,
                'extractaudio': False,
                'audioformat': 'mp3',
                'audioquality': '0',
                'writethumbnail': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'embed_subs': True,
            }
            
            print(f"\n{Fore.GREEN}Downloading: {url}{Style.RESET_ALL}")
            print(f"Format: {format_spec}")
            print(f"Output directory: {self.output_dir}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"{Fore.GREEN}✓ Download completed successfully!{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}✗ Download failed: {e}{Style.RESET_ALL}")
            return False
    
    def download_multiple(self, urls: List[str], format_id: Optional[str] = None) -> Dict[str, bool]:
        """
        Download multiple videos
        
        Args:
            urls: List of YouTube URLs
            format_id: Specific format ID to download (optional)
        
        Returns:
            Dict mapping URLs to success status
        """
        results = {}
        
        print(f"{Fore.CYAN}Starting batch download of {len(urls)} videos...{Style.RESET_ALL}")
        print(f"Output directory: {self.output_dir}")
        print(f"Format preference: {self.format_preference}")
        
        for i, url in enumerate(urls, 1):
            print(f"\n{Fore.YELLOW}[{i}/{len(urls)}] Processing: {url}{Style.RESET_ALL}")
            results[url] = self.download_video(url, format_id)
        
        # Summary
        successful = sum(results.values())
        failed = len(results) - successful
        
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}DOWNLOAD SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"Total videos: {len(urls)}")
        print(f"{Fore.GREEN}Successful: {successful}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {failed}{Style.RESET_ALL}")
        
        if failed > 0:
            print(f"\n{Fore.RED}Failed downloads:{Style.RESET_ALL}")
            for url, success in results.items():
                if not success:
                    print(f"  - {url}")
        
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

def load_urls_from_file(filename: str) -> List[str]:
    """Load URLs from a text file (one URL per line)"""
    try:
        with open(filename, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return urls
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{filename}' not found{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED}Error reading file '{filename}': {e}{Style.RESET_ALL}")
        return []

def save_urls_to_file(filename: str, urls: List[str]):
    """Save URLs to a text file"""
    try:
        with open(filename, 'w') as f:
            for url in urls:
                f.write(f"{url}\n")
        print(f"{Fore.GREEN}URLs saved to {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error saving URLs to {filename}: {e}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos in specific formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download a single video in best quality
  python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  
  # Download multiple videos in MP4 format
  python youtube_downloader.py -f mp4 url1 url2 url3
  
  # Download videos from a file
  python youtube_downloader.py -i urls.txt -f 720p
  
  # List available formats for a video
  python youtube_downloader.py -l "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  
  # Download with specific format ID
  python youtube_downloader.py --format-id 22 "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        """
    )
    
    parser.add_argument('urls', nargs='*', help='YouTube URLs to download')
    parser.add_argument('-i', '--input-file', help='File containing URLs (one per line)')
    parser.add_argument('-o', '--output-dir', default='downloads', help='Output directory (default: downloads)')
    parser.add_argument('-f', '--format', default='best', 
                       choices=['best', 'worst', 'mp4', 'webm', '720p', '1080p', 'audio_only', 'audio_mp3'],
                       help='Preferred format (default: best)')
    parser.add_argument('--format-id', help='Specific format ID to download')
    parser.add_argument('-l', '--list-formats', action='store_true', help='List available formats for URLs')
    parser.add_argument('--save-urls', help='Save URLs to a file')
    
    args = parser.parse_args()
    
    # Collect URLs
    urls = []
    if args.input_file:
        urls.extend(load_urls_from_file(args.input_file))
    if args.urls:
        urls.extend(args.urls)
    
    if not urls:
        print(f"{Fore.RED}Error: No URLs provided. Use -i/--input-file or provide URLs as arguments.{Style.RESET_ALL}")
        parser.print_help()
        sys.exit(1)
    
    # Save URLs if requested
    if args.save_urls:
        save_urls_to_file(args.save_urls, urls)
    
    # Create downloader
    downloader = YouTubeDownloader(args.output_dir, args.format)
    
    # List formats if requested
    if args.list_formats:
        for url in urls:
            downloader.list_formats(url)
        return
    
    # Download videos
    downloader.download_multiple(urls, args.format_id)


def download_urls(urls):
    
    # Create downloader instance
    downloader = YouTubeDownloader(
        output_dir="my_downloads",
        format_preference="720p"  # Download in 720p quality
    )
    
    # List available formats for first video
    print("Listing available formats for first video:")
    downloader.list_formats(urls[0])
    
    # Download all videos
    print("\nStarting downloads...")
    results = downloader.download_multiple(urls)
    
    # Print results
    print("\nDownload Results:")
    for url, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        print(f"{url}: {status}")

if __name__ == "__main__":
    main() 