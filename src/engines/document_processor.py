import concurrent.futures
import fitz  # PyMuPDF
import re

class ParallelDocumentProcessor:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers

    def process_documents_parallel(self, pdf_paths):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_pdf = {executor.submit(self.extract_semantic_sections, path): path for path in pdf_paths}
            results = {}
            for future in concurrent.futures.as_completed(future_to_pdf):
                pdf = future_to_pdf[future]
                results[pdf] = future.result()
            return results

    def extract_semantic_sections(self, pdf_path):
        doc = fitz.open(pdf_path)
        sections = []
        current_section = None
        for page_num in range(len(doc)):
            page = doc[page_num]
            text_blocks = page.get_text("blocks")
            for block in text_blocks:
                text = block[4].strip()
                if not text: continue
                if re.match(r'^(?:[A-Z][A-Z0-9 ,.:\-\(\)]+)$', text) and len(text.split()) < 15:
                    section = {
                        "section_title": text,
                        "page_number": page_num+1,
                        "content": [],
                    }
                    if current_section:
                        sections.append(current_section)
                    current_section = section
                elif current_section:
                    current_section["content"].append(text)
        if current_section:
            sections.append(current_section)
        for sec in sections:
            sec["content"] = "\n".join(sec["content"])
        return sections
