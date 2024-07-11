# Talking Avatar

Ein interaktives Python-Projekt, das einen sprechenden Avatar verwendet, um Witze zu erzählen, Musik abzuspielen und Grüße auszugeben. Der Avatar spricht Begrüßungstexte, wenn er angeklickt wird, und bietet verschiedene Optionen über Schaltflächen.

## Anforderungen

- Python 3.x
- Pygame
- gTTS (Google Text-to-Speech)

## Installation

1. Installieren Sie die erforderlichen Python-Bibliotheken:

   ```sh
   pip install pygame gtts
   ```

2. Platzieren Sie die folgenden Dateien im gleichen Verzeichnis wie Ihr Python-Skript:

   - `avatar_closed.png`
   - `avatar_half_open.png`
   - `avatar_open.png`
   - `background.mp3`
   - `content.txt`

3. Erstellen Sie die Datei `content.txt` mit folgendem Inhalt:

   ```txt
   # Witze
   Warum können Geister so schlecht lügen? Weil man durch sie hindurchsehen kann.
   Warum dürfen Geister keine Lügen erzählen? Weil man sie durchschauen kann.

   # Musiktitel
   background.mp3
   new_background.mp3

   # Grüße
   Hallo zusammen!
   Schönen Tag euch allen!

   # Hello
   Mein Name ist Sahra.
   Ich bin ein sprechender Avatar.
   Wie kann ich dir helfen?
   ```

## Nutzung

1. Führen Sie das Python-Skript aus:

   ```sh
   python talking_avatar.py
   ```

2. Klicken Sie auf den Avatar, um Begrüßungstexte in der Reihenfolge abzuspielen.

3. Verwenden Sie die Schaltflächen am unteren Rand des Bildschirms, um verschiedene Aktionen auszuführen:
   - Erzähle einen zufälligen Witz
   - Spiele andere Musik
   - Gruß in die Runde
   - Beenden
