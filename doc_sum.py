from PyPDF2 import PdfReader

def parse_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text_body = ""
    for page in reader.pages:
        text_body += " " + page.extract_text()
    return text_body

def research_paper_summary(chat_completion: openai.ChatCompletion, text_body: str, prompt: str, max_num_words: int) -> str:
    pass

def textbook_summary(text_body: str, prompt: str, max_num_words: int) -> str:
    pass

def book_summary(text_body: str, prompt: str, max_num_words: int) -> str:
    pass
