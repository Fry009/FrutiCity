"""Rehace de cero las tres entregas: portada, victoria y derrota.

Un solo comando, porque el proceso alterna dos interpretes y es facil
equivocarse de orden: las caras y las composiciones van con el Python del
sistema (necesitan PIL, que el Python de Blender NO trae) y los modelos y
los renders van con el de Blender.

    caras -> modelos -> esqueletos -> renders -> composicion

Uso:
    python hacer.py                # todo
    python hacer.py composicion    # solo rehacer portada y pantallas
    python hacer.py renders composicion

Las fases se pueden pedir sueltas porque `renders` es la lenta con
diferencia (unos minutos): son 80 fotogramas de las dos secuencias por
personaje, y no hace falta repetirla para mover un rotulo.
"""
import subprocess, sys, time
from pathlib import Path

# sin esto, al no haber terminal Python guarda la salida en el buffer y el
# log se queda vacio hasta el final: no hay forma de ver por donde va
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

HERE = Path(__file__).resolve().parent
V5 = HERE / 'fresita_v5'
QUIENES = ("fresi", "pablo", "nora")
ANIMADOS = ("fresi", "pablo")          # los que salen en victoria y derrota

FASES = ["caras", "modelos", "esqueletos", "renders", "composicion"]


def blender():
    for p in sorted(Path("C:/Program Files/Blender Foundation").glob("Blender */blender.exe"),
                    reverse=True):
        return str(p)
    raise SystemExit("no encuentro blender.exe")


def corre(cmd, titulo):
    t0 = time.time()
    print("\n== %s" % titulo, flush=True)
    r = subprocess.run(cmd, cwd=str(HERE), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stdout[-2500:])
        print(r.stderr[-1500:])
        raise SystemExit("fallo en: %s" % titulo)
    for linea in (r.stdout or "").splitlines():
        if linea.startswith(("[", "RENDER", "BLEND", "PORTADA", "TIRA")):
            print("   " + linea, flush=True)
    print("   (%.0f s)" % (time.time() - t0), flush=True)


def main():
    pedidas = [a for a in sys.argv[1:] if a in FASES] or FASES
    B = blender()
    py = sys.executable

    if "caras" in pedidas:
        corre([py, "caras_fresita.py"], "caras: sprites de expresion por personaje")

    if "modelos" in pedidas:
        corre([B, "--background", "--factory-startup", "--python", "frutis.py",
               "--", "todos"], "modelos: fresi, pablo y nora")

    if "esqueletos" in pedidas:
        for q in QUIENES:
            corre([B, "--background", str(V5 / ("%s.blend" % q)),
                   "--python", "fresita_rig.py"], "esqueleto de %s" % q)

    if "renders" in pedidas:
        for q in QUIENES:
            corre([B, "--background", str(V5 / ("%s_rig.blend" % q)),
                   "--python", "escenas.py", "--", "portada"],
                  "pose de portada de %s" % q)
        for q in ANIMADOS:
            corre([B, "--background", str(V5 / ("%s_rig.blend" % q)),
                   "--python", "escenas.py", "--", "victoria", "derrota"],
                  "secuencias de %s (lo lento)" % q)

    if "composicion" in pedidas:
        corre([py, "portada.py"], "portada 1080x1920")
        corre([py, "pantallas.py"], "pantallas de victoria y derrota")

    print("\nLISTO. Las entregas:")
    for r in (V5 / "portada_fruticity.png",
              V5 / "pantalla_victoria_fresi.gif", V5 / "pantalla_victoria_pablo.gif",
              V5 / "pantalla_derrota_fresi.gif", V5 / "pantalla_derrota_pablo.gif"):
        print("   %s %s" % ("OK " if r.exists() else "falta", r.name))


if __name__ == "__main__":
    main()
