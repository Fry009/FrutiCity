"""Reproducible toy-piano/marimba arrangements from public-domain Mutopia MIDI.
Requires numpy, mido and ffmpeg. No third-party sound recordings or soundfonts.
Keeps original MIDI and provenance; renders complete pieces, never tiny note loops.
"""
from pathlib import Path
import json, subprocess, urllib.request, wave
import xml.etree.ElementTree as ET
import mido
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'FrutiCity/Assets/FrutiCity/AudioSources'
WORK = ROOT / 'artifacts/audio'
OUT = ROOT / 'FrutiCity/Assets/FrutiCity/Resources/Audio'
SOURCE.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
TRACKS = [
    ('Marcha turca · Mozart', 'MozartWA/KV331/KV331_3_RondoAllaTurca/KV331_3_RondoAllaTurca'),
    ('Arabesca · Burgmüller', 'BurgmullerJFF/O100/25EF-02/25EF-02'),
    ('La caza · Burgmüller', 'BurgmullerJFF/O100/25EF-09/25EF-09'),
    ('La estiriana · Burgmüller', 'BurgmullerJFF/O100/25EF-14/25EF-14'),
]
RATE = 44100
report = []
for index, (name, remote) in enumerate(TRACKS):
    base = 'https://www.mutopiaproject.org/ftp/' + remote
    midi_path = SOURCE / f'classical_{index:02}.mid'
    rdf_path = SOURCE / f'classical_{index:02}.rdf'
    for ext, path in [('mid', midi_path), ('rdf', rdf_path)]:
        if not path.exists():
            path.write_bytes(urllib.request.urlopen(base + '.' + ext, timeout=30).read())
    meta = ET.fromstring(rdf_path.read_bytes())
    ns = {'mp': 'http://www.mutopiaproject.org/piece-data/0.1/'}
    assert meta.find('.//mp:licence', ns).text == 'Public Domain'
    now, active, notes = 0., {}, []
    for msg in mido.MidiFile(midi_path):
        now += msg.time
        if msg.type not in ('note_on', 'note_off'): continue
        key = (msg.channel, msg.note)
        if msg.type == 'note_on' and msg.velocity:
            active.setdefault(key, []).append((now, msg.velocity))
        elif key in active and active[key]:
            start, velocity = active[key].pop(0)
            notes.append((start, max(.035, now-start), msg.note, velocity))
    assert notes and not any(active.values()), 'Unmatched MIDI notes'
    # Remove the MIDI count-in, retain a short natural breath between whole pieces.
    offset = min(n[0] for n in notes)
    length = max(s+d for s,d,_,_ in notes) - offset + .65
    mix = np.zeros((int(length*RATE)+1, 2), dtype=np.float64)
    for start, duration, pitch, velocity in notes:
        t = np.arange(int((duration+.22)*RATE)) / RATE
        freq = 440 * 2 ** ((pitch-69)/12)
        attack = 1-np.exp(-t/.004)
        release = np.exp(-np.maximum(0,t-duration)/.05)
        # Rounded plucked keyboard: harmonic decay, no square waves or hard edges.
        voice = np.zeros_like(t)
        for harmonic, amplitude in [(1,1), (2,.32), (3,.12), (4,.065), (6,.018)]:
            if freq*harmonic >= RATE*.45: continue
            voice += amplitude*np.sin(2*np.pi*freq*harmonic*t)*np.exp(-t*(1.7+harmonic*1.3))
        voice *= attack * release * (velocity/127)**.65 * .23
        pan = np.clip(.5 + (pitch-65)/110, .22, .78)
        stereo = voice[:,None]*np.array([np.sqrt(1-pan), np.sqrt(pan)])
        pos = int((start-offset)*RATE)
        count = min(len(stereo), len(mix)-pos)
        mix[pos:pos+count] += stereo[:count]
    dry = mix.copy()
    for delay, gain in [(.047,.10),(.079,.07),(.113,.045)]:
        shift=int(delay*RATE)
        mix[shift:] += dry[:-shift, ::-1]*gain
    peak=float(np.max(np.abs(mix)))
    mix *= .85/max(peak, 1e-9)
    wav = WORK / f'classical_{index:02}.wav'
    with wave.open(str(wav),'wb') as stream:
        stream.setparams((2,2,RATE,0,'NONE','not compressed'))
        stream.writeframes((mix*32767).astype('<i2').tobytes())
    dest = OUT / f'classical_{index:02}.ogg'
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(wav),'-af',
        'loudnorm=I=-18:TP=-2:LRA=7','-ar',str(RATE),'-c:a','libvorbis','-q:a','5',str(dest)],check=True)
    report.append(dict(name=name, source=base+'.mid', licence='Public Domain',
        maintainer=meta.find('.//mp:maintainer',ns).text, seconds=round(length,2),
        notes=len(notes), midi_bytes=midi_path.stat().st_size, ogg_bytes=dest.stat().st_size))
    print(json.dumps(report[-1],ensure_ascii=False),flush=True)
(WORK/'sources.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
