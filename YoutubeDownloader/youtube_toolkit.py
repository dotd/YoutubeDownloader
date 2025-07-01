#!/usr/bin/env python3
"""
YouTube Toolkit - Complete solution for extracting channel URLs and downloading videos
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List
from colorama import init, Fore, Style

# Import our modules
from channel_extractor import YouTubeChannelExtractor
from YoutubeDownloader.youtube_downloader import YouTubeDownloader

# Initialize colorama
init(autoreset=True)

class YouTubeToolkit:
    def __init__(self, output_dir: str = "youtube_content"):
        """
        Initialize the YouTube toolkit
        
        Args:
            output_dir: Base directory for all operations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.urls_dir = self.output_dir / "extracted_urls"
        self.downloads_dir = self.output_dir / "downloads"
        self.urls_dir.mkdir(exist_ok=True)
        self.downloads_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.extractor = YouTubeChannelExtractor(str(self.urls_dir))
        self.downloader = YouTubeDownloader(str(self.downloads_dir))
    
    def extract_and_download(self, channels: List[str], format_preference: str = "720p", 
                           max_videos: int = None, download: bool = True):
        """
        Extract URLs from channels and optionally download videos
        
        Args:
            channels: List of channel URLs
            format_preference: Video format preference
            max_videos: Maximum videos per channel
            download: Whether to download videos after extraction
        """
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}YouTube Toolkit - Extract & Download{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        # Step 1: Extract URLs
        print(f"\n{Fore.YELLOW}Step 1: Extracting URLs from {len(channels)} channels...{Style.RESET_ALL}")
        results = self.extractor.extract_multiple_channels(channels, max_videos)
        
        if not results:
            print(f"{Fore.RED}No URLs extracted. Exiting.{Style.RESET_ALL}")
            return
        
        # Combine all URLs
        all_urls = []
        for urls in results.values():
            all_urls.extend(urls)
        
        # Save URLs
        urls_file = "extracted_urls.txt"
        self.extractor.save_urls_to_file(all_urls, urls_file)
        
        print(f"\n{Fore.GREEN}✓ Extracted {len(all_urls)} video URLs{Style.RESET_ALL}")
        
        # Step 2: Download videos (if requested)
        if download and all_urls:
            print(f"\n{Fore.YELLOW}Step 2: Downloading {len(all_urls)} videos...{Style.RESET_ALL}")
            
            # Update downloader format preference
            self.downloader.format_preference = format_preference
            
            # Download videos
            download_results = self.downloader.download_multiple(all_urls)
            
            successful = sum(download_results.values())
            print(f"\n{Fore.GREEN}Download Summary: {successful}/{len(all_urls)} videos downloaded successfully{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Files saved:{Style.RESET_ALL}")
        print(f"- URLs: {self.urls_dir / urls_file}")
        print(f"- Downloads: {self.downloads_dir}")
    
    def extract_only(self, channels: List[str], max_videos: int = None, 
                    output_file: str = "channel_urls.txt"):
        """Extract URLs only, without downloading"""
        print(f"{Fore.CYAN}Extracting URLs from {len(channels)} channels...{Style.RESET_ALL}")
        
        results = self.extractor.extract_multiple_channels(channels, max_videos)
        
        if results:
            all_urls = []
            for urls in results.values():
                all_urls.extend(urls)
            
            self.extractor.save_urls_to_file(all_urls, output_file)
            print(f"\n{Fore.GREEN}✓ Ready to download with:{Style.RESET_ALL}")
            print(f"python youtube_downloader.py -i {output_file} -f 720p")
    
    def download_only(self, urls_file: str, format_preference: str = "720p"):
        """Download videos from a URL file"""
        print(f"{Fore.CYAN}Downloading videos from {urls_file}...{Style.RESET_ALL}")
        
        # Load URLs
        try:
            with open(urls_file, 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(f"{Fore.RED}Error: File '{urls_file}' not found{Style.RESET_ALL}")
            return
        
        if not urls:
            print(f"{Fore.RED}No URLs found in file{Style.RESET_ALL}")
            return
        
        # Update downloader format preference
        self.downloader.format_preference = format_preference
        
        # Download videos
        results = self.downloader.download_multiple(urls)
        
        successful = sum(results.values())
        print(f"\n{Fore.GREEN}Download Summary: {successful}/{len(urls)} videos downloaded successfully{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Toolkit - Extract channel URLs and download videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract and download from channels
  python youtube_toolkit.py -c "https://www.youtube.com/@example" -f 720p
  
  # Extract only (no download)
  python youtube_toolkit.py -c "https://www.youtube.com/@example" --extract-only
  
  # Download only from URL file
  python youtube_toolkit.py --download-only urls.txt -f mp4
  
  # Extract from multiple channels with limit
  python youtube_toolkit.py -i channels.txt -m 10 -f 1080p
  
  # Extract from channels and save URLs
  python youtube_toolkit.py -c "https://www.youtube.com/@example" --extract-only -o my_urls.txt
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-c', '--channels', nargs='+', help='Channel URLs to process')
    input_group.add_argument('-i', '--input-file', help='File containing channel URLs')
    input_group.add_argument('--download-only', help='Download only from URL file')
    
    # Operation options
    parser.add_argument('--extract-only', action='store_true', help='Extract URLs only, no download')
    parser.add_argument('-m', '--max-videos', type=int, help='Maximum videos per channel')
    parser.add_argument('-f', '--format', default='720p', 
                       choices=['best', 'worst', 'mp4', 'webm', '720p', '1080p', 'audio_only', 'audio_mp3'],
                       help='Video format preference')
    parser.add_argument('-o', '--output-file', help='Output file for extracted URLs')
    parser.add_argument('-d', '--output-dir', default='youtube_content', help='Base output directory')
    
    args = parser.parse_args()
    
    # Create toolkit
    toolkit = YouTubeToolkit(args.output_dir)
    
    # Handle different modes
    if args.download_only:
        # Download only mode
        toolkit.download_only(args.download_only, args.format)
    
    else:
        # Extract mode (with or without download)
        channels = []
        if args.channels:
            channels = args.channels
        elif args.input_file:
            try:
                with open(args.input_file, 'r') as f:
                    channels = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            except FileNotFoundError:
                print(f"{Fore.RED}Error: File '{args.input_file}' not found{Style.RESET_ALL}")
                sys.exit(1)
        
        if not channels:
            print(f"{Fore.RED}Error: No channels provided{Style.RESET_ALL}")
            sys.exit(1)
        
        if args.extract_only:
            # Extract only
            output_file = args.output_file or "channel_urls.txt"
            toolkit.extract_only(channels, args.max_videos, output_file)
        else:
            # Extract and download
            toolkit.extract_and_download(channels, args.format, args.max_videos, download=True)

if __name__ == "__main__":
    main() 