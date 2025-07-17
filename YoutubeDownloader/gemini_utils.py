import google.generativeai as genai

def get_gemini_api_key():
    with open("api_keys/gemini_api_key.txt", "r") as f:
        return f.read().strip()
    
def set_gemini_api_key():
    genai.configure(api_key=get_gemini_api_key())
    
def get_gemini_client(model_name="gemini-2.5-pro"):
    return genai.GenerativeModel(model_name, api_key=get_gemini_api_key())

def list_gemini_models():
    set_gemini_api_key()
    return [model.name for model in genai.list_models()]