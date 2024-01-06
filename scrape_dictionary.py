import requests
import os
from tqdm import tqdm  

def handle_paths():
    SCRIPT_PATH = os.path.abspath(__file__)
    SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)

    return SCRIPT_DIR

def get_definitions_and_examples(word):
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            definitions = data[0]['meanings'][0]['definitions']
            examples = [definition.get('example') for definition in definitions if 'example' in definition]
            examples = examples[:3]  # Get up to three examples
            return definitions[0]['definition'], examples
        else:
            return None, []
    except requests.RequestException as e:
        print(f"Error fetching data for word '{word}': {e}")
        return None, []

def read_words_from_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass  # Creates an empty file
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def write_results_to_file(file_path, results):
    with open(file_path, 'w') as file:
        for word, (definition, examples) in results.items():
            if definition:
                file.write(f"Word: {word}\nDefinition: {definition}\n")
                for i, example in enumerate(examples, 1):
                    if example:
                        file.write(f"Example {i}: {example}\n")
                file.write("\n")

def main():
    SCRIPT_DIR = handle_paths()
    EXTRACTED_TEXT = os.path.join(SCRIPT_DIR, 'extracted_text')

    if not os.path.exists(EXTRACTED_TEXT):
        os.makedirs(EXTRACTED_TEXT)  

    input_file_path = os.path.join(EXTRACTED_TEXT, 'output.txt')
    output_file_path = os.path.join(EXTRACTED_TEXT, 'output_definitions_and_examples_02.txt')

    words = read_words_from_file(input_file_path)

    results = {}
    for word in tqdm(words, desc="Processing Words"):
        result = get_definitions_and_examples(word)
        results[word] = result

    write_results_to_file(output_file_path, results)

if __name__ == '__main__':
    main()