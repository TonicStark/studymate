# Importing Libraries
import spacy
from collections import Counter
from heapq import nlargest
import math
import itertools

# Load Italian Language Model
nlp = spacy.load('it_core_news_sm')

# Get the text from a file
def get_text(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf8") as file:
            text = file.read()
        return text
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.") from e
    except IOError as e:
        raise IOError(f"An error occurred while reading the file: {str(e)}") from e
    
# Extract titles and paragraphs from the file content
def extract_title_and_paragraphs(file_content: str):
    lines = file_content.split('\n')
    main_title = ''
    paragraphs = {}

    current_title = ''
    current_paragraph = []

    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            if not main_title:
                main_title = line[1:]
            else:
                if current_paragraph:
                    paragraphs[current_title] = ' '.join(current_paragraph).strip()
                current_title = line[1:]
                current_paragraph = []
        elif line.startswith('##'):
            current_title = line[2:]
        elif current_title:
            current_paragraph.append(line)

    if current_title and current_paragraph:
        paragraphs[current_title] = ' '.join(current_paragraph).strip()

    # Remove '#' and space before each paragraph title
    paragraphs = {title.strip('# '): content for title, content in paragraphs.items()}

    return main_title, paragraphs
