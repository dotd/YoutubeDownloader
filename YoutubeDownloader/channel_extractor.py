#!/usr/bin/env python3
"""
YouTube Channel URL Extractor - Extract all video URLs from a YouTube channel
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Optional
import yt_dlp
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class YouTubeChannelExtractor:
    def __init__(self, output_dir: str = "extracted_urls"):
        """
        Initialize the YouTube channel extractor
        
        Args:
            output_dir: Directory to save extracted URLs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def extract_channel_urls(self, channel_url: str, max_videos: Optional[int] = None) -> List[str]:
        """
        Extract all video URLs from a YouTube channel
        
        Args:
            channel_url: YouTube channel URL
            max_videos: Maximum number of videos to extract (None for all)
        
        Returns:
            List of video URLs
        """
        try:
            print(f"{Fore.CYAN}Extracting URLs from channel: {channel_url}{Style.RESET_ALL}")
            
            # Configure yt-dlp options for channel extraction
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,  # Don't download, just extract info
                'ignoreerrors': True,
                'no_warnings': True,
            }
            
            if max_videos:
                ydl_opts['playlistend'] = max_videos
            
            urls = []
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract channel info
                info = ydl.extract_info(channel_url, download=False)
                
                if not info:
                    print(f"{Fore.RED}Error: Could not extract channel information{Style.RESET_ALL}")
                    return []
                
                # Get channel title
                channel_title = info.get('title', 'Unknown Channel')
                print(f"{Fore.GREEN}Channel: {channel_title}{Style.RESET_ALL}")
                
                # Extract video URLs from entries
                entries = info.get('entries', [])
                if not entries:
                    print(f"{Fore.YELLOW}No videos found in channel{Style.RESET_ALL}")
                    return []
                
                print(f"{Fore.CYAN}Found {len(entries)} videos{Style.RESET_ALL}")
                
                for i, entry in enumerate(entries, 1):
                    if entry and 'url' in entry:
                        video_url = entry['url']
                        video_title = entry.get('title', 'Unknown Title')
                        urls.append(video_url)
                        print(f"{Fore.GREEN}[{i}] {video_title}{Style.RESET_ALL}")
                        print(f"    URL: {video_url}")
                        
                        if max_videos and i >= max_videos:
                            break
            
            print(f"\n{Fore.GREEN}✓ Successfully extracted {len(urls)} video URLs{Style.RESET_ALL}")
            return urls
            
        except Exception as e:
            print(f"{Fore.RED}✗ Error extracting channel URLs: {e}{Style.RESET_ALL}")
            return []
    
    def extract_multiple_channels(self, channel_urls: List[str], max_videos: Optional[int] = None) -> Dict[str, List[str]]:
        """
        Extract URLs from multiple channels
        
        Args:
            channel_urls: List of channel URLs
            max_videos: Maximum number of videos per channel
        
        Returns:
            Dict mapping channel URLs to lists of video URLs
        """
        results = {}
        
        print(f"{Fore.CYAN}Starting extraction from {len(channel_urls)} channels...{Style.RESET_ALL}")
        
        for i, channel_url in enumerate(channel_urls, 1):
            print(f"\n{Fore.YELLOW}[{i}/{len(channel_urls)}] Processing: {channel_url}{Style.RESET_ALL}")
            urls = self.extract_channel_urls(channel_url, max_videos)
            results[channel_url] = urls
        
        # Summary
        total_videos = sum(len(urls) for urls in results.values())
        successful_channels = sum(1 for urls in results.values() if urls)
        
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}EXTRACTION SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"Total channels: {len(channel_urls)}")
        print(f"Successful extractions: {successful_channels}")
        print(f"Total videos found: {total_videos}")
        
        return results
    
    def save_urls_to_file(self, urls: List[str], filename: str):
        """Save URLs to a text file"""
        try:
            filepath = self.output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("# YouTube video URLs extracted from channel\n")
                f.write("# Generated by YouTube Channel Extractor\n\n")
                for url in urls:
                    f.write(f"{url}\n")
            print(f"{Fore.GREEN}✓ URLs saved to: {filepath}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Error saving URLs: {e}{Style.RESET_ALL}")
    
    def save_results_to_json(self, results: Dict[str, List[str]], filename: str):
        """Save extraction results to JSON file"""
        try:
            filepath = self.output_dir / filename
            
            # Prepare data for JSON
            json_data = {
                'extraction_info': {
                    'total_channels': len(results),
                    'total_videos': sum(len(urls) for urls in results.values()),
                    'successful_channels': sum(1 for urls in results.values() if urls)
                },
                'channels': {}
            }
            
            for channel_url, urls in results.items():
                json_data['channels'][channel_url] = {
                    'video_count': len(urls),
                    'urls': urls
                }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            print(f"{Fore.GREEN}✓ Results saved to: {filepath}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Error saving JSON: {e}{Style.RESET_ALL}")

