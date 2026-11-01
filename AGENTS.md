# AGENTS.md - Contexto e Instrucciones para Agentes de IA

## 📌 Información del Proyecto
- **Nombre:** Color Lab
- **Descripción:** Asistente web en Streamlit para cálculo de recetas de mezcla de pintura asistido por la API de Gemini.
- **Autor:** Francisco Antonio Esquivel Barrantes
- **Repositorio:** https://github.com/esquivf1-lab/Color-Lab

---

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.10+
- **Framework Web:** Streamlit
- **SDK de IA:** `google-genai`
- **Modelos de Gemini:**
  - Principal: `gemini-3.5-flash-lite` (para baja latencia y cuota gratuita)
  - Respaldo / Fallback: `gemini-3.8-flash`

---

## 🎯 Reglas del Negocio e Instrucciones del Sistema
1. **Paleta Restringida:** Toda propuesta de mezcla DEBE desglosarse ÚNICAMENTE en 5 colores base:
   - Rojo
   - Azul
   - Amarillo
   - Blanco
   - Negro
2. **Formato de Salida:** La API de Gemini debe responder estrictamente en un objeto **JSON válido** que contenga:
   - `hex`: Código hexadecimal estimado del color.
   - `componentes`: Desglose porcentual (la suma debe ser exactamente 100%).
   - `partes`: Relación de partes enteras o decimales simples para fácil medición.
   - `tip`: Consejo técnico adaptado según la técnica elegida (Acrílico, Manicura/Gel, Óleo).

---

## 🔒 Manejo de Secretos y Excepciones
- La API Key (`GEMINI_API_KEY`) NUNCA debe estar hardcodeada en el código. Debe leerse mediante `os.environ` o `st.secrets["GEMINI_API_KEY"]`.
- Las llamadas a la API deben incluir manejo de excepciones y reintentos automáticos (*backoff*) ante errores `503 UNAVAILABLE` o picos de tráfico.
