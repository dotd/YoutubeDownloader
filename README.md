# YouTube Downloader & Channel Extractor

A powerful Python toolkit for extracting video URLs from YouTube channels and downloading videos in specific formats with support for batch processing.

## Features

- ✅ **Channel URL Extraction**: Extract all video URLs from YouTube channels
- ✅ **Multiple Video Downloads**: Download multiple YouTube videos at once
- ✅ **Format Selection**: Support for various video formats (MP4, WebM, etc.)
- ✅ **Quality Selection**: Choose quality (720p, 1080p, best, worst, etc.)
- ✅ **Audio-only Downloads**: Extract audio in various formats
- ✅ **Batch Processing**: Process multiple channels and videos
- ✅ **Progress Tracking**: Real-time progress with colored output
- ✅ **Automatic Subtitles**: Download subtitles automatically
- ✅ **Thumbnail Download**: Save video thumbnails
- ✅ **Format Listing**: View available formats for videos
- ✅ **Comprehensive Toolkit**: All-in-one solution for channel processing

## Installation

1. **Clone or download this repository**
   ```bash
   cd YoutubeDownloader
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install yt-dlp requests tqdm colorama
   ```

## Quick Start

### Extract and Download from a Channel
```bash
# Extract all videos from a channel and download them in 720p
python youtube_toolkit.py -c "https://www.youtube.com/@example" -f 720p

# Extract first 10 videos from a channel
python youtube_toolkit.py -c "https://www.youtube.com/@example" -m 10 -f mp4
```

### Extract URLs Only
```bash
# Extract URLs without downloading
python youtube_toolkit.py -c "https://www.youtube.com/@example" --extract-only

# Extract from multiple channels
python youtube_toolkit.py -i channels.txt --extract-only
```

### Download from URL File
```bash
# Download videos from extracted URLs
python youtube_toolkit.py --download-only urls.txt -f 1080p
```

## Individual Tools

### 1. Channel Extractor (`channel_extractor.py`)

Extract all video URLs from YouTube channels.

```bash
# Extract all videos from a channel
python channel_extractor.py "https://www.youtube.com/@example"

# Extract first 10 videos
python channel_extractor.py -m 10 "https://www.youtube.com/@example"

# Extract from multiple channels
python channel_extractor.py channel1_url channel2_url

# Extract from channels listed in a file
python channel_extractor.py -i channels.txt

# Save results to specific files
python channel_extractor.py -o my_urls.txt -j results.json "https://www.youtube.com/@example"
```

**Channel URL Formats Supported:**
- `https://www.youtube.com/@channelname`
- `https://www.youtube.com/c/channelname`
- `https://www.youtube.com/channel/CHANNEL_ID`
- `https://www.youtube.com/user/username`

### 2. Video Downloader (`youtube_downloader.py`)

Download videos in specific formats.

```bash
# Download a single video in best quality
python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Download multiple videos in MP4 format
python youtube_downloader.py -f mp4 url1 url2 url3

# Download videos from a file
python youtube_downloader.py -i urls.txt -f 720p

# List available formats for a video
python youtube_downloader.py -l "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### 3. Complete Toolkit (`youtube_toolkit.py`)

All-in-one solution combining extraction and downloading.

```bash
# Extract and download from channels
python youtube_toolkit.py -c "https://www.youtube.com/@example" -f 720p

# Extract only (no download)
python youtube_toolkit.py -c "https://www.youtube.com/@example" --extract-only

# Download only from URL file
python youtube_toolkit.py --download-only urls.txt -f mp4

# Extract from multiple channels with limit
python youtube_toolkit.py -i channels.txt -m 10 -f 1080p
```

## Command Line Options

### Channel Extractor Options
- `channels`: YouTube channel URLs to extract from
- `-i, --input-file`: File containing channel URLs (one per line)
- `-o, --output-file`: Output file for URLs (default: channel_urls.txt)
- `-j, --json-file`: Output JSON file for detailed results
- `-d, --output-dir`: Output directory (default: extracted_urls)
- `-m, --max-videos`: Maximum number of videos to extract per channel

### Video Downloader Options
- `urls`: YouTube URLs to download
- `-i, --input-file`: File containing URLs (one per line)
- `-o, --output-dir`: Output directory (default: downloads)
- `-f, --format`: Preferred format (best, worst, mp4, webm, 720p, 1080p, audio_only, audio_mp3)
- `--format-id`: Specific format ID to download
- `-l, --list-formats`: List available formats for URLs

### Toolkit Options
- `-c, --channels`: Channel URLs to process
- `-i, --input-file`: File containing channel URLs
- `--download-only`: Download only from URL file
- `--extract-only`: Extract URLs only, no download
- `-m, --max-videos`: Maximum videos per channel
- `-f, --format`: Video format preference
- `-o, --output-file`: Output file for extracted URLs
- `-d, --output-dir`: Base output directory

## Format Options

- `best`: Best quality available
- `worst`: Worst quality available
- `mp4`: Best MP4 format
- `webm`: Best WebM format
- `720p`: Best quality up to 720p
- `1080p`: Best quality up to 1080p
- `audio_only`: Audio only (M4A)
- `audio_mp3`: Audio only (MP3)

## Programmatic Usage

### Channel Extraction
```python
from channel_extractor import YouTubeChannelExtractor

