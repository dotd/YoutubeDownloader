import google.generativeai as genai
from YoutubeDownloader.gemini_utils import get_gemini_client, list_gemini_models

def tst_simple_query():
    print("\n".join(list_gemini_models()))
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("what is the capital of France? Please provide a full answer.")
    print(response.text)


if __name__ == "__main__":
    tst_simple_query()