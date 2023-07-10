# Importing Libraries
import spacy
from collections import Counter
from heapq import nlargest
import math
import itertools
import streamlit as st
from io import StringIO

# Load Italian Language Model
nlp = spacy.load('it_core_news_sm')

# Extract titles and paragraphs from the file content


def extract_title_and_paragraphs(file_content: str) -> tuple[str, dict]:
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
                    paragraphs[current_title] = ' '.join(
                        current_paragraph).strip()
                current_title = line[1:]
                current_paragraph = []
        elif line.startswith('##'):
            current_title = line[2:]
        elif current_title:
            current_paragraph.append(line)

    if current_title and current_paragraph:
        paragraphs[current_title] = ' '.join(current_paragraph).strip()

    # Remove '#' and space before each paragraph title
    paragraphs = {
        title.strip('# '): content for title,
        content in paragraphs.items()}

    return main_title, paragraphs

# Summarize a given text using TF-IDF


def summarize(text: str, perc: int) -> str:
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
    divisor = 100 // perc
    num_summarized_sents = len(list(doc.sents)) // divisor

    # Get the top n sentences with the highest strength
    summarized_sentences = nlargest(
        num_summarized_sents,
        sent_strength,
        key=sent_strength.get)

    return ' '.join([sent.text.strip() for sent in summarized_sentences])

# Estimate the Average reading time


def reading_time(text: str) -> int:
    # Using an average silent reading time in words per minute
    avg_read_speed = 200

    # Calculate the number of words
    wordcount = len(text.split())

    return math.ceil(wordcount / avg_read_speed)


# Main Program
if __name__ == "__main__":

    # Modifiyng App name and icon
    st.set_page_config(
        page_title='Studymate',
        page_icon="favicon.ico",
        layout="wide")

    # Title of the Program
    st.title("Studymate")

    # Asking to input a file
    file = st.file_uploader(
        ".", ["md", "txt"], False, label_visibility="hidden")

    # Creating a slider for managing the amount of summarization
    perc_slider = st.select_slider(
        "Select the precentage (%) of the summary",
        (10,
         20,
         30,
         40,
         50,
         60,
         70,
         80,
         90),
        50)

    # Checking and executing only if a file is uploaded
    if file is not None:

        # Starting a Spinner while executing the summarization
        with st.spinner("Summarizing..."):

            # Extract text from test file
            stringio = StringIO(file.getvalue().decode("utf-8"))
            text = stringio.read()

            # Calculate the time it takes to read
            original_rtime = reading_time(text)

            # Extract parts of the text
            MAIN_TITLE, paragraphs = extract_title_and_paragraphs(text)

            # Summarize each paragraph
            for key in paragraphs.keys():
                paragraphs[key] = summarize(paragraphs[key], perc_slider)

            # Create a new unique file string to calculate final reading time
            final_string = MAIN_TITLE
            for title, paragraph in paragraphs.items():
                final_string += f"\n{title}\n{paragraph}"
            final_rtime = reading_time(final_string)

            # Calculate % improvement on time
            improvment = round(100 - (final_rtime * 100) / original_rtime)

        # Displaying text in the Web App
        col1, col2 = st.columns(2, gap="large")
        col1.header(MAIN_TITLE)
        col2.metric(
            "Reading Time",
            f"{final_rtime} min",
            f"{improvment}%" if improvment != 0 else "",
            "inverse" if improvment != 0 else "off")
        for subheader, paragraph in paragraphs.items():

            # Checking if the paragraph content exist
            if paragraph:
                st.subheader(subheader)
                st.write(paragraph)
