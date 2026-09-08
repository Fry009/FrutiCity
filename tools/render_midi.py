"""Convierte los MIDI de Assets/Audio/MIDI en las pistas del juego.

Estos MIDI si son interpretaciones: traen entre 11 y 123 intensidades distintas por
pieza. Los de Mutopia traian UNA sola (velocidad 90 en todas las notas), y por eso
sonaban a politono por muy bien que se sintetizaran.

El sintetizador de aqui es lo que aprovecha ese matiz:

- Envolvente con sostenido de verdad. La version vieja apagaba cada nota nada mas
  tocarla, asi que daba igual lo larga que fuese: todo sonaba a pulsacion de timbre.
- Brillo por intensidad, no solo volumen. Tocar fuerte abre el timbre, que es lo que
  hace que un acento se OIGA como acento.
- Papel por pista: la voz mas aguda lleva mas armonicos y se pone al frente; el
  acompanamiento va mas oscuro y mas abierto en el estereo.
- Cuerdas ligeramente desafinadas entre si y vibrato en las notas largas: sin eso, un
  acorde suena a organo de juguete.
- Reverberacion de siete tomas con cruce de canales, y saturacion suave al final para
  pegarlo todo.

Requiere numpy, mido y ffmpeg.
"""
from pathlib import Path
import json, subprocess, sys
import mido
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]
FUENTE = ROOT / 'Assets/Audio/MIDI'
WORK = ROOT / 'artifacts/midi'
OUT = ROOT / 'FrutiCity/Assets/FrutiCity/Resources/Audio'
WORK.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

RATE = 44100
MAX_SEGUNDOS = 150.0
PERCUSION = 9          # el canal 10 del estandar: ahi el numero de nota es un tambor

# (nombre en el juego, fichero, segundo de entrada)
PISTAS = [
    ('Pequeña serenata nocturna · Mozart', 'Eine Kleine Nachtmusik - Mozart.mid', 0),
    ('Marcha turca · Mozart', 'Rondo Alla Turca - Mozart.mid', 0),
    ('Himno de la alegría · Beethoven', 'Ode to Joy - Beethoven.mid', 0),
    ('Primavera · Vivaldi', 'Primavera - Vivaldi 1st mov.mid', 0),
    ('Otoño · Vivaldi', 'Otono - Vivaldi 1st mov.mid', 0),
    ('Danza del hada · Chaikovski', 'Dance of the Sugar Plum Fairy - Tchaikovsky.mid', 0),
    ('Danza de los duendes · Grieg', 'Danza de los Duendes - Grieg.mid', 0),
    ('Badinerie · Bach', 'Badinerie (Suite Orchestral No. 2) - Bach.mid', 0),
    ('Minueto en sol · Bach', 'Minuet in G - Bach-Petzold.mid', 0),
    ('Minueto · Boccherini', 'Minuet - Boccherini.mid', 0),
    ('Cakewalk · Debussy', 'Golliwogs Cakewalk - Debussy.mid', 0),
    ('El elefante · Saint-Saëns', 'The Elephant - Saint-Saens.mid', 0),
]


def leer(path):
    """Notas emparejadas (inicio, duracion, altura, intensidad, canal)."""
    activas, notas = {}, []
    ahora = 0.0
    for msg in mido.MidiFile(path):
        ahora += msg.time
        if msg.type not in ('note_on', 'note_off'):
            continue
        if msg.channel == PERCUSION:
            continue
        clave = (msg.channel, msg.note)
        if msg.type == 'note_on' and msg.velocity:
            activas.setdefault(clave, []).append((ahora, msg.velocity))
        elif activas.get(clave):
            inicio, velocidad = activas[clave].pop(0)
            notas.append((inicio, max(.05, ahora - inicio), msg.note, velocidad, msg.channel))
    return notas


