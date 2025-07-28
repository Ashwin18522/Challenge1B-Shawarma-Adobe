# Persona-Driven Document Intelligence System (Hackathon Round 1B)

This project implements the **Persona-Driven Document Intelligence** pipeline designed for the Adobe Hackathon Round 1B challenge.  
It processes multiple PDFs in parallel, intelligently understands a specific user persona and their job to be done, and extracts and ranks the most relevant PDF content tailored to that persona.

---

## Features

- Lightning-fast parallel PDF processing
- Semantic chunking and structured content extraction
- Zero-shot persona and job-to-be-done understanding via NLP
- Fast and efficient semantic matching with SentenceTransformers (`all-MiniLM-L6-v2`)
- Multi-criteria intelligent ranking combining semantic similarity, keyword relevance, and section importance
- Fully offline, CPU-only execution, Dockerized and optimized for `linux/amd64`
- JSON output formatted per hackathon strict requirements

---

## Directory Structure
```
persona_engine/
├── input/ # Place PDFs and persona_job.json here
├── output/ # Output JSON files will be saved here
├── models/ # Offline embedding model files (e.g. all-MiniLM-L6-v2)
├── src/
│ ├── engines/
│ │ ├── document_processor.py
│ │ ├── persona_engine.py
│ │ ├── semantic_engine.py
│ │ └── ranking_engine.py
│ └── utils/
├── main.py # Orchestrates the full pipeline execution
├── requirements.txt
├── Dockerfile
├── en_core_web_sm-3.6.0-py3-none-any.whl # Offline spaCy model wheel
├── .gitignore
└── README.md # This file
```

---

## Setup & Installation

### Prerequisites

- Docker Desktop with Linux containers enabled (recommended)  
- Python 3.9+ (only for local testing, not required if using Docker)

### Python Dependencies (for local runs/testing)

Install dependencies:

```
pip install -r requirements.txt
pip install ./en_core_web_sm-3.6.0-py3-none-any.whl
```

> *Note:* The spaCy model wheel is included offline per hackathon requirement.

### Models

- Download the [all-MiniLM-L6-v2](https://www.sbert.net/docs/pretrained_models.html) SentenceTransformer model **offline** and place it inside the `models/all-MiniLM-L6-v2/` directory.
- Keep the spaCy model wheel (`en_core_web_sm-3.6.0-py3-none-any.whl`) in the root for offline install during Docker build or local install.

---

## Usage

### Step 1: Prepare Inputs

Place your **input PDF files** into the `input/` folder.

Add a `persona_job.json` file in `input/` describing the persona and job, example(as per given in the instructions:
```
{
"persona": "PhD Researcher in Computational Biology",
"job_to_be_done": "Prepare comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
}
```

### Step 2: Run Locally (Optional)

You can run the pipeline locally:

```
python main.py
```

Outputs will be saved to the `output/output.json` file.

### Step 3: Run with Docker (Recommended for Production/Submission)

1. **Build the Docker Image**

```
docker build --platform linux/amd64 -t persona_engine:latest .
```

2. **Run the Docker Container**

```
docker run --rm
-v $(pwd)/input:/app/input
-v $(pwd)/output:/app/output
--network none persona_engine:latest
```

> On Windows, replace `$(pwd)` with the full absolute path, e.g.:  
>  
> ```
> docker run --rm `
>   -v "C:\path\to\persona_engine\input:/app/input" `
>   -v "C:\path\to\persona_engine\output:/app/output" `
>   --network none persona_engine:latest
> ```

3. The results will be available in `output/output.json`.

---

## System Architecture Overview

### Phase 1: Parallel Document Processor

- Uses multithreading (`ThreadPoolExecutor`) and `PyMuPDF` for fast, parallel PDF section extraction.
- Produces semantically chunked sections with metadata (page numbers, section titles).

### Phase 2: Zero-Shot Persona Engine

- Analyzes persona descriptions and job-to-be-done text using spaCy NLP.
- Extracts skills, interests, and job information requirements dynamically without training.

### Phase 3: Semantic Matching Engine

- Encodes document sections and combined persona-job information using efficient CPU-friendly MiniLM embeddings.
- Uses cosine similarity combined with keyword boosting for relevance scoring.

### Phase 4: Intelligent Ranker

- Applies multi-criteria ranking: semantic similarity, keyword relevance, section importance.
- Extracts refined sub-sections and validates output quality.
- Produces final ranked content ready for downstream consumption.

---

## Input/Output Specifications

### Input
```
{
"documents": ["doc1.pdf", "doc2.pdf", "doc3.pdf"],
"persona": "PhD Researcher in Computational Biology",
"job_to_be_done": "Prepare comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
}
```

- `documents`: list of PDF filenames located in `input/`  
- `persona`: string describing the persona  
- `job_to_be_done`: string describing the task  

### Output (`output/output.json`)

JSON containing:

- `metadata` (input parameters, timestamps, processing time)  
- `extracted_sections` (document, page, section title, importance rank, relevance score)  
- `sub_section_analysis` (refined text extracted from top sections, ranked)  

(Full output format per hackathon requirements.)

---

## Important Notes

- The entire system runs **CPU-only**, no GPU dependencies.  
- Model sizes are under **1GB**, compliant with hackathon constraints.  
- No internet is required during runtime; all models are pre-downloaded and included.  
- Docker container runs on Linux/amd64 as mandated.  
- Input/output folders are mounted into Docker; no hardcoded paths.  
- Processing time aims to be under 60 seconds for 3-5 documents.

---

## Troubleshooting

- Ensure your PDFs and `persona_job.json` are correctly placed in `input/`.  
- Confirm the MiniLM model folder exists at `models/all-MiniLM-L6-v2`.  
- For Docker, ensure correct path mounting and that Docker Desktop is running with Linux containers enabled.  
- If spaCy throws errors about missing models, confirm the wheel is installed during Docker build or locally.  
- Check Docker build logs for errors during dependency installation.  
- Use logs/print statements inside code for debugging phase-specific issues.

---

## License

This project is licensed under the MIT License.



