# AGENTS.md · Color Lab

> Este fichero lo leen los agentes de programación (Copilot, Cursor, Codex, Gemini CLI y otros) antes de tocar vuestro código. Para Claude Code, cread un `CLAUDE.md` con una sola línea: `Sigue las instrucciones de AGENTS.md`. Para Gemini CLI, haced lo mismo con `GEMINI.md`.

## Qué es este proyecto

Asistente web interactivo que calcula la receta exacta de mezcla de pintura (en porcentajes y partes) a partir de una paleta fija de 5 colores base para aficionados al arte, manualidades y manicura.

## Cómo está hecho

- Python 3.10+
- Interfaz: Streamlit (ruta A).
- IA: API de Gemini con el SDK `google-genai`. El modelo principal es `gemini-3.5-flash-lite` y respaldo en `gemini-3.8-flash`.
- Archivos: `app.py` (toda la app), `requirements.txt` (dependencias) y `README.md`.
- La especificación completa está en https://github.com/esquivf1-lab/Color-Lab/blob/main/README.md.

## Reglas

- La clave de la API va SIEMPRE en secretos (`st.secrets["GEMINI_API_KEY"]` en Streamlit Cloud) o variable de entorno (`GEMINI_API_KEY`). Nunca en el código, en el README ni en el chat.
- Cada llamada a la API va dentro de `try/except` con reintentos automáticos (exponential backoff) y muestra un mensaje claro para el usuario.
- Textos de la interfaz en español, sencillos, pensados para alguien sin conocimientos técnicos.
- Cambios pequeños: uno por petición. Al terminar, explica qué has cambiado y por qué.
- Si añades una librería, añádela también a `requirements.txt` y dilo.
- No uses datos personales reales. Para probar, inventa ejemplos.

## Cómo comprobar que funciona

- Ruta A: `streamlit run app.py` en local (con `.streamlit/secrets.toml`), o haz push y revisa la app en Streamlit Cloud.
- Casos de prueba (entrada → lo que esperamos):
  1. Texto: "Vino tinto oscuro" → Receta en JSON con desgloses de Rojo, Azul, Negro sumando 100% y un tip para acrílico/manualidades.
  2. Imagen: Muestra de color en PNG/JPG → Detección multimodal del color con porcentajes y partes correspondientes.
  3. Entrada vacía (botón Calcular sin texto ni foto) → Advertencia amigable `st.warning("⚠️ Ingresa un color o selecciona una imagen.")` sin invocar la API.

## Qué no hacer

- No borres ni reescribas el README sin preguntar.
- No cambies el modelo ni la arquitectura sin preguntar.
- No hagas push ni despliegues sin que yo lo haya revisado.
