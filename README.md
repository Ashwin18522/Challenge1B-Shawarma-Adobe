# Challenge1B-Shawarma-Adobe
# PDF Structure Extraction Pipeline

This project extracts hierarchical structure (titles, headings, outline) from PDF documents using a combination of font, text pattern, visual, and semantic analysis.

## Features

- Multi-threaded PDF analysis for speed  
- Font, text pattern, and visual layout analysis  
- Semantic validation of headings  
- Outputs structured JSON for each PDF  

---

## Directory Structure

- `src/` - Source code for extractors and processors  
- `input/` - Place your PDF files here for processing  
- `output/` - Extracted JSON files will be saved here  
- `requirements.txt` / `Requirements.txt` - Python dependencies  
- `Dockerfile` - For containerized execution  

---

## Requirements

- Python 3.8+  
- System dependencies:  
  - Tesseract OCR (for visual analysis)  
  - libgl1-mesa-glx, libglib2.0-0 (for OpenCV)  
- See `requirements.txt` for Python packages  

### Python Dependencies

Install with:

pip install -r requirements.txt

text

### System Dependencies (Ubuntu/Debian)

sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng libgl1-mesa-glx libglib2.0-0

text

On Windows, install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and ensure it is in your PATH.

---

## Usage

### 1. Place PDFs in the Input Folder

Copy your PDF files into the `input/` directory.

### 2. Run the Extractor

From the `extractions/` directory, run:

python src/main.py

text

- The script will process all PDFs in `input/` and write JSON files to `output/`.

### 3. View Results

Check the `output/` directory for `.json` files corresponding to each input PDF.

---

## Docker Usage

A Dockerfile is provided for easy setup.

### Build the Docker Image

docker build -t pdf-extractor .

text

### Run the Container

docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-extractor

text

- Mounts your local `input/` and `output/` folders into the container.

---

## Configuration

- Most settings are in `src/utils/config.py` (DPI, timeouts, confidence thresholds, etc.)  
- By default, processes all PDFs in `input/` and writes to `output/`.

---

## Sample Data

- Example PDFs are in `input/`  
- Example outputs are in `output/`

---

## Troubleshooting

- Ensure Tesseract OCR is installed and accessible.  
- For Windows, you may need to add Tesseract to your PATH.  
- If you encounter missing dependencies, check both `requirements.txt` and system packages.  

---

## License

MIT License
