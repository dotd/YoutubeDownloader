#!/usr/bin/env python3
"""
Example usage of the YouTube Downloader
"""

from YoutubeDownloader.youtube_downloader import YouTubeDownloader

def main():
    # Example URLs (replace with your own)
    urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
        "https://www.youtube.com/watch?v=9bZkp7q19f0",  # Gangnam Style
    ]
    
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