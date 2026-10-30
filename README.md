# IPTV – canales en abierto de España

Lista M3U con los canales de TV que se emiten en abierto por Internet en España, generada a partir de [TDTChannels](https://github.com/LaQuay/TDTChannels). Se actualiza sola cada día con GitHub Actions.

## URL para tu reproductor

```
https://raw.githubusercontent.com/daniel-garcia-avila/iptv/main/mis_canales_es.m3u8
```

Guía de programación (EPG), por si tu reproductor no la carga sola:

```
https://www.tdtchannels.com/epg/TV.xml.gz
```

- **VLC:** Medio → Abrir ubicación de red.
- **Kodi:** complemento *PVR IPTV Simple Client* → URL de la lista M3U.
- **TiviMate / IPTV Smarters / app IPTV de la tele:** añadir lista por URL.

## Cómo funciona

- `scripts/build.py` descarga la tabla de canales de TDTChannels y genera `mis_canales_es.m3u8`, agrupada en Nacionales, Informativos, Deportivos, Infantiles, Eventuales y Autonómicos por comunidad.
- Si un canal tiene varios enlaces, se usa el primero que funcione.
- `quitar.txt`: canales que no quieres (un nombre por línea).
- `extra.m3u8`: canales tuyos que se añaden al final de la lista.
- `.github/workflows/actualizar.yml` lo ejecuta cada día y sube la lista si ha cambiado. También se puede lanzar a mano desde la pestaña **Actions**.

## Comprobar los enlaces

- `scripts/check.py` revisa cada canal de todas las listas `.m3u`/`.m3u8` del repo y escribe el resultado en `estado.md` (los que funcionan, los dudosos y los que fallan).
- `.github/workflows/comprobar.yml` lo ejecuta cada día. También se puede lanzar a mano en **Actions → Comprobar enlaces → Run workflow**.
- Ojo: GitHub hace la prueba desde servidores fuera de España, así que los canales con bloqueo por país pueden salir como fallidos aunque en casa funcionen. Para una prueba real desde tu conexión: `python scripts/check.py mis_canales_es.m3u8`.
