import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TOP_N_SECTIONS = 10
TOP_N_SUBSECTIONS = 5

def extract_headings_from_text(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                text = " ".join([span["text"] for span in line["spans"]]).strip()
                if 20 < len(text) < 100 and text[0].isupper() and not text.endswith("."):
                    headings.append({
                        "text": text,
                        "page": page_num + 1
                    })
    return headings

def rank_sections_tfidf(headings, persona, job):
    query = f"{persona} needs to {job}"
    if not headings:
        return []

    texts = [query] + [h["text"] for h in headings]
    vecs = TfidfVectorizer().fit_transform(texts)
    scores = cosine_similarity(vecs[0:1], vecs[1:]).flatten()

    for i, h in enumerate(headings):
        h["score"] = scores[i]

    top_sections = sorted(headings, key=lambda x: -x["score"])[:TOP_N_SECTIONS]
    for idx, sec in enumerate(top_sections):
        sec["section_title"] = sec.pop("text")
        sec["page_number"] = sec.pop("page")
        sec["importance_rank"] = idx + 1
        del sec["score"]
    return top_sections

def extract_page_text(pdf_path, page_number):
    try:
        doc = fitz.open(pdf_path)
        return doc.load_page(page_number - 1).get_text("text")
    except:
        return ""

def textrank_summary(text, max_lines=3):
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 40]
    if len(lines) <= max_lines:
        return " ".join(lines)

    vecs = TfidfVectorizer().fit_transform(lines)
    scores = cosine_similarity(vecs, vecs).sum(axis=1)
    ranked = [line for _, line in sorted(zip(scores, lines), reverse=True)]
    return " ".join(ranked[:max_lines])

def process_collection(collection_path):
    input_file = os.path.join(collection_path, "challenge1b_input.json")
    output_file = os.path.join(collection_path, "challenge1b_output.json")
    pdf_dir = os.path.join(collection_path, "PDFs")

    if not os.path.exists(input_file) or not os.path.isdir(pdf_dir):
        print(f"⚠️ Skipping: {collection_path}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    persona = data.get("persona")
    job = data.get("job_to_be_done")
    documents = data.get("documents")

    all_headings = []
    for doc in documents:
        filename = doc.get("document") or doc.get("filename")
        pdf_path = os.path.join(pdf_dir, filename)
        if not os.path.exists(pdf_path):
            continue
        doc_headings = extract_headings_from_text(pdf_path)
        for h in doc_headings:
            h["document"] = filename
        all_headings.extend(doc_headings)

    extracted_sections = rank_sections_tfidf(all_headings, persona, job)

    subsection_analysis = []
    seen_pages = set()
    for sec in extracted_sections:
        key = (sec["document"], sec["page_number"])
        if key in seen_pages:
            continue
        seen_pages.add(key)
        raw_text = extract_page_text(os.path.join(pdf_dir, sec["document"]), sec["page_number"])
        summary = textrank_summary(raw_text)
        subsection_analysis.append({
            "document": sec["document"],
            "page_number": sec["page_number"],
            "refined_text": summary
        })
        if len(subsection_analysis) >= TOP_N_SUBSECTIONS:
            break

    output = {
        "metadata": {
            "input_documents": [doc.get("document") or doc.get("filename") for doc in documents],
            "persona": persona,
            "job_to_be_done": job,
            "timestamp": datetime.now().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Processed: {collection_path}")

def main():
    root = os.getcwd()
    print(f"🔍 Scanning folders in: {root}")
    for d in os.listdir(root):
        full_path = os.path.join(root, d)
        if os.path.isdir(full_path) and "Collection" in d:
            print(f"Processing: {full_path}")
            process_collection(full_path)

if __name__ == "__main__":
    main()
