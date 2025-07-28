# Round 1B - Adobe PDF Collection Analyzer

This project processes a set of document collections using PDF parsing, heading extraction, and relevance-based ranking to extract the **most useful sections and summaries** based on a given persona and job description.

---

## Directory Structure

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

Each collection must contain:

* A `PDFs/` folder with documents
* A `challenge1b_input.json` file specifying the persona, task, and filenames

---

## How to Run

### Option 1: Python (Locally)

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the processor**

   ```bash
   python main.py
   ```

---

### Option 2: Docker

1. **Build the image**

   ```bash
   docker build --platform linux/amd64 -t adobe-pdf-processor:ciscopaypal-v1 .
   ```

2. **Run the container**

   Mount the current directory inside Docker so it can access all collections:

   ```bash
   docker run --rm -v $(pwd):/app adobe-pdf-processor:ciscopaypal-v1
   ```

   On Windows (PowerShell):

   ```powershell
   docker run --rm -v ${PWD}:/app adobe-pdf-processor:ciscopaypal-v1
   ```

---

## Output

Each `challenge1b_output.json` will contain:

* `metadata`: Input details and timestamp
* `extracted_sections`: Top 10 relevant headings across documents
* `subsection_analysis`: Concise summaries from top pages

---

## Team

**Team Name**: Cisco\_Paypal\_Unemployed
**Members**:

* Ram Srikanth
* Nikhileshwar Reddy
* Thanush

---

## Notes

* Uses TF-IDF + cosine similarity for relevance ranking
* Summarization is done using sentence ranking (unsupervised)
* Fully self-contained with zero external API dependencies

---
