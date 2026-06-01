#!/usr/bin/env python3
"""Genera una baraja de Anki (.apkg) para aprender codigo Morse, con audio."""
import math
import os
import struct
import wave

import genanki

MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
}

# Parametros de audio
FRAMERATE = 44100
FREQ = 600          # Hz del tono
UNIT = 0.09         # duracion de un "dit" en segundos
AMP = 0.5           # amplitud (0-1)

MEDIA_DIR = os.path.join(os.path.dirname(__file__), "media")


def tone(duration):
    n = int(FRAMERATE * duration)
    frames = []
    for i in range(n):
        # fade in/out de 3ms para evitar clicks
        env = 1.0
        fade = int(FRAMERATE * 0.003)
        if i < fade:
            env = i / fade
        elif i > n - fade:
            env = (n - i) / fade
        v = AMP * env * math.sin(2 * math.pi * FREQ * i / FRAMERATE)
        frames.append(int(v * 32767))
    return frames


def silence(duration):
    return [0] * int(FRAMERATE * duration)


def morse_samples(code):
    dit = tone(UNIT)
    dah = tone(UNIT * 3)
    intra = silence(UNIT)          # gap entre simbolos de una letra
    samples = []
    for i, sym in enumerate(code):
        if i:
            samples += intra
        samples += dit if sym == "." else dah
    return samples


def write_wav(path, samples):
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(FRAMERATE)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))


def main():
    os.makedirs(MEDIA_DIR, exist_ok=True)
    media_files = []
    for ch, code in MORSE.items():
        fname = f"morse_{ch}.wav"
        fpath = os.path.join(MEDIA_DIR, fname)
        write_wav(fpath, morse_samples(code))
        media_files.append(fpath)

    model = genanki.Model(
        1607392319,
        "Morse",
        fields=[
            {"name": "Caracter"},
            {"name": "Codigo"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Caracter -> Morse",
                "qfmt": '<div class="big">{{Caracter}}</div>',
                "afmt": '{{FrontSide}}<hr id="answer">'
                        '<div class="morse">{{Codigo}}</div>{{Audio}}',
            },
            {
                "name": "Sonido -> Caracter",
                "qfmt": '<div class="morse">&#9835;</div>{{Audio}}',
                "afmt": '{{FrontSide}}<hr id="answer">'
                        '<div class="big">{{Caracter}}</div>'
                        '<div class="morse">{{Codigo}}</div>',
            },
        ],
        css=""".card{font-family:Arial;text-align:center;background:#1e1e1e;color:#eee}
.big{font-size:120px;font-weight:bold}
.morse{font-size:48px;letter-spacing:8px;color:#4fc3f7}""",
    )

    deck = genanki.Deck(2059400110, "Codigo Morse")
    for ch, code in MORSE.items():
        deck.add_note(genanki.Note(
            model=model,
            fields=[ch, code, f"[sound:morse_{ch}.wav]"],
        ))

    pkg = genanki.Package(deck)
    pkg.media_files = media_files
    out = os.path.join(os.path.dirname(__file__), "Codigo_Morse.apkg")
    pkg.write_to_file(out)
    print(f"OK -> {out} ({len(MORSE)} tarjetas, {len(media_files)} audios)")


if __name__ == "__main__":
    main()
