# [📡 Juego de Morse — jugar online](https://yagoestudios.github.io/morse-juego/)

Aprende código Morse en español: una baraja de Anki con audio y un juego web para practicar al oído.

## Jugar

👉 **[yagoestudios.github.io/morse-juego](https://yagoestudios.github.io/morse-juego/)**

Escucha el pitido y escribe la frase. Ajusta la velocidad (PPM) para subir la dificultad; el tiempo disponible escala con la velocidad y siempre da un margen extra. 44 frases con palabras comunes en español. Acentos y ñ se ignoran al comparar.

- ▶ Empezar / Siguiente · 🔁 Repetir · ⏭ Saltar · `Enter` comprueba.
- Audio sintetizado con Web Audio (tono de 600 Hz), por eso la velocidad es variable.

## Baraja de Anki

En [`anki/`](anki/): `Codigo_Morse.apkg` (26 letras A-Z, cada una con su audio en Morse). Ábrelo con doble clic o *File → Import* en Anki.

Para regenerarla:

```bash
pip install genanki
python anki/build_deck.py
```

Ajusta velocidad (`UNIT`), tono (`FREQ`) o añade caracteres editando `build_deck.py`.
