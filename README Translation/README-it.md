# Studymate
Studymate è un software portatile che ti aiuta nello studio e nella memorizzazione.

## Set Up
### Localmente
Scarica la cartella ZIP o clona il repository con:
```
clone di git https://github.com/TonicStark/studymate.git
```

Quindi installa le dipendenze in un virtualenv puoi crearne una tramite `python -m venv <nome del virtualenv>` con:
```
pip install -r requirements.txt
```

Quando hai finito, puoi già utilizzare l'app semplicemente *attivando* il tuo virtualenv ed eseguendo:
```
streamlit run .\main.py
```

Questo avvierà un **server locale** sul tuo *computer* e un altro sulla **rete** (Wi-Fi se sei connesso) in modo che tu possa *accedere* da diversi dispositivi.

### Online
Per usare questa app online, visita semplicemente [studymate](https://studymate.streamlit.app/)!

## Sintassi e Formattazione
Per utilizzare questa app, devi fornire un file con una struttura e una sintassi specifiche, ad esempio:
``` md
# Titolo principale

## Sottotitolo 1
Paragrafo 1

## Sottotitolo 2
Paragrafo 2
ECC...
```

Fornisci un *titolo principale* e poi per ogni *sottotitolo*, il corrispondente *paragrafo* **(usando la sintassi `.md`)**.

# Goditelo
A questo punto puoi utilizzare l'app con la **semplicità** di cliccare un pulsante!