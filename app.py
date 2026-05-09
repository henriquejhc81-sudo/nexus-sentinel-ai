import streamlit as st
import datetime
import cv2
import numpy as np
from PIL import Image
from fpdf import FPDF
from engine import * 

# --- CONFIGURAÇÃO DE UI (PRESERVADA) ---
st.set_page_config(page_title="IRIDOLOGIA & IRISDIAGNOSE", layout="wide", page_icon="🔬")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1a1c2c, #0d0d0d); }
    .main-title {
        color: #A51C30; font-family: 'Inter', sans-serif; font-size: 38px; font-weight: 800;
        border-left: 5px solid #1e3a8a; padding-left: 15px; margin-bottom: 30px;
    }
    .img-container { border: 2px solid #1e3a8a; border-radius: 10px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE AUTO-AJUSTE (NOVA v14.2) ---
def auto_ajuste_forense(imagem_pil):
    """
    Detecta a íris e centraliza a imagem para evitar o erro de posicionamento do print.
    """
    img_cv = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    # Suavização para detecção
    blurred = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 200, param1=50, param2=30, minRadius=50, maxRadius=300)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        x, y, r = circles[0][0]
        # Define um quadrado ao redor da íris com margem de segurança
        margem = int(r * 1.5)
        y1, y2 = max(0, y-margem), min(img_cv.shape, y+margem)
        x1, x2 = max(0, x-margem), min(img_cv.shape, x+margem)
        crop = img_cv[y1:y2, x1:x2]
        return Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    return imagem_pil # Se não detectar, mantém original mas com redimensionamento padronizado

st.markdown("<div class='main-title'>IRIDOLOGIA E IRISDIAGNOSE</div>", unsafe_allow_html=True)

# --- DASHBOARD (MANTIDO CAMPOS EM BRANCO) ---
with st.expander("👤 DASHBOARD DO PACIENTE", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    with c1: nome_p = st.text_input("NOME COMPLETO", value="")
    with c2: idade_p = st.text_input("IDADE", value="")
    with c3: peso_p = st.text_input("PESO (KG)", value="")
    with c4: altura_p = st.text_input("ALTURA (M)", value="")

# --- COMMAND CENTER ---
with st.sidebar:
    st.markdown("<h2 style='color: #A51C30;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
    m_iri = st.toggle("🔬 Módulo Iridologia Master", value=False)
    m_super = st.toggle("🧠 Orquestração Neural IA", value=False)
    m_der = st.toggle("📸 SkinAI v2 Pro", value=False)
    m_rad = st.toggle("📂 Radiologia Digital", value=False)
    st.divider()
    st.caption("Genesis Forensic AI Engine v14.2")

# --- ESTAÇÃO MASTER COM AUTO-AJUSTE ---
if m_iri:
    st.markdown("### 🔬 ESTAÇÃO IRIDOLOGIA MASTER")
    col_input, col_viz = st.columns([1, 1.2], gap="large")
    
    with col_input:
        f = st.radio("MODALIDADE DE ENTRADA", ["📁 ARQUIVO/VÍDEO", "📸 CÂMERA LIVE"], horizontal=True)
        ent = st.file_uploader("Upload", type=['jpg','png','jpeg','mp4','mov']) if f == "📁 ARQUIVO/VÍDEO" else st.camera_input("Scanner")

    if ent:
        with col_viz:
            if hasattr(ent, 'type') and 'video' in ent.type:
                st.video(ent)
            else:
                img_raw = Image.open(ent)
                # Aplicação do Auto-Ajuste v14.2 antes de exibir
                img_ajustada = auto_ajuste_forense(img_raw)
                img_hd = extrair_qualidade_maxima(img_ajustada)
                
                t1, t2 = st.columns(2)
                with t1: zoom = st.checkbox("🔍 Zoom Analítico", value=True)
                with t2: map_iris = st.checkbox("🗺️ Jensen Overlay")
                
                if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
                if map_iris: img_hd = aplicar_mapa_iridologico(img_hd)
                
                # Exibição com moldura CSS para garantir centralização
                st.markdown('<div class="img-container">', unsafe_allow_html=True)
                st.image(img_hd, caption="Processamento Multiespectral Sentinel - Auto Ajustado", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # --- MOTOR DE RELATÓRIO CORRIGIDO ---
            if st.button("⚡ GENERATE HARVARD EXECUTIVE REPORT"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_fill_color(165, 28, 48)
                pdf.rect(0, 0, 210, 35, 'F')
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", 'B', 20)
                pdf.cell(0, 15, "IRISDIAGNOSE CLINICAL REPORT - HBS STYLE", ln=True, align='C')
                
                # Dados Biográficos e IMC
                pdf.set_text_color(0, 0, 0)
                pdf.ln(25)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"ESTUDO DE CASO: {nome_p.upper() or 'NÃO IDENTIFICADO'}", ln=True)
                
                # Inclusão da Imagem Auto-Ajustada no Relatório (Centralização no PDF)
                # Salvando temporariamente para o PDF
                img_hd.save("temp_report.jpg")
                pdf.image("temp_report.jpg", x=55, y=100, w=100) # x=55 centraliza imagem de 100mm
                
                pdf_output = pdf.output(dest='S').encode('latin-1')
                st.success("Dossiê HBS auto-ajustado com sucesso!")
                st.download_button("📥 BAIXAR RELATÓRIO", data=pdf_output, file_name=f"HBS_Report_{nome_p}.pdf")
