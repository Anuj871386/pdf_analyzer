
from pypdf import PdfReader
from pypdf.errors import PdfReadError

def extract_text(path):
    text = ""

    try:
        reader = PdfReader(path)
    except Exception as e:
        print("PDF open error:", e)
        return ""

    for i, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        except PdfReadError as e:
            print(f"Skipping page {i} due to error:", e)
            continue
        except Exception as e:
            print(f"Unexpected error on page {i}:", e)
            continue

    return text.strip()