# Create extractor
extractor = YouTubeChannelExtractor(output_dir="extracted_urls")

# Extract URLs from channels
channels = ["https://www.youtube.com/@example"]
results = extractor.extract_multiple_channels(channels, max_videos=10)

# Save results
all_urls = []
for urls in results.values():
    all_urls.extend(urls)
extractor.save_urls_to_file(all_urls, "my_urls.txt")
```

### Video Downloading
```python
from youtube_downloader import YouTubeDownloader

# Create downloader
downloader = YouTubeDownloader(output_dir="downloads", format_preference="720p")

# Download videos
urls = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
results = downloader.download_multiple(urls)
```

### Complete Workflow
```python
from youtube_toolkit import YouTubeToolkit

# Create toolkit
toolkit = YouTubeToolkit(output_dir="youtube_content")

# Extract and download
channels = ["https://www.youtube.com/@example"]
toolkit.extract_and_download(channels, format_preference="720p", max_videos=5)
```

## File Structure

```
YoutubeDownloader/
├── youtube_downloader.py      # Video downloader
├── channel_extractor.py       # Channel URL extractor
├── youtube_toolkit.py         # Complete toolkit
├── example.py                 # Downloader example
├── channel_example.py         # Extractor example
├── requirements.txt           # Dependencies
├── urls.txt                   # Sample video URLs
├── channels.txt               # Sample channel URLs
└── README.md                  # This file
```

## Examples

### Complete Channel Processing
```bash
# 1. Extract URLs from a channel
python channel_extractor.py "https://www.youtube.com/@example" -o channel_urls.txt

# 2. Download all videos in 720p
python youtube_downloader.py -i channel_urls.txt -f 720p

# Or do it all at once:
python youtube_toolkit.py -c "https://www.youtube.com/@example" -f 720p
```

### Batch Processing Multiple Channels
```bash
# Create channels.txt with your channel URLs
echo "https://www.youtube.com/@channel1" > channels.txt
echo "https://www.youtube.com/@channel2" >> channels.txt

# Extract first 5 videos from each channel
python youtube_toolkit.py -i channels.txt -m 5 --extract-only

# Download all extracted videos
python youtube_toolkit.py --download-only channel_urls.txt -f mp4
```

### Audio Extraction
```bash
# Extract audio only from channel videos
python youtube_toolkit.py -c "https://www.youtube.com/@example" -f audio_only
```

## Output

- **Extracted URLs**: Saved to text files for easy reuse
- **Downloaded Videos**: Saved to organized directories
- **Progress Tracking**: Real-time progress with colored output
- **Detailed Results**: JSON files with extraction metadata
- **Automatic Organization**: Separate directories for URLs and downloads

## Requirements

- Python 3.6+
- yt-dlp (YouTube downloader library)
- requests (HTTP library)
- tqdm (Progress bars)
- colorama (Colored output)

## Troubleshooting

### Common Issues

1. **"No module named 'yt_dlp'"**
   ```bash
   pip install yt-dlp
   ```

2. **Channel extraction fails**
   - Check if the channel URL is valid
   - Try different channel URL formats
   - Some channels may have restrictions

3. **Download fails**
   - Check if the URL is valid
   - Try a different format
   - Check your internet connection

4. **Permission errors**
   - Make sure you have write permissions to the output directory
   - Try running with administrator privileges if needed

### Getting Format IDs

To find the best format ID for a video:
```bash
python youtube_downloader.py -l "YOUR_YOUTUBE_URL"
```

This will show all available formats with their IDs, quality, and file sizes.

## Legal Notice

This tool is for personal use only. Please respect YouTube's Terms of Service and copyright laws. Only download videos you have permission to download.

## License

This project is open source and available under the MIT License. # YoutubeDownloader
