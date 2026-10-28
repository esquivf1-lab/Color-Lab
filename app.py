import json
import os
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

# Inicializar historial en la memoria de sesión si no existe
if "historial" not in st.session_state:
    st.session_state.historial = []

# 2. Estilos CSS para personalizar el diseño
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E293B; margin-bottom: 0px; }
    .sub-title { color: #64748B; font-size: 1rem; margin-bottom: 20px; }
    .color-box { height: 80px; border-radius: 12px; border: 2px solid #E2E8F0; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# 3. BARRA LATERAL (Sidebar)
with st.sidebar:
    st.image("https://em-content.zobj.net/source/microsoft-teams/337/artist-palette_1f3a8.png", width=50)
    st.title("Color Lab")
    
    st.subheader("🎨 Tipo de Aplicación")
    tecnica = st.selectbox("Selecciona la técnica:", ["Manualidades / Acrílico", "Manicura / Gel o Esmalte", "Óleo / Lienzo"])
    
    st.divider()
    st.write("**Paleta base disponible:**")
    st.markdown("- 🔴 Rojo\n- 🔵 Azul\n- 🟡 Amarillo\n- ⚪ Blanco\n- ⬛ Negro")
    
    # SECCIÓN DE HISTORIAL EN LA BARRA LATERAL
    st.divider()
    st.subheader("📜 Consultas Recientes")
    if st.session_state.historial:
        for item in reversed(st.session_state.historial[-5:]): # Muestra los últimos 5
            st.caption(f"• **{item['color']}** ({item['hex']})")
    else:
        st.caption("Aún no has realizado búsquedas.")
        
    st.divider()
    st.caption("Powered by Gemini 3.8 Flash")

# 4. ENCABEZADO
st.markdown('<p class="main-title">🎨 Asistente de Mezclas de Pintura</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Obtén la proporción exacta de mezcla y consejos prácticos para tus proyectos.</p>', unsafe_allow_html=True)

# 5. INSTRUCCIÓN DEL SISTEMA
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

# FUNCIÓN CON CACHÉ PARA OPTIMIZAR
@st.cache_data(show_spinner=False)
def obtener_receta_texto(prompt_texto, api_key):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"Dame la receta para obtener el color: {prompt_texto}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            temperature=0.2
        )
    )
    return json.loads(response.text)

# 6. SECCIÓN DE ENTRADA
col_input, col_space = st.columns([2, 1])

with col_input:
    tab1, tab2 = st.tabs(["📝 Entrada por Texto", "📷 Captura o Imagen"])
    color_deseado = None
    imagen_cargada = None

    with tab1:
        color_input = st.text_input("¿Qué tono buscas obtener?", placeholder="Ej: Terracota, Verde musgo, Nude melocotón, Palo de rosa")
        
        # Sugerencias rápidas con botones secundarios (tipo chips)
        st.caption("Sugerencias rápidas:")
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        if col_b1.button("Piel / Nude", type="secondary"): color_deseado = "Piel clara nude"
        elif col_b2.button("Vino Tinto", type="secondary"): color_deseado = "Vino tinto oscuro"
        elif col_b3.button("Verde Oliva", type="secondary"): color_deseado = "Verde oliva"
        elif col_b4.button("Lavanda", type="secondary"): color_deseado = "Lavanda pastel"
        else:
            color_deseado = color_input

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

# 7. RESULTADOS
if btn_calcular:
    if not color_deseado and not imagen_cargada:
        st.warning("⚠️ Ingresa un color o selecciona una imagen.")
    else:
        st.divider()
        with st.spinner("🔍 Analizando pigmentos..."):
            try:
                api_key = os.environ.get("GEMINI_API_KEY")

                if imagen_cargada:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=[imagen_cargada, "Identifica el color principal en esta imagen y dame la receta de mezcla."],
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                            response_mime_type="application/json",
                            temperature=0.2
                        )
                    )
                    datos = json.loads(response.text)
                else:
                    datos = obtener_receta_texto(color_deseado, api_key)

                # Guardar en el historial de sesión
                color_nombre = datos.get('color', color_deseado or 'Color analizado')
                hex_code = datos.get("hex_estimado", "#2563EB")
                
                # Evitar duplicados consecutivos en el historial
                if not any(h['color'] == color_nombre for h in st.session_state.historial):
                    st.session_state.historial.append({"color": color_nombre, "hex": hex_code})

                # Muestra visual del resultado
                col_res1, col_res2 = st.columns([1, 3])
                
                with col_res1:
                    st.markdown(f'<div class="color-box" style="background-color: {hex_code};"></div>', unsafe_allow_html=True)
                    st.caption(f"Tono estimado: **{hex_code}**")

                with col_res2:
                    st.subheader(f"🧪 Receta para: **{color_nombre}**")

                # Porcentajes en tarjetas
                componentes = datos.get("mezcla", [])
                cols = st.columns(len(componentes) if componentes else 1)
                for idx, elem in enumerate(componentes):
                    with cols[idx]:
                        st.metric(label=elem['pigmento'], value=f"{elem['porcentaje']}%", delta=elem['partes'], delta_color="off")

                if "instruccion_rapida" in datos:
                    st.info(f"💡 **Tip para {tecnica}:** {datos['instruccion_rapida']}")

            except Exception as e:
                st.error(f"Error en la consulta: {e}")
