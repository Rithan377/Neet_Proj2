# services/parser.py
import fitz  # PyMuPDF
import re

def clean_text(text: str) -> str:
    """Remove extra spaces and newlines."""
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_pdf(file_path: str, chunk_size: int = 500):
    """
    Parse a PDF into chunks, handling multi-page continuation of topics.

    Returns:
        List of dicts: [{"title": str, "text": str, "start_page": int, "end_page": int}, ...]
    """
    doc = fitz.open(file_path)
    chunks = []
    current_title = None    
    current_text = ""
    start_page = 1

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        text = clean_text(text)
        if not text:
            continue

        # Split text into paragraphs first
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        for para in paragraphs:
            # Detect if paragraph is a new title
            if re.match(r"^(Chapter|Section|Topic|\d+(\.\d+)*)(:?\s.*)?$", para):
                # Save previous chunk
                if current_text:
                    chunks.append({
                        "title": current_title or "Unknown",
                        "text": current_text.strip(),
                        "start_page": start_page,
                        "end_page": page_num
                    })
                current_title = para
                current_text = ""
                start_page = page_num
            else:
                current_text += " " + para

            # Split large text into smaller chunks
            if len(current_text) > chunk_size:
                chunks.append({
                    "title": current_title or "Unknown",
                    "text": current_text.strip(),
                    "start_page": start_page,
                    "end_page": page_num
                })
                current_text = ""
                start_page = page_num

    # Save remaining text
    if current_text:
        chunks.append({
            "title": current_title or "Unknown",
            "text": current_text.strip(),
            "start_page": start_page,
            "end_page": page_num
        })

    return chunks

# =========================
# Example usage
# =========================
if __name__ == "__main__":
    chunks = parse_pdf("./data/med-test-rag.pdf")
    for chunk in chunks[:5]:
        print(chunk)
