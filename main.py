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