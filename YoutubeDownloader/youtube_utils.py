from YoutubeDownloader.channel_extractor import get_channel_urls
from YoutubeDownloader.definitions import PROJECT_ROOT_DIR

def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    print(lines)
    # Read each line. If the line starts with # then skip it.
    # if the line start with channel, then parse the channel
    # if line starts with url, download it

    urls = list()

    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        elif line.startswith("channel"):
            words = line.split(" ")
            all_urls, results = get_channel_urls(words[1]) 
            urls.extend(all_urls)
        # Check if the line contains youtube
        elif "youtube" in line:
            urls.append(line)
        else:
            print(f"Unknown line: {line}")
    return urls


if __name__ == "__main__":
    urls = parse_file(f"{PROJECT_ROOT_DIR}/scripts/long_list.txt")
    print(f"Total urls: {len(urls)}")