def voz(duracion, freq, loud, papel, rng):
    """Una nota. Devuelve la onda mono ya con su envolvente."""
    cola = .42
    n = int((duracion + cola) * RATE)
    t = np.arange(n) / RATE
    brillo = .35 + .65 * loud
    ataque = .004 + .014 * (1 - loud)
    piso = .52 if papel == 'melodia' else .40
    env = np.clip(t / ataque, 0, 1)
    env *= piso + (1 - piso) * np.exp(-t / (.60 if papel == 'melodia' else .95))
    env *= np.exp(-np.maximum(0, t - duracion) / .13)
    # Vibrato solo en lo que dura: en notas cortas no da tiempo ni a oirse.
    vibrato = .0026 * np.sin(2 * np.pi * 5.4 * t) * np.clip((t - .28) / .45, 0, 1)
    onda = np.zeros(n)
    armonicos = 11 if papel == 'melodia' else 7
    for h in range(1, armonicos + 1):
        f = freq * h
        if f > RATE * .45:
            break
        amp = h ** -(2.15 - .95 * brillo)
        if h % 2 == 0:
            amp *= .74
        # Los agudos se apagan antes que el fundamental, como en cualquier cuerda.
        amortigua = .34 + .66 * np.exp(-t * (.55 + .48 * h))
        desafina = 1 + (rng.random() - .5) * .0013
        onda += amp * amortigua * np.sin(2 * np.pi * f * desafina * (t + vibrato))
    golpe = int(.018 * RATE)
    onda[:golpe] += rng.standard_normal(golpe) * np.exp(-np.arange(golpe) / (.0035 * RATE)) * .04
    return onda * env * loud * .17


def render(path, salida, nombre, desde):
    notas = leer(path)
    if not notas:
        raise SystemExit('sin notas: ' + str(path))
    origen = min(n[0] for n in notas)
    notas = [(s - origen - desde, d, p, v, c) for s, d, p, v, c in notas]
    notas = [n for n in notas if n[0] >= 0 and n[0] < MAX_SEGUNDOS]
    # La voz mas aguda de la pieza lleva la melodia: se le da brillo y el centro.
    alturas = {}
    for _, _, p, _, c in notas:
        alturas.setdefault(c, []).append(p)
    medias = {c: sum(v) / len(v) for c, v in alturas.items()}
    principal = max(medias, key=medias.get) if medias else None
    largo = min(MAX_SEGUNDOS, max(s + d for s, d, _, _, _ in notas) + .8)
    mezcla = np.zeros((int(largo * RATE) + RATE, 2))
    rng = np.random.default_rng(20260908)
    for inicio, duracion, altura, velocidad, canal in notas:
        papel = 'melodia' if canal == principal else 'fondo'
        freq = 440 * 2 ** ((altura - 69) / 12)
        onda = voz(min(duracion, 6.0), freq, (velocidad / 127) ** .75, papel, rng)
        pan = np.clip(.5 + (altura - 64) / 130 + (0 if papel == 'melodia' else (canal % 5 - 2) * .06), .18, .82)
        if papel != 'melodia':
            onda *= .82
        estereo = onda[:, None] * np.array([np.sqrt(1 - pan), np.sqrt(pan)])
        pos = int(inicio * RATE)
        cuenta = min(len(estereo), len(mezcla) - pos)
        if cuenta > 0:
            mezcla[pos:pos + cuenta] += estereo[:cuenta]
    seco = mezcla.copy()
    for retardo, ganancia in [(.023, .15), (.037, .12), (.053, .095), (.079, .075),
                              (.113, .055), (.157, .04), (.211, .026)]:
        desplaza = int(retardo * RATE)
        mezcla[desplaza:] += seco[:-desplaza, ::-1] * ganancia
    pico = float(np.max(np.abs(mezcla)))
    mezcla *= .82 / max(pico, 1e-9)
    mezcla = np.tanh(mezcla * 1.25) / 1.25
    wav = WORK / (salida + '.wav')
    import wave
    with wave.open(str(wav), 'wb') as flujo:
        flujo.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
        flujo.writeframes((np.clip(mezcla, -1, 1) * 32767).astype('<i2').tobytes())
    destino = OUT / (salida + '.ogg')
    fin = max(2.0, largo - 3.5)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(wav), '-vn', '-map_metadata', '-1',
                    '-af', 'afade=t=in:st=0:d=1.2,afade=t=out:st=%.2f:d=3.5,loudnorm=I=-17:TP=-2:LRA=9' % fin,
                    '-ar', str(RATE), '-ac', '2', '-c:a', 'libvorbis', '-q:a', '3', str(destino)], check=True)
    return dict(name=nombre, file=salida, seconds=round(largo, 1), notes=len(notas),
                source=path.name, ogg_bytes=destino.stat().st_size)


if __name__ == '__main__':
    informe = []
    for indice, (nombre, fichero, desde) in enumerate(PISTAS):
        informe.append(render(FUENTE / fichero, 'classical_%02d' % indice, nombre, desde))
        print(json.dumps(informe[-1], ensure_ascii=False), flush=True)
    (WORK / 'sources.json').write_text(json.dumps(informe, ensure_ascii=False, indent=2), encoding='utf-8')
    print('TOTAL KB', sum(r['ogg_bytes'] for r in informe) // 1024)
