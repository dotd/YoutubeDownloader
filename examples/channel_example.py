#!/usr/bin/env python3
"""
Example usage of the YouTube Channel Extractor
"""

from YoutubeDownloader.channel_extractor import get_channel_urls
from YoutubeDownloader.youtube_downloader import download_urls

if __name__ == "__main__":
    # Get the channel urls
    channels = [
        "https://www.youtube.com/@BORGAutomotiveReman/videos",  # Replace with actual channel
        # "https://www.youtube.com/c/example",  # Another channel format
    ]
    all_urls, results = get_channel_urls(channels) 
    print(f"Total videos extracted: {len(all_urls)}")
    all_urls_str = "\n".join([f"{i}. {url}" for i, url in enumerate(all_urls)])  
    print(f"all_urls:\n{all_urls_str}")
    print(f"results:\n {results}")
    
    # Download the urls
    download_urls(all_urls)

