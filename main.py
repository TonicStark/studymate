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

# Summarize a given text using TF-IDF
def summarize(text: str) -> str:
    doc = nlp(text)

    # Define the desired POS tags
    pos_tags = {'PROPN', 'ADJ', 'NOUN', 'VERB'}
    # Extract keywords based on the desired POS tags
    keywords = [token.text for token in doc if token.pos_ in pos_tags]

    # Count the frequency of each keyword
    freq_words = Counter(keywords)

    # Find the maximum frequency
    max_freq = max(freq_words.values())

    # Normalize the frequencies of keywords
    freq_words = {word: freq / max_freq for word, freq in freq_words.items()}

    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_words:
                # Calculate the sentence strength based on the frequency of
                # keywords
                sent_strength.setdefault(sent, 0)
                sent_strength[sent] += freq_words[word.text]

    # Calculate the number of sentences to reduce the summary to
    num_summarized_sents = len(list(doc.sents)) // 2

    # Get the top n sentences with the highest strength
    summarized_sentences = nlargest(
        num_summarized_sents,
        sent_strength,
        key=sent_strength.get)

    return ' '.join([sent.text.strip() for sent in summarized_sentences])