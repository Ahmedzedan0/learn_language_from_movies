# IELTS Helper Project

## Description
IELTS Helper is a Python-based tool designed to assist in preparing for the IELTS exam. It processes a given IELTS vocabulary PDF by extracting images, cropping specific regions, converting them to black and white, and extracting English words using OCR. The words are then saved in a text file.

## Project Structure
- `main.py`: The main script for PDF processing and image handling.
- `image_selector.py`: A GUI tool to select regions from an image.
- `requirements.txt`: Lists all Python dependencies for the project.
- `images/`: Directory for storing extracted images from the PDF.
- `processed_images/`: Directory for storing cropped images.
- `extracted_text/`: Directory where extracted text files are saved.
- `IELTS ADVANCED VOCABS.pdf`: Sample input PDF file.

## Installation
Ensure you have Python 3.x installed on your system. Then install the required Python libraries:

```bash
pip install -r requirements.txt
