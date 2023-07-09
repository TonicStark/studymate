# Studymate
Studymate is a portable piece of software that helps you with studying and memorization.

## Set Up
### Locally
Download the ZIP Folder, or Clone the Repository with:
```
git clone https://github.com/TonicStark/studymate.git
```

Then install the dependencies in a virtualenv you can create one via `python -m venv <name of the virtualenv>` with:
```python
pip install -r requirements.txt
```

When you are done with this, you can already use the app by simply *activating* your virtualenv and running:
```
streamlit run .\main.py
```

This will start a **local server** on your *computer*, and another one on the **network** (Wi-Fi if you're connected) so that you can *access* from different devices.

### Online
To use this app online, simply visit [studymate](https://studymate.streamlit.app/)!

## Format
To use this app, you need to provide a file with a specific structure and syntax, for example:
```md
# Main Title
## Subtitle 1
Paragraph 1
## Subtitle 2
Paragraph 2
ECC...
```

You provide a *main title* and then for each *subtitle*, the correspondent *paragraph* **(all using `.md` syntax)**.

# Enjoy it
At this point you can use the app with the **simplicity** of clicking a button!