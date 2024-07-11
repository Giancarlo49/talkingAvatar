import time
import pygame
from gtts import gTTS
import random  # Import der random-Bibliothek für zufällige Auswahl

# Initialisierung von Pygame und Pygame Mixer
pygame.init()
pygame.mixer.init()

# Laden der Avatar-Bilder
avatar_closed = pygame.image.load('avatar_closed.png')
avatar_half_open = pygame.image.load('avatar_half_open.png')
avatar_open = pygame.image.load('avatar_open.png')

# Fenstergröße und Initialisierung
size = width, height = 840, 580
screen = pygame.display.set_mode(size)
black = 0, 0, 0
white = (255, 255, 255)
gray = (169, 169, 169)
button_color = (70, 130, 180)
button_hover_color = (100, 149, 237)

# Avatar-Bilder und Rechteck
avatar_images = [avatar_closed, avatar_half_open, avatar_open]
current_avatar_index = 0
avatar_rect = avatar_images[current_avatar_index].get_rect()

# Skalierung des Bildes, falls es größer als das Fenster ist
if avatar_rect.width > width or avatar_rect.height > height:
    for i in range(len(avatar_images)):
        avatar_images[i] = pygame.transform.scale(avatar_images[i], (width // 2, height // 2))
    avatar_rect = avatar_images[current_avatar_index].get_rect()
avatar_rect.center = (width // 2, height // 2)

# Zeitverzögerung zwischen den Bildwechseln (0.2 Sekunden)
change_interval = 0.2  # in Sekunden
last_change_time = time.time()

# Texte aus der Datei laden
def load_content(file_path):
    jokes = []
    music_files = []
    greetings = []
    hellos = []  # Neue Liste für 'hello'-Sätze
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().splitlines()
        section = None
        for line in content:
            if line.startswith('# Witze'):
                section = 'jokes'
            elif line.startswith('# Musiktitel'):
                section = 'music'
            elif line.startswith('# Grüße'):
                section = 'greetings'
            elif line.startswith('# Hello'):
                section = 'hellos'  # Neue Sektion für 'hello'
            elif line.strip() == '':
                section = None
            elif section == 'jokes':
                jokes.append(line)
            elif section == 'music':
                music_files.append(line)
            elif section == 'greetings':
                greetings.append(line)
            elif section == 'hellos':
                hellos.append(line)  # Zeile zur 'hellos'-Liste hinzufügen
    return jokes, music_files, greetings, hellos

jokes, music_files, greetings, hellos = load_content('content.txt')

# Hintergrundmusik laden und abspielen
background_channel = pygame.mixer.Channel(1)
background_music = pygame.mixer.Sound(music_files[0])  # Standard-Hintergrundmusik
background_channel.play(background_music, loops=-1)
background_channel.set_volume(0.2)

# Text-to-Speech Funktion mit gTTS und Pygame Mixer
def speak(text):
    global last_change_time, current_avatar_index  # Zugriff auf die globalen Variablen
    tts = gTTS(text=text, lang='de')  # Verwenden Sie 'de' für Deutsch
    tts.save("output.mp3")

    # MP3-Datei mit Pygame Mixer abspielen
    speech_channel = pygame.mixer.Channel(0)
    speech_sound = pygame.mixer.Sound("output.mp3")
    speech_channel.play(speech_sound)

    # Initialisierung von last_change_time, falls es noch nicht initialisiert wurde
    if 'last_change_time' not in globals():
        last_change_time = time.time()

    # Warten, bis die Wiedergabe beendet ist
    while speech_channel.get_busy():
        pygame.time.Clock().tick(10)

        # Zeit für den Bildwechsel überprüfen
        if time.time() - last_change_time > change_interval:
            current_avatar_index = (current_avatar_index + 1) % len(avatar_images)
            last_change_time = time.time()
        screen.fill(black)
        screen.blit(avatar_images[current_avatar_index], avatar_rect)
        pygame.display.flip()

# Funktion, um neue Hintergrundmusik zu spielen
def play_new_music(music_file):
    background_channel.stop()
    new_music = pygame.mixer.Sound(music_file)
    background_channel.play(new_music, loops=-1)
    background_channel.set_volume(0.2)

# Funktion für zufälligen Witz
def get_random_joke():
    return random.choice(jokes)

# Funktion für zufälligen Gruß
def get_random_greeting():
    return random.choice(greetings)

def get_random_hello():
    return random.choice(hellos)

# Schaltflächen erstellen
button_font = pygame.font.Font(None, 20)
button_texts = ["Erzähle einen zufälligen Witz", "Spiele andere Musik", "Gruß in die Runde", "Beenden"]
buttons = []

# Schaltflächenposition und -größe
button_width = 200
button_height = 40
button_margin = 10
button_y = height - button_height - 10
button_x_start = (width - (button_width + button_margin) * len(button_texts) + button_margin) // 2
for i, text in enumerate(button_texts):
    button_x = button_x_start + i * (button_width + button_margin)
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    buttons.append((text, button_rect))

# Hauptschleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if avatar_rect.collidepoint(event.pos):
                speak(get_random_hello())  # Zufälligen 'hello'-Satz abspielen
            for i, (text, button_rect) in enumerate(buttons):
                if button_rect.collidepoint(event.pos):
                    if i == 0:
                        speak(get_random_joke())  # Zufälligen Witz abspielen
                    elif i == 1:
                        play_new_music(random.choice(music_files))  # Zufällige Musik abspielen
                    elif i == 2:
                        speak(get_random_greeting())  # Zufälligen Gruß abspielen
                    elif i == 3:
                        running = False
    screen.fill(black)
    screen.blit(avatar_images[current_avatar_index], avatar_rect)
    for text, button_rect in buttons:
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, button_rect)
        else:
            pygame.draw.rect(screen, button_color, button_rect)
        button_text = button_font.render(text, True, white)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)
    pygame.display.flip()

# Beenden von Pygame
pygame.quit()