def load_channels_from_file(filename: str) -> List[str]:
    """Load channel URLs from a text file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return urls
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{filename}' not found{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED}Error reading file '{filename}': {e}{Style.RESET_ALL}")
        return []

def main():
    parser = argparse.ArgumentParser(
        description="Extract all video URLs from YouTube channels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract all videos from a channel
  python channel_extractor.py "https://www.youtube.com/@example"
  
  # Extract first 10 videos from a channel
  python channel_extractor.py -m 10 "https://www.youtube.com/@example"
  
  # Extract from multiple channels
  python channel_extractor.py channel1_url channel2_url
  
  # Extract from channels listed in a file
  python channel_extractor.py -i channels.txt
  
  # Save results to specific files
  python channel_extractor.py -o my_urls.txt -j results.json "https://www.youtube.com/@example"
        """
    )
    
    parser.add_argument('channels', nargs='*', help='YouTube channel URLs to extract from')
    parser.add_argument('-i', '--input-file', help='File containing channel URLs (one per line)')
    parser.add_argument('-o', '--output-file', help='Output file for URLs (default: channel_urls.txt)')
    parser.add_argument('-j', '--json-file', help='Output JSON file for detailed results')
    parser.add_argument('-d', '--output-dir', default='extracted_urls', help='Output directory (default: extracted_urls)')
    parser.add_argument('-m', '--max-videos', type=int, help='Maximum number of videos to extract per channel')
    
    args = parser.parse_args()
    
    # Collect channel URLs
    channels = []
    if args.input_file:
        channels.extend(load_channels_from_file(args.input_file))
    if args.channels:
        channels.extend(args.channels)
    
    if not channels:
        print(f"{Fore.RED}Error: No channel URLs provided. Use -i/--input-file or provide URLs as arguments.{Style.RESET_ALL}")
        parser.print_help()
        sys.exit(1)
    
    # Create extractor
    extractor = YouTubeChannelExtractor(args.output_dir)
    
    # Extract URLs
    results = extractor.extract_multiple_channels(channels, args.max_videos)
    
    # Save results
    if results:
        # Combine all URLs
        all_urls = []
        for urls in results.values():
            all_urls.extend(urls)
        
        # Save to text file
        output_filename = args.output_file or "channel_urls.txt"
        extractor.save_urls_to_file(all_urls, output_filename)
        
        # Save to JSON if requested
        if args.json_file:
            extractor.save_results_to_json(results, args.json_file)
        
        print(f"\n{Fore.GREEN}Ready to download! Use these commands:{Style.RESET_ALL}")
        print(f"python youtube_downloader.py -i {output_filename}")
        print(f"python youtube_downloader.py -i {output_filename} -f 720p")
        print(f"python youtube_downloader.py -i {output_filename} -f mp4 -o downloads")



def get_channel_urls(channels):
    # Example channel URLs (replace with your own)
    if isinstance(channels, str):
        channels = [channels]

    # Create extractor instance
    extractor = YouTubeChannelExtractor(output_dir="extracted_channels")

    # Extract URLs from channels (limit to 5 videos per channel for demo)
    print("Extracting URLs from channels...")
    results = extractor.extract_multiple_channels(channels, max_videos=500)

    # Print results
    print("\nExtraction Results:")
    for channel_url, urls in results.items():
        print(f"\nChannel: {channel_url}")
        print(f"Videos found: {len(urls)}")
        for i, url in enumerate(urls[:3], 1):  # Show first 3 URLs
            print(f"  {i}. {url}")
        if len(urls) > 3:
            print(f"  ... and {len(urls) - 3} more")

    # Save results
    if results:
        # Combine all URLs
        all_urls = []
        for urls in results.values():
            all_urls.extend(urls)

        # Save to files
        # extractor.save_urls_to_file(all_urls, "example_channel_urls.txt")
        # extractor.save_results_to_json(results, "example_results.json")

        print(f"\nTotal videos extracted: {len(all_urls)}")
        print("Files saved:")
        print("- example_channel_urls.txt (for downloading)")
        print("- example_results.json (detailed results)")
    return all_urls, results

if __name__ == "__main__":
    main() 
