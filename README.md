# IPTV

Listas M3U propias.

## Comprobar los enlaces

- `scripts/check.py` revisa cada canal de todas las listas `.m3u`/`.m3u8` del repo y escribe el resultado en `estado.md` (los que funcionan, los dudosos y los que fallan). Los enlaces de AceStream se marcan como "sin comprobar", porque solo se pueden probar con el motor instalado.
- `.github/workflows/comprobar.yml` lo ejecuta cada día. También se puede lanzar a mano en **Actions → Comprobar enlaces → Run workflow**.
- GitHub hace la prueba desde servidores fuera de España, así que los canales con bloqueo por país pueden salir como fallidos aunque en casa funcionen. Para probar desde tu conexión: `python scripts/check.py lista.m3u8`.

## Reproductor web

`player/index.html` es un reproductor que se abre desde el navegador (GitHub Pages):
**https://daniel-garcia-avila.github.io/iptv/player/**

- Carga sola `canales.m3u8`; también admite importar otras listas, favoritos e historial.
- Los canales AceStream necesitan **Ace Stream abierto en el mismo equipo** (Windows: Ace Stream Media; Android: Ace Stream Engine). La web se conecta a él en `http://127.0.0.1:6878`. Si el navegador pide permiso de acceso a la red local, hay que aceptarlo.
- Los canales HLS normales (`https://...m3u8`) funcionan sin motor. Los que son `http://` el navegador los bloquea en una web https: usa "Copiar enlace VLC".
- Enlace directo a un canal: `.../player/#<ID de AceStream>`.
- No funciona en iPhone/iPad (no hay motor AceStream para iOS).
