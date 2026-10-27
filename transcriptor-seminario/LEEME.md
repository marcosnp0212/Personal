# Transcriptor del seminario

Herramienta de un solo archivo (`transcriptor.html`) para transcribir en directo las ponencias del campus remoto de la UVigo, en castellano y en gallego, y preguntar a Claude sobre lo que se ha dicho.

## Preparación (esta noche, unos 10 minutos)

1. Descarga `transcriptor.html` y ábrelo con doble clic en **Chrome o Edge**.
2. Pega las dos claves en la ventana de Ajustes:
   - **Groq** (transcripción): https://console.groq.com/keys → *Create API Key*. Plan gratuito; si quieres ir sobre seguro, añade una tarjeta en *Billing*: las 12 h saldrían por ~1,30 $.
   - **Anthropic** (preguntas): https://platform.claude.com → *API keys*.
3. Pulsa **Probar claves**: deben salir dos ✅.
4. **Prueba general**: abre un vídeo de YouTube en gallego en otra pestaña, pulsa **● Empezar**, elige *Pestaña de Chrome* → la del vídeo → activa **«Compartir también el audio de la pestaña»** → *Compartir*.

## Durante el seminario

- Crea una **+ Nueva ponencia** para cada charla (ayuda a ordenar y a que las preguntas a la IA sean más baratas y precisas).
- Pon el campus y la herramienta en **dos ventanas**, una al lado de la otra. Seguirás oyendo la ponencia con normalidad.
- El texto aparece cada 10–25 s. Haz clic en cualquier fragmento para corregirlo.
- Al final de cada día pulsa **Copia de seguridad**. Todo se guarda también en el navegador, pero no borres los datos de navegación.

## Si algo falla

| Problema | Solución |
|---|---|
| «Groq ❌ bloqueado por el navegador» o Groq caído | Cambia a **Modo emergencia (gratis, Chrome, micrófono)**: usa el reconocimiento de voz de Chrome escuchando por el micrófono, así que pon los altavoces. Solo un idioma a la vez. |
| Aviso de límite gratuito de Groq | La herramienta reintenta sola y no pierde audio. Para evitarlo, añade una tarjeta en Groq → Billing. |
| No sale texto | Comprueba que la barra de nivel se mueve. Si no se mueve, no se activó «Compartir audio»: Parar y Empezar de nuevo. |

## Costes estimados

- Transcripción (Groq, whisper-large-v3): gratis dentro del límite diario; si no, ~0,11 $ por hora.
- Preguntas (Claude): céntimos por pregunta sobre una ponencia; algo más si preguntas sobre todo el seminario. Puedes elegir un modelo más económico en Ajustes.
