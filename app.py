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
    .img-container { border: 2px solid #1e3a8a; border-radius: 10px; overflow: hidden; background: #000; }
    </style>
""", unsafe_allow_html=True)

# --- NOVA FUNÇÃO: RASTREADOR AUTOMÁTICO DE ÍRIS (v14.5) ---
def motor_rastreio_iris(imagem_pil):
    """
    Independente de onde o olho estiver, a função localiza a íris e foca nela 
    automaticamente para a leitura forense.
    """
    img_cv = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Suavização inteligente para isolar o globo ocular
    gray_blur = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Detecção Paramétrica Circular (Busca Dinâmica em toda a imagem)
    circles = cv2.HoughCircles(gray_blur, cv2.HOUGH_GRADIENT, 1.2, 100, 
                               param1=50, param2=35, minRadius=30, maxRadius=int(img_cv.shape[0]/2))
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # Cria um recorte focado na íris detectada, ignorando o resto da foto
            pad = int(r * 1.5)
            y1, y2 = max(0, y-pad), min(img_cv.shape, y+pad)
            x1, x2 = max(0, x-pad), min(img_cv.shape, x+pad)
            crop = img_cv[y1:y2, x1:x2]
            return Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
            
    return imagem_pil # Fallback caso a luz esteja muito baixa

st.markdown("<div class='main-title'>IRIDOLOGIA E IRISDIAGNOSE</div>", unsafe_allow_html=True)

# --- DASHBOARD DO PACIENTE (CAMPOS LIMPOS) ---
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
    st.caption("Genesis Forensic AI Engine v14.5")

# --- ESTAÇÃO MASTER COM RASTREIO AUTOMÁTICO ---
if m_iri:
    st.subheader("🔬 ESTAÇÃO IRIDOLOGIA MASTER")
    col_input, col_viz = st.columns([1, 1.2], gap="large")
    
    with col_input:
        f = st.radio("MODALIDADE DE ENTRADA", ["📁 ARQUIVO/VÍDEO", "📸 CÂMERA LIVE"], horizontal=True)
        ent = st.file_uploader("Importar Mídia", type=['jpg','png','jpeg','mp4','mov']) if f == "📁 ARQUIVO/VÍDEO" else st.camera_input("Scanner")

    if ent:
        with col_viz:
            if hasattr(ent, 'type') and 'video' in ent.type:
                st.video(ent)
            else:
                img_raw = Image.open(ent)
                # O SISTEMA ENCONTRA A ÍRIS AUTOMATICAMENTE AQUI
                img_focada = motor_rastreio_iris(img_raw)
                img_hd = extrair_qualidade_maxima(img_focada)
                
                t1, t2 = st.columns(2)
                with t1: zoom = st.checkbox("🔍 Zoom Analítico", value=True)
                with t2: map_iris = st.checkbox("🗺️ Jensen Overlay")
                
                if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
                if map_iris: img_hd = aplicar_mapa_iridologico(img_hd)
                
                st.markdown('<div class="img-container">', unsafe_allow_html=True)
                st.image(img_hd, caption="Detecção Automática e Foco na Íris Sentinel", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # --- CORREÇÃO DEFINITIVA DO MOTOR DE PDF (v14.5) ---
            if st.button("⚡ GENERATE HARVARD EXECUTIVE REPORT"):
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_fill_color(165, 28, 48)
                    pdf.rect(0, 0, 210, 35, 'F')
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", 'B', 20)
                    pdf.cell(0, 15, "IRISDIAGNOSE CLINICAL REPORT", ln=True, align='C')
                    
                    pdf.set_text_color(0, 0, 0)
                    pdf.ln(25)
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(0, 10, f"PACIENTE: {nome_p.upper() if nome_p else 'NÃO IDENTIFICADO'}", ln=True)
                    
                    # Salva e anexa a imagem focada
                    img_hd.save("temp_report.jpg")
                    pdf.image("temp_report.jpg", x=55, y=100, w=100)
                    
                    # O segredo para não dar erro: Gerar o buffer binário fora do botão de download
                    pdf_bin = pdf.output(dest='S').encode('latin-1', 'replace')
                    
                    st.success("Dossiê gerado com sucesso!")
                    st.download_button(
                        label="📥 BAIXAR RELATÓRIO PDF",
                        data=pdf_bin,
                        file_name=f"HBS_Report_{nome_p}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Erro ao gerar relatório: {e}")
