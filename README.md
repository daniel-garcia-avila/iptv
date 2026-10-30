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
- `.github/workflows/actualizar.yml` lo ejecuta cada día y sube la lista si ha cambiado. También se puede lanzar a mano desde la pestaña **Actions**.
