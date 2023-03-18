import openai
from PyPDF2 import PdfReader

def load_api_key(file_path: str):
    with open(file_path, "r") as f:
        return f.readline().strip("\n")

def create_chat_object(file_path: str):
    api_key = load_api_key(file_path)
    openai.api_key = api_key
    return openai.ChatCompletion

def parse_results(chatgpt_output) -> str:
    return chatgpt_output["choices"][0]["message"]["content"]

def parse_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text_body = ""
    for page in reader.pages:
        text_body += " " + page.extract_text()
    return text_body

def parse_pdf_from_flask_object(file_obj) -> str:
    reader = PdfReader(file_obj)
    text_body = ""
    for page in reader.pages:
        text_body += " " + page.extract_text()
    return text_body

