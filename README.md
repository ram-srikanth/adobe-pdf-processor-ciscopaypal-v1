# Cisco\_Paypal\_Unemployed - Adobe Hackathon 2025 Round 1B Submission

## Team Members

* Ram Srikanth
* Nikhileshwar Reddy
* Thanush

---

## Project Overview

Our Round 1B solution processes multiple document collections to intelligently extract the most relevant sections and summaries based on a user persona and their job-to-be-done. It uses a combination of rule-based heading extraction, TF-IDF-based relevance scoring, and light summarization to generate concise insights from a given corpus. The code is entirely offline, scalable, and designed to work efficiently with diverse PDF formats.

---

## Technology Stack

* [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) — for extracting text and structure from PDF files
* [scikit-learn](https://scikit-learn.org/) — for TF-IDF vectorization and cosine similarity
* Python 3.11 — core programming language

---

## Execution Instructions

### Build the Docker Image

```bash
docker build --platform linux/amd64 -t adobe-pdf-processor:ciscopaypal-v1 .
```

### Run the Docker Container

   For Unix/macOS:

   ```bash
   docker run --rm -v $(pwd):/app adobe-pdf-processor:ciscopaypal-v1b
   ```

   For Windows (PowerShell):

   ```powershell
   docker run --rm -v ${PWD}:/app adobe-pdf-processor:ciscopaypal-v1b
   ```

---

## Output Format

Each `challenge1b_output.json` will contain:

```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "Travel Agent",
    "job_to_be_done": "Plan a trip to South of France",
    "timestamp": "2025-07-28T18:30:00"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Best Itineraries",
      "importance_rank": 1,
      "page_number": 3,
      "relevance_score": 0.832,
      "relevance_factors": ["Title matches: itineraries", "Optimal length"]
    },
    ...
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "page_number": 3,
      "refined_text": "The south of France is known for its coastal beauty, charming villages..."
    },
    ...
  ]
}
```

---

## Directory Layout

```
.
├── main.py
├── Dockerfile
├── requirements.txt
├── Collection 1/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection 2/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
├── Collection 3/
│   ├── PDFs/
│   ├── challenge1b_input.json
│   └── challenge1b_output.json
```

---

## Compliance Checklist

* [x] Works offline without internet access
* [x] Processes all specified PDF documents
* [x] Produces `challenge1b_output.json` for each collection
* [x] Completes execution within time and memory constraints
* [x] Uses interpretable, rule-based methods for structure and content extraction

---

## Submission Statement

This repository is submitted as part of **Adobe Hackathon 2025 - Round 1B** by the team **Cisco\_Paypal\_Unemployed**.
