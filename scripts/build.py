"""Genera mis_canales_es.m3u8 a partir de la tabla publica de TDTChannels (canales en abierto de Espana).

- Si un canal tiene varios enlaces, usa el primero que responda (si no responde ninguno, deja el primero).
- quitar.txt: nombres de canales a excluir, uno por linea (las lineas con # se ignoran).
- extra.m3u8: canales propios que se anaden al final de la lista.
"""
import os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

SRC_URL = "https://raw.githubusercontent.com/LaQuay/TDTChannels/master/TELEVISION.md"
EPG = "https://www.tdtchannels.com/epg/TV.xml.gz"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
STOP_AT = "Int. Europa"  # a partir de aqui son canales internacionales
dst = sys.argv[1] if len(sys.argv) > 1 else "mis_canales_es.m3u8"
CHECK = os.environ.get("NO_CHECK") != "1"

def norm(s):
    return s.strip().lower()

quitar = set()
if os.path.exists("quitar.txt"):
    quitar = {norm(l) for l in open("quitar.txt", encoding="utf-8") if l.strip() and not l.lstrip().startswith("#")}

def works(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=10) as r:
            head = r.read(2048)
            ctype = r.headers.get("Content-Type", "").lower()
            return b"#EXTM3U" in head or b"<MPD" in head or "mpegurl" in ctype or "video" in ctype
    except Exception:
        return False

def pick(links):
    if CHECK and len(links) > 1:
        for u in links:
            if works(u):
                return u
    return links[0]

lines = urllib.request.urlopen(SRC_URL, timeout=60).read().decode("utf-8").splitlines()
channels, group, sub = [], None, None
for l in lines:
    if l.startswith("## "):
        group, sub = l[3:].strip(), None
        if group == STOP_AT:
            break
        continue
    if l.startswith("### "):
        sub = l[4:].strip(); continue
    if not l.startswith("| ") or l.startswith("| Canal") or l.startswith("| -"):
        continue
    cols = [c.strip() for c in l.strip("|").split(" | ")]
    if len(cols) < 5:
        continue
    name, m3u, _web, logo, epg = cols[:5]
    links = re.findall(r'\[m3u8[^\]]*\]\((https?://[^)]+)\)', m3u)
    if not links or norm(name) in quitar:
        continue
    lg = re.search(r'\((https?://[^)]+)\)', logo)
    g = f"Autonómicos - {sub}" if group == "Autonómicos" and sub else group
    channels.append((name, links, lg.group(1) if lg else "", "" if epg == "-" else epg, g))

if len(channels) < 50:
    sys.exit(f"Solo {len(channels)} canales: algo ha fallado, no se sobrescribe")

with ThreadPoolExecutor(20) as ex:
    urls = list(ex.map(lambda c: pick(c[1]), channels))

out = [f'#EXTM3U url-tvg="{EPG}" x-tvg-url="{EPG}"']
alt = 0
for (name, links, logo, epg, g), url in zip(channels, urls):
    alt += url != links[0]
    out.append(f'#EXTINF:-1 tvg-id="{epg}" tvg-name="{name}" tvg-logo="{logo}" group-title="{g}",{name}')
    out.append(url)

extra = 0
if os.path.exists("extra.m3u8"):
    for l in open("extra.m3u8", encoding="utf-8"):
        l = l.rstrip("\n")
        if l.strip() and not l.startswith("#EXTM3U") and not l.startswith("# "):
            out.append(l); extra += l.startswith("#EXTINF")

open(dst, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"{len(channels)} canales de TDTChannels ({alt} con enlace de reserva), {extra} extra, {len(quitar)} en quitar.txt")
