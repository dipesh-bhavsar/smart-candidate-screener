from pathlib import Path
import pypdf
from docx import Document
def extract_text(file_path):
    path=Path(file_path);suffix=path.suffix.lower()
    if suffix=='.pdf': return '\n'.join(p.extract_text() or '' for p in pypdf.PdfReader(str(path)).pages)
    elif suffix=='.docx': return '\n'.join(p.text for p in Document(str(path)).paragraphs if p.text.strip())
    elif suffix=='.txt': return path.read_text(encoding='utf-8',errors='ignore')
    raise ValueError(f'Unsupported: {suffix}')
