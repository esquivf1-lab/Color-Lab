# 🎨 Color Lab - Asistente de Mezclas de Pintura

**Color Lab** es una aplicación web interactiva desarrollada en **Streamlit** y potenciada por la **API de Google Gemini**. Su objetivo es calcular la receta exacta de mezcla (en porcentajes y partes) a partir de una paleta fija de 5 colores primarios/base, adaptándose a distintas técnicas de aplicación como acrílico, óleo o manicura en gel.

---

## 🚀 Enlaces del Proyecto

- **App Desplegada:** [Color Lab en Streamlit Cloud](https://color-lab-jlbcb9okorcd2lhomsvht2.streamlit.app/)
- **Repositorio:** [GitHub - esquivf1-lab/Color-Lab](https://github.com/esquivf1-lab/Color-Lab)

---

## 🎯 Problema y Solución

### El Problema
Aficionados a las manualidades, artistas plásticos y profesionales de la manicura suelen desperdiciar tiempo y material intentando obtener tonos específicos mediante ensayo y error.

### La Solución
Color Lab utiliza un modelo multimodal de IA para analizar solicitudes en texto o muestras en imagen, entregando la proporción exacta de pigmentos en formato porcentual y partes concretas, acompañado de un consejo técnico específico para la técnica seleccionada.

---

## 🛠️ Especificaciones Técnicas

- **Lenguaje:** Python 3.10+
- **Framework Web:** Streamlit
- **SDK de IA:** `google-genai`
- **Modelos Utilizados:** `gemini-3.5-flash-lite` (Principal) y `gemini-3.8-flash` (Respaldo/Fallback)
- **Procesamiento:** Estructuración de salida en formato **JSON estricto** mediada por `system_instruction`.

---

## 🎨 Paleta Base Disponible

Cualquier color solicitado se desglosa únicamente utilizando los siguientes 5 pigmentos:
- 🔴 **Rojo**
- 🔵 **Azul**
- 🟡 **Amarillo**
- ⚪ **Blanco**
- ⬛ **Negro**

---

## 🛡️ Robustez y Manejo de Errores

1. **Gestión de Secretos:** La `GEMINI_API_KEY` se lee directamente de las variables de entorno o de `st.secrets`, garantizando que nunca quede expuesta en el código fuente.
2. **Reintentos y Fallback:** Si un modelo experimenta congestión (`503 UNAVAILABLE`) o errores de cuota, la app reintenta de forma automática con un modelo secundario (`gemini-3.5-flash-lite`) y captura las excepciones sin interrumpir la experiencia del usuario.

---

## 💻 Instalación y Ejecución Local

Si deseas clonar y correr la aplicación localmente:

```bash
# 1. Clonar el repositorio
git clone [https://github.com/esquivf1-lab/Color-Lab.git](https://github.com/esquivf1-lab/Color-Lab.git)
cd Color-Lab

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar la API Key
export GEMINI_API_KEY="tu_api_key_aqui"

# 4. Ejecutar la app
streamlit run app.py
