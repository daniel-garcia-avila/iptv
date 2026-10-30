"""Comprueba si los enlaces de una o varias listas M3U responden.

Uso:  python scripts/check.py lista1.m3u8 [lista2.m3u8 ...]
Sin argumentos revisa todos los .m3u/.m3u8 de la carpeta raiz.
Genera estado.md con el resultado.
"""
import glob, re, sys, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

def parse(path):
    name, out = None, []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line.startswith("#EXTINF"):
            name = line.split(",", 1)[-1].strip()
        elif line and not line.startswith("#"):
            out.append((name or line, line)); name = None
    return out

def check(url):
    if url.startswith("acestream://") or "127.0.0.1:6878" in url or "localhost:6878" in url:
        return "ACE", "AceStream: solo se puede probar en un dispositivo con el motor instalado"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=12) as r:
            head = r.read(2048)
            ctype = r.headers.get("Content-Type", "")
            if b"#EXTM3U" in head or "mpegurl" in ctype.lower() or "video" in ctype.lower() or "dash" in ctype.lower() or b"<MPD" in head:
                return "OK", ""
            return "DUDOSO", f"responde pero no parece un vídeo ({ctype or 'sin tipo'})"
    except urllib.error.HTTPError as e:
        return "FALLA", f"HTTP {e.code}" + (" (posible bloqueo por país)" if e.code in (401, 403, 451) else "")
    except Exception as e:
        return "FALLA", type(e).__name__

files = sys.argv[1:] or sorted(glob.glob("*.m3u") + glob.glob("*.m3u8"))
report = ["# Estado de los enlaces", ""]
total = {"OK": 0, "DUDOSO": 0, "FALLA": 0, "ACE": 0}
for f in files:
    items = parse(f)
    with ThreadPoolExecutor(20) as ex:
        res = list(ex.map(lambda it: check(it[1]), items))
    c = {k: sum(1 for r in res if r[0] == k) for k in total}
    for k in total: total[k] += c[k]
    report += [f"## {f}", "", f"✅ {c['OK']} funcionan · ⚠️ {c['DUDOSO']} dudosos · ❌ {c['FALLA']} fallan · 🔵 {c['ACE']} AceStream (sin comprobar)", ""]
    bad = [(n, u, s, d) for (n, u), (s, d) in zip(items, res) if s != "OK"]
    if bad:
        report += ["| Canal | Estado | Detalle |", "| - | - | - |"]
        report += [f"| [{n}]({u}) | { {'DUDOSO': '⚠️', 'ACE': '🔵'}.get(s, '❌') } | {d} |" for n, u, s, d in bad]
        report.append("")
    print(f"{f}: {c}")
open("estado.md", "w", encoding="utf-8").write("\n".join(report) + "\n")
