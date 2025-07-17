import google.generativeai as genai
import time
from YoutubeDownloader.gemini_utils import get_gemini_api_key
from YoutubeDownloader.definitions import PROJECT_ROOT_DIR


# Make sure to set your API key
genai.configure(api_key=get_gemini_api_key())

# 1. Upload the video file
print("Uploading file...")
video_file = genai.upload_file(path=f"{PROJECT_ROOT_DIR}/data/denso.mp4",
                               display_name="Denso")
print(f"Completed upload: {video_file.uri}")

# The video is processed asynchronously, so you need to wait for it to be ready. Show the time it takes to process the video.
while video_file.state.name == "PROCESSING":
    print("Waiting for video to be processed.")
    time.sleep(10)
    video_file = genai.get_file(video_file.name)
    
if video_file.state.name == "FAILED":
    raise ValueError(video_file.state.name)

# 2. Make a prompt with the video file
print("Making LLM inference request...")
model = genai.GenerativeModel(model_name="gemini-2.5-pro")

# Create the prompt with your question and the file reference
prompt = "Please describe the video in detail. Please include the following: \n" \
         "1. The times for every scene.\n" \
         "2. Describe the setup that is seen in each scene.\n" \
         "3. Provide a a list of the tools that are used in each scene.\n" \
         "4. Provide the actions that are taken in each scene.\n" \
         "5. Also provide what the narrator says in each scene.\n" \
         "6. Enumerate the scenes in the order they are seen in the video.\n" 
response = model.generate_content([prompt, video_file],
                                  request_options={"timeout": 600})

print(response.text)