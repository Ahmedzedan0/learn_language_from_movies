# Imports
import PyPDF2
import fitz
import pytesseract
from PIL import Image
import os
import re

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def handle_paths():
    SCRIPT_PATH = os.path.abspath(__file__)
    SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
    CURRENT_DIR = os.path.abspath(os.getcwd())

    # print(f'Script path: {SCRIPT_PATH}')
    # print(f'Script directory: {SCRIPT_DIR}')
    # print(f'Absolute path of the current working directory: {CURRENT_DIR}')
    return SCRIPT_DIR

def pdf_to_images(PDF_PATH, IMAGES_DIR):
    pdf = fitz.open(PDF_PATH)

    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    for page_num in range(pdf.page_count):
        page = pdf.load_page(page_num)  # Load the page
        pix = page.get_pixmap()  # Render page to an image pixmap
        img_path = os.path.join(
            IMAGES_DIR, f'page_{page_num + 1}.png')  # Define image path
        pix.save(img_path)  # Save the image pixmap as an image file
        print(f'Pages saved to {IMAGES_DIR}')

    pdf.close()

def crop_image(input_dir, output_dir, coords):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, 'cut_' + filename)

            with Image.open(image_path) as img:
                cut_img = img.crop(coords)
                cut_img.save(output_path)
                print(f"Cut image saved to {output_path}")

def process_images_to_text(input_dir, output_text_file):

    all_words = []

    # Check if the output file exists; if not, create it
    if not os.path.exists(output_text_file):
        os.makedirs(os.path.dirname(output_text_file), exist_ok=True)
        open(output_text_file, 'a').close()

    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(input_dir, filename)

            # Convert image to black and white
            with Image.open(image_path) as img:
                bw_img = img.convert('L')

            # Extract text from the image
            text = pytesseract.image_to_string(bw_img)

            # Split the text into words and extend the all_words list
            words = text.split()
            all_words.extend(words)

    # Write words to the output file
    with open(output_text_file, 'w') as file:
        for word in all_words:
            file.write(word + '\n')

    print(f"Processed words saved to {output_text_file}")

def preprocess_text_from_file(file_path):
    processed_words = []

    with open(file_path, 'r') as file:
        for line in file:
            # Apply preprocessing steps to each line
            line = line.strip()
            line = line.replace('\t', ' ')
            line = re.sub(r'\s+', ' ', line)
            line = re.sub(r'[^a-zA-Z\s]', '', line)
            line = line.lower()

            # Split the line into words, remove stop words and add to the list if they are 3 or more characters
            words = line.split()
            for word in words:
                if word not in stop_words and len(word) >= 3:
                    processed_words.append(word)

    # Join the processed words with a newline character
    processed_text = '\n'.join(processed_words)

    # Write the processed text back to the file
    with open(file_path, 'w') as file:
        file.write(processed_text)

def main():
    # Define a list of English stop words
    stop_words = set([
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your',
        'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
        'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
        'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
        'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
        'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
        'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
        'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o',
        're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn',
        "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan',
        "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
    ])

    SCRIPT_DIR = handle_paths()
    PDF_PATH = 'IELTS ADVANCED VOCABS.pdf'
    INPUT_DIR = os.path.join(SCRIPT_DIR, 'images')
    PROCESSED_IMAGES_DIR = os.path.join(SCRIPT_DIR, 'processed_images')
    IMAGES_DIR = os.path.join(SCRIPT_DIR, 'images')
    EXTRACTED_TEXT_DIR = os.path.join(SCRIPT_DIR, 'extracted_text')
    output_text_file = os.path.join(EXTRACTED_TEXT_DIR, 'words.txt')
    coords = (37, 82, 152, 547)

    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    # pdf_to_images(PDF_PATH, IMAGES_DIR)
    # crop_image(INPUT_DIR, PROCESSED_IMAGES_DIR, coords)
    print(output_text_file)
    # process_images_to_text(PROCESSED_IMAGES_DIR, output_text_file)
    preprocess_text_from_file(output_text_file)

if __name__ == '__main__':
    main()
