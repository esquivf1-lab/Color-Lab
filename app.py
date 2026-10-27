import json
import os
import streamlit as st
from google import genai
from google.genai import types

st.title("🎨 Asistente de Mezclas de Pintura")
st.write("Escribe el color que necesitas y obtén la receta de mezcla con pinturas tradicionales.")

color_deseado = st.text_input(
    "¿Qué color deseas obtener?",
    placeholder="Ejemplo: Naranja terracota, Verde musgo, Turquesa brillante, Piel clara"
)

SYSTEM_INSTRUCTION = """
Eres un experto en pintura física tradicional.
Cuando el usuario te pida un color, calcula las proporciones de mezcla usando únicamente:
Rojo, Azul, Amarillo, Blanco y Negro.

Responde ÚNICAMENTE en formato JSON con la siguiente estructura:
{
  "color": "Nombre del color",
  "mezcla": [
    {"pigmento": "Nombre", "porcentaje": 0, "partes": "ej. 2 partes"}
  ],
  "instruccion_rapida": "Breve frase de cómo mezclarlo"
}
"""

if st.button("Calcular Mezcla") and color_deseado:
    with st.spinner("Calculando la receta de pintura..."):
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            client = genai.Client(api_key=api_key)

            prompt = f"Dame la receta de pintura tradicional para obtener el color: {color_deseado}"

            # Usamos el modelo solicitado por la API: gemini-3.8-flash
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )

            datos = json.loads(response.text)

            st.subheader(f"Mezcla para: {datos['color']}")
            for elem in datos["mezcla"]:
                st.write(f"• **{elem['pigmento']}**: {elem['porcentaje']}% ({elem['partes']})")

            st.info(f"💡 **Tip de mezcla:** {datos['instruccion_rapida']}")

        except Exception as e:
            st.error(f"Error al consultar Gemini: {e}")
