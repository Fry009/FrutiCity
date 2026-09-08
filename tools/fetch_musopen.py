"""Banda sonora desde las grabaciones del Kickstarter de Musopen (archive.org, CC0).

Son interpretaciones reales de orquesta, cuarteto y piano: nada de MIDI. Los MIDI de
Mutopia venian de partituras grabadas con LilyPond y traian TODAS las notas a velocidad
90, sin un solo acento, que es exactamente por lo que sonaban a politono.

Cada pista se recorta a un extracto que aguante en bucle, se normaliza y se guarda en OGG.
Requiere ffmpeg. El item de origen esta dedicado a dominio publico bajo CC0 1.0.
"""
from pathlib import Path
import json, subprocess, sys, time, urllib.parse, urllib.request

# Los nombres llevan tildes y una 'r' checa: sin esto, escribir el informe revienta en
# cuanto la salida va a un fichero con la consola en cp1252.
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'artifacts/musopen'
OUT = ROOT / 'FrutiCity/Assets/FrutiCity/Resources/Audio'
ITEM = 'MusopenKickstarterRecordings'
ZIP = 'https://archive.org/download/' + ITEM + '/Musopen%20DVD.zip/'
LICENCE = 'https://creativecommons.org/publicdomain/zero/1.0/'
WORK.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

# (destino, nombre en el juego, carpeta/fichero dentro del DVD, segundo de inicio, duracion)
MENU = ('menu_theme', 'Las bodas de Fígaro · Mozart',
        'Mozart - Marriage Of Figaro/Marriage of Figaro.mp3', 6, 122)
TRACKS = [
    ('Sinfonía nº 40 · Mozart', 'Mozart - Symphony No 40 in G Minor /1st Mov Molto allegro.mp3', 0, 118),
    ('En la cueva del rey · Grieg', 'Grieg - Peer Gynt/Peer Gynt Suite No. 1, Op. 46 - IV. In the Hall Of The Mountain King.mp3', 0, 132),
    ('Mañana · Grieg', 'Grieg - Peer Gynt/Peer Gynt Suite No. 1, Op. 46 - I. Morning.mp3', 0, 124),
    ('La flauta mágica · Mozart', 'Mozart - Magic Flute Overture/Magic Flute Overture.mp3', 12, 118),
    ('Egmont · Beethoven', 'Beethoven - Egmont Overture Op. 84/Egmont Overture Op. 84.mp3', 0, 122),
    ('Heroica · Beethoven', 'Beethoven - Symphony No 3 Eroica/Symphony No. 3 in E Flat Major Eroica, Op. 55 - I. Allegro con brio.mp3', 0, 120),
    ('El Moldava · Smetana', 'Smetana - Vltava/Ma Vlast (My Fatherland) - Vltava.mp3', 55, 126),
    ('Sinfonía italiana · Mendelssohn', "Mendelssohn - Italian Symphony/Symphon No. 4 in A Major, Op. 90 'Italian' - I. Allegro vivace.mp3", 2, 118),
    ('Las Hébridas · Mendelssohn', "Mendelssohn - Hebrides/Hebrides Overture Fingal's Cave.mp3", 0, 124),
    ('Sinfonía nº 3 · Brahms', 'Brahms - Symphony No 3/Symphony No. 3 in F Major, Op. 90 - III. Poco allegretto.mp3', 0, 120),
    ('Aria Goldberg · Bach', 'Goldberg Variations/Goldberg Variations, BWV 988 - Aria.mp3', 0, 110),
    ('Cuarteto Americano · Dvořák', 'String Quartets/Dvorak - American in F major/String Quartet No. 12 in F Major, Op. 96, American - III. Molto Vivace.mp3', 2, 112),
]

def fetch(inner):
    # archive.org corta con 503 si se le piden varios trozos del ZIP seguidos: se espera y se
    # reintenta, y lo ya bajado se reutiliza para poder retomar donde lo dejo.
    cache = WORK / inner.replace('/', '_')
    if cache.exists() and cache.stat().st_size > 0:
        return cache
    url = ZIP + urllib.parse.quote('Musopen DVD/' + inner, safe='')
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for attempt in range(8):
        try:
            cache.write_bytes(urllib.request.urlopen(request, timeout=900).read())
            return cache
        except Exception as error:
            print('reintento %d de %s: %s' % (attempt + 1, cache.name[:40], error), flush=True)
            time.sleep(20 * (attempt + 1))
    raise SystemExit('No se pudo bajar ' + inner)

def encode(source, destination, start, length):
    # Fundido de entrada y de salida: el extracto tiene que poder repetirse sin dar un salto.
    filters = ('afade=t=in:st=0:d=1.5,afade=t=out:st=%s:d=3.5,'
               'loudnorm=I=-17:TP=-2:LRA=9' % (length - 3.5))
    # -vn y -map_metadata -1 son obligatorios: los MP3 traen caratula, y sin esto ffmpeg la
    # copia como pista de video Theora dentro del OGG. Unity importa ese fichero con
    # "FSBTool ERROR: Internal error from FMOD sub-system" y el clip se queda en null.
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(start), '-t', str(length),
                    '-i', str(source), '-vn', '-map_metadata', '-1', '-af', filters,
                    '-ar', '44100', '-ac', '2',
                    '-c:a', 'libvorbis', '-q:a', '3', str(destination)], check=True)

report = []
for index, (name, inner, start, length) in enumerate([(MENU[1], MENU[2], MENU[3], MENU[4])] +
                                                     [(n, p, s, l) for n, p, s, l in TRACKS]):
    stem = 'menu_theme' if index == 0 else 'classical_%02d' % (index - 1)
    source = fetch(inner)
    destination = OUT / (stem + '.ogg')
    encode(source, destination, start, length)
    report.append(dict(name=name, file=stem, seconds=length, licence=LICENCE,
                       source='https://archive.org/details/' + ITEM, inside=inner,
                       ogg_bytes=destination.stat().st_size))
    print(json.dumps(report[-1], ensure_ascii=False), flush=True)
(WORK / 'sources.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('TOTAL KB', sum(r['ogg_bytes'] for r in report) // 1024)
