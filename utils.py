import openai

def load_api_key(file_path: str):
    with open(file_path, "r") as f:
        return f.readline().strip("\n")

def create_chat_object(file_path: str):
    api_key = load_api_key(file_path)
    openai.api_key = api_key
    return openai.ChatCompletion

def parse_results(chatgpt_output) -> str:
    return chatgpt_output["choices"][0]["message"]["content"]
