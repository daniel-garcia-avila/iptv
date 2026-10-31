# IPTV

Listas M3U propias.

## Comprobar los enlaces

- `scripts/check.py` revisa cada canal de todas las listas `.m3u`/`.m3u8` del repo y escribe el resultado en `estado.md` (los que funcionan, los dudosos y los que fallan). Los enlaces de AceStream se marcan como "sin comprobar", porque solo se pueden probar con el motor instalado.
- `.github/workflows/comprobar.yml` lo ejecuta cada día. También se puede lanzar a mano en **Actions → Comprobar enlaces → Run workflow**.
- GitHub hace la prueba desde servidores fuera de España, así que los canales con bloqueo por país pueden salir como fallidos aunque en casa funcionen. Para probar desde tu conexión: `python scripts/check.py lista.m3u8`.
