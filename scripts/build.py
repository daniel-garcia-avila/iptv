"""Genera mis_canales_es.m3u8 a partir de la tabla publica de TDTChannels (canales en abierto de Espana)."""
import re, sys, urllib.request
SRC_URL = "https://raw.githubusercontent.com/LaQuay/TDTChannels/master/TELEVISION.md"
dst = sys.argv[1] if len(sys.argv) > 1 else "mis_canales_es.m3u8"
SKIP_FROM = "Int. Europa"
lines = urllib.request.urlopen(SRC_URL, timeout=60).read().decode("utf-8").splitlines()
group = sub = None; out = ['#EXTM3U url-tvg="https://www.tdtchannels.com/epg/TV.xml.gz" x-tvg-url="https://www.tdtchannels.com/epg/TV.xml.gz"']
n = 0; stop = False; counts = {}
for l in lines:
    if l.startswith("## "):
        group = l[3:].strip(); sub = None
        if group == SKIP_FROM: stop = True
        continue
    if stop: break
    if l.startswith("### "): sub = l[4:].strip(); continue
    if not l.startswith("| ") or l.startswith("| Canal") or l.startswith("| -"): continue
    cols = [c.strip() for c in l.strip("|").split(" | ")]
    if len(cols) < 5: continue
    name, m3u, web, logo, epg = cols[:5]
    links = re.findall(r'\[m3u8[^\]]*\]\((https?://[^)]+)\)', m3u)
    # prefer links not marked GEOCAT-only
    if not links: continue
    url = links[0]
    lg = re.search(r'\((https?://[^)]+)\)', logo); lg = lg.group(1) if lg else ""
    epg = "" if epg == "-" else epg
    g = f"Autonómicos - {sub}" if group == "Autonómicos" and sub else group
    out.append(f'#EXTINF:-1 tvg-id="{epg}" tvg-name="{name}" tvg-logo="{lg}" group-title="{g}",{name}')
    out.append(url); n += 1; counts[g] = counts.get(g,0)+1
if n < 50:
    sys.exit(f"Solo {n} canales: algo ha fallado, no se sobrescribe")
print(f"{n} canales")
open(dst, "w", encoding="utf-8").write("\n".join(out)+"\n")
