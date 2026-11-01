# Color Lab

**Enlace a la app:** https://color-lab-jlvcb9okorcd2lhomsvht2.streamlit.app/
**Autor/a:** Francisco Antonio Esquivel Barrantes

## Pitch

Obtener la proporción exacta para lograr un tono de pintura específico es un problema común en manualidades, arte y manicura que hoy se resuelve perdiendo tiempo y material por ensayo y error.
Color Lab es un asistente web en Streamlit que calcula instantáneamente la receta exacta de mezcla a partir de texto o fotografías usando una paleta base de 5 colores.
La IA aporta la capacidad multimodal de desglosar la colorimetría de una foto e interpretar matices complejos en lenguaje natural, algo imposible de programar con reglas estáticas.
Durante la fase de prueba aprendimos que los servidores sufrían picos de demanda, por lo que optimizamos el motor hacia el modelo gemini-3.5-flash-lite con reintentos automáticos para garantizar alta velocidad y disponibilidad.
A futuro incorporaremos un exportador de recetas en PDF y un estimador de volumen en mililitros respaldado por pruebas de uso directo en talleres de manicura y artesanía.

## El problema

Aficionados a las manualidades, artistas plásticos y profesionales de la manicura (decoración en uñas) necesitan obtener tonos de pintura específicos a partir de una paleta limitada de colores primarios. Hoy en día lo resuelven mediante ensayo y error, desperdiciando material y tiempo al no lograr la proporción correcta. Merece la pena resolverlo porque optimiza el uso de insumos, reduce costos y ahorra tiempo en proyectos creativos.

## Qué hace la app

1. El usuario selecciona la técnica de pintura deseada en la barra lateral (Acrílico, Manicura/Gel, Óleo).
2. Ingresa el nombre del color mediante texto (ej. "Vino tinto oscuro") o sube/captura una fotografía de la muestra de color.
3. Puede hacer clic en los botones de **Sugerencias Rápidas** ("Piel / Nude", "Vino Tinto", "Verde Oliva", "Lavanda") para un llenado automático.
4. Presiona "Calcular Receta de Mezcla".
5. Visualiza la tarjeta de color (#HEX), las métricas en columnas con los porcentajes y partes de cada pigmento base (Rojo, Azul, Amarillo, Blanco, Negro) y un consejo técnico adaptado.

## La pieza de IA

- **Qué usa:** API de Gemini mediante el nuevo SDK `google-genai`, utilizando `gemini-3.5-flash-lite` como motor principal y `gemini-3.8-flash` como respaldo.
- **Por qué esa opción:** Se eligió por su bajísima latencia, soporte nativo multimodal y alta disponibilidad en cuota gratuita.
- **Qué pasa si falla:** La app cuenta con un bloque de reintentos progresivos (exponential backoff). Si la API experimenta saturación (503 UNAVAILABLE) o agota cuotas, despliega un mensaje amigable: `st.error("Servidores ocupados temporalmente. Por favor reintenta en unos segundos.")`.

## Cómo la he construido

- **Herramientas:** Google Colab con el asistente Gemini integrado para generación del script `app.py`, VS Code y GitHub.
- **Fichero de contexto del agente:** https://github.com/esquivf1-lab/Color-Lab/blob/main/AGENTS.md
- **Prompts clave:**
  1. *"Actúa como un experto en colorimetría. Crea una System Instruction que restrinja las proporciones de mezcla de cualquier color pedido únicamente a Rojo, Azul, Amarillo, Blanco y Negro, respondiendo en formato JSON estricto."*
  2. *"Adapta la llamada del cliente usando el nuevo SDK google-genai para enviar tanto imágenes como texto e implementar un sistema de reintentos ante errores 503."*
  3. *"Optimiza la interfaz en Streamlit para mostrar las métricas por columnas y mantener el estado de la búsqueda mediante callbacks en los botones de sugerencia rápida."*
- **Qué delegué al agente y qué revisé a mano:** Se delegó la estructura base de CSS, el prompt del sistema y el maquetado de `app.py`. Se revisó a mano la jerarquía de llamadas del SDK `google-genai`, la indentación de variables de estado (`componentes`) y la depuración de modelos obsoletos.

## Prueba y mejora

| Quién la probó | Qué probó | Qué pasó | Qué cambié |
|---|---|---|---|
| **Usuaria final (Esposa)** | Consultó colores específicos para manicura (ej. "Nude melocotón") en la pestaña de texto. | La mezcla dio el tono adecuado, pero sugirió acceso directo a colores frecuentes. | Se agregaron los botones de **Sugerencias Rápidas** en la interfaz. |
| **Compañeros en debate del hito** | Probaron la carga de fotografías para detectar colores de muestra. | La app procesó bien la imagen, pero con picos de tráfico lanzaba errores de cuota (`503 UNAVAILABLE`). | Se optimizó el motor hacia `gemini-3.5-flash-lite` con reintentos automáticos (*backoff*). |
| **Usuario / Creador** | Interacción repetida con botones de sugerencia y envío del formulario. | Se perdía la selección y la variable `componentes` lanzaba un error `NameError` de indentación. | Se reestructuró la gestión de estado (`st.session_state`) con callbacks (`on_click=set_color`) y se corrigió la indentación. |

## Ejecutar en local (opcional)

```bash
pip install -r requirements.txt

# Ruta A: poned la clave en .streamlit/secrets.toml y ejecutad
streamlit run app.py
