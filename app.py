import json
import os
import time
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# 1. Configuración de página
st.set_page_config(
    page_title="Color Lab - Asistente de Mezclas", 
    page_icon="🎨",
    layout="wide"
)

# Inicializar variables de estado
if "historial" not in st.session_state:
    st.session_state.historial = []
if "color_input" not in st.session_state:
    st.session_state.color_input = ""

def set_color(nombre_color):
    st.session_state.color_input = nombre_color

# 2. Estilos CSS
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E293B; margin-bottom: 0px; }
    .sub-title { color: #64748B; font-size: 1rem; margin-bottom: 20px; }
    .color-box { height: 80px; border-radius: 12px; border: 2px solid #E2E8F0; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# 3. BARRA LATERAL
with st.sidebar:
    st.image("https://em-content.zobj.net/source/microsoft-teams/337/artist-palette_1f3a8.png", width=50)
    st.title("Color Lab")
    
    st.subheader("🎨 Tipo de Aplicación")
    tecnica = st.selectbox("Selecciona la técnica:", ["Manualidades / Acrílico", "Manicura / Gel o Esmalte", "Óleo / Lienzo"])
    
    st.divider()
    st.write("**Paleta base disponible:**")
    st.markdown("- 🔴 Rojo\n- 🔵 Azul\n- 🟡 Amarillo\n- ⚪ Blanco\n- ⬛ Negro")
    
    st.divider()
    st.subheader("📜 Consultas Recientes")
    if st.session_state.historial:
        for item in reversed(st.session_state.historial[-5:]):
            st.caption(f"• **{item['color']}** ({item['hex']})")
    else:
        st.caption("Aún no has realizado búsquedas.")
        
    st.divider()
    st.caption("Powered by Gemini 3.8 Flash")

# 4. ENCABEZADO
st.markdown('<p class="main-title">🎨 Asistente de Mezclas de Pintura</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Obtén la proporción exacta de mezcla y consejos prácticos para tus proyectos.</p>', unsafe_allow_html=True)

SYSTEM_INSTRUCTION = f"""
Eres un experto en colorimetría y mezcla de pinturas tradicionales.
Técnica elegida por el usuario: {tecnica}.
Calcula las proporciones usando únicamente: Rojo, Azul, Amarillo, Blanco y Negro.

Responde ÚNICAMENTE en formato JSON estricto con esta estructura:
{{
  "color": "Nombre del color",
  "hex_estimado": "#HEX_DEL_COLOR",
  "mezcla": [
    {{"pigmento": "Nombre", "porcentaje": 0, "partes": "ej. 2 partes"}}
  ],
  "instruccion_rapida": "Consejo técnico adaptado a {tecnica}"
}}
"""

def obtener_api_key():
    # Intenta buscar primero en os.environ (para Colab/Cloudflare) y luego en st.secrets (para Streamlit Cloud)
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        try:
            if "GEMINI_API_KEY" in st.secrets:
                key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
    return key

def consultar_gemini(contents, api_key):
    if not api_key:
        raise ValueError("No se encontró la GEMINI_API_KEY. Configúrala en las variables de entorno o Secrets.")
        
    client = genai.Client(api_key=api_key)
    
    # Cadena de modelos oficiales
    modelos = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    
    ultimo_error = None
    for modelo in modelos:
        try:
            response = client.models.generate_content(
                model=modelo,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            return json.loads(response.text)
        except Exception as e:
            ultimo_error = e
            time.sleep(1) # Pausa ligera de 1 segundo antes de probar el siguiente modelo
            continue
            
    raise Exception(f"Los servidores de la API están ocupados en este momento ({ultimo_error}). Por favor reintenta en unos segundos.")

@st.cache_data(show_spinner=False)
def obtener_receta_texto(prompt_texto, api_key):
    contents = f"Dame la receta para obtener el color: {prompt_texto}"
    return consultar_gemini(contents, api_key)

# 5. SECCIÓN DE ENTRADA
col_input, col_space = st.columns([2, 1])

with col_input:
    tab1, tab2 = st.tabs(["📝 Entrada por Texto", "📷 Captura o Imagen"])
    imagen_cargada = None

    with tab1:
        color_deseado = st.text_input(
            "¿Qué tono buscas obtener?", 
            placeholder="Ej: Terracota, Verde musgo, Nude melocotón, Palo de rosa",
            key="color_input"
        )
        
        st.caption("Sugerencias rápidas:")
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        col_b1.button("Piel / Nude", type="secondary", on_click=set_color, args=("Piel clara nude",))
        col_b2.button("Vino Tinto", type="secondary", on_click=set_color, args=("Vino tinto oscuro",))
        col_b3.button("Verde Oliva", type="secondary", on_click=set_color, args=("Verde oliva",))
        col_b4.button("Lavanda", type="secondary", on_click=set_color, args=("Lavanda pastel",))

    with tab2:
        opcion_foto = st.radio("Origen de la imagen:", ["Subir de la galería", "Tomar foto con la cámara"], horizontal=True)
        if opcion_foto == "Subir de la galería":
            archivo = st.file_uploader("Sube una imagen muestra", type=["jpg", "jpeg", "png"])
            if archivo: imagen_cargada = Image.open(archivo)
        else:
            captura = st.camera_input("Toma una foto al color deseado")
            if captura: imagen_cargada = Image.open(captura)
            
        if imagen_cargada:
            st.image(imagen_cargada, caption="Muestra seleccionada", width=200)

    btn_calcular = st.button("✨ Calcular Receta de Mezcla", type="primary")

# 6. RESULTADOS
if btn_calcular:
    if not color_deseado and not imagen_cargada:
        st.warning("⚠️ Ingresa un color o selecciona una imagen.")
    else:
        st.divider()
        with st.spinner("🔍 Analizando pigmentos..."):
            try:
                api_key = obtener_api_key()

                if imagen_cargada:
                    prompt = "Identifica el color principal en esta imagen y dame la receta de mezcla."
                    datos = consultar_gemini([imagen_cargada, prompt], api_key)
                else:
                    datos = obtener_receta_texto(color_deseado, api_key)

                color_nombre = datos.get('color', color_deseado or 'Color analizado')
                hex_code = datos.get("hex_estimado", "#2563EB")
                
                if not any(h['color'] == color_nombre for h in st.session_state.historial):
                    st.session_state.historial.append({"color": color_nombre, "hex": hex_code})

                col_res1, col_res2 = st.columns([1, 3])
                
                with col_res1:
                    st.markdown(f'<div class="color-box" style="background-color: {hex_code};"></div>', unsafe_allow_html=True)
                    st.caption(f"Tono estimado: **{hex_code}**")

                with col_res2:
                    st.subheader(f"🧪 Receta para: **{color_nombre}**")

                componentes = datos.get("mezcla", [])
                cols = st.columns(len(componentes) if componentes else 1)
                for idx, elem in enumerate(componentes):
                    with cols[idx]:
                        st.metric(label=elem['pigmento'], value=f"{elem['porcentaje']}%", delta=elem['partes'], delta_color="off")

                if "instruccion_rapida" in datos:
                    st.info(f"💡 **Tip para {tecnica}:** {datos['instruccion_rapida']}")

            except Exception as e:
                st.error(f"⚠️ {e}")
