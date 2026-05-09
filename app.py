import streamlit as st
import datetime
from PIL import Image
from fpdf import FPDF
from engine import * # Motores preservados v12/v13

# --- DESIGN PREMIUM: INSPIRAÇÃO BATELLO & HARVARD ---
st.set_page_config(page_title="IRIDOLOGIA & IRISDIAGNOSE", layout="wide", page_icon="🔬")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1a1c2c, #0d0d0d); }
    .main-title {
        color: #A51C30;
        font-family: 'Inter', sans-serif;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1px;
        border-left: 5px solid #1e3a8a; /* Azul Batello */
        padding-left: 15px;
        margin-bottom: 30px;
    }
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    .stButton>button {
        background: linear-gradient(135deg, #1e3a8a 0%, #A51C30 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO CORRIGIDO (v14.0) ---
st.markdown("<div class='main-title'>IRIDOLOGIA E IRISDIAGNOSE</div>", unsafe_allow_html=True)

# --- DASHBOARD DO PACIENTE (CAMPOS LIMPOS) ---
with st.expander("👤 DASHBOARD DO PACIENTE", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    with c1: nome_p = st.text_input("NOME COMPLETO", value="", placeholder="Identificação do Caso...")
    with c2: idade_p = st.text_input("IDADE", value="", placeholder="Anos")
    with c3: peso_p = st.number_input("PESO (KG)", value=0.0, format="%.2f")
    with c4: altura_p = st.number_input("ALTURA (M)", value=0.0, format="%.2f")

# --- COMMAND CENTER (BOTÕES DESLIGADOS POR PADRÃO) ---
with st.sidebar:
    st.markdown("<h2 style='color: #A51C30;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
    m_iri = st.toggle("🔬 Módulo Iridologia Master", value=False)
    m_super = st.toggle("🧠 Orquestração Neural IA", value=False)
    m_der = st.toggle("📸 SkinAI v2 Pro", value=False)
    m_rad = st.toggle("📂 Radiologia Digital", value=False)
    st.divider()
    st.caption("Genesis Forensic AI Engine v14.0")

# --- ESTAÇÃO MASTER (CORREÇÃO DO ERRO DE IMAGEM) ---
if m_iri:
    st.markdown("### 🔬 ESTAÇÃO IRIDOLOGIA MASTER")
    col_input, col_viz = st.columns([1, 1.2], gap="large")
    
    with col_input:
        # CORREÇÃO: st.radio substitui st.segmented_control para máxima compatibilidade
        f = st.radio("MODALIDADE DE ENTRADA", ["📁 ARQUIVO/VÍDEO", "📸 CÂMERA LIVE"], horizontal=True)
        
        if f == "📁 ARQUIVO/VÍDEO":
            ent = st.file_uploader("Upload de Amostra (Imagens HD ou Vídeos Forenses)", type=['jpg','png','jpeg','mp4','mov'])
        else:
            ent = st.camera_input("Scanner Sentinel Online")

    if ent:
        with col_viz:
            st.info("💡 Processamento Ativo via Lanczos4")
            if hasattr(ent, 'type') and 'video' in ent.type:
                st.video(ent)
            else:
                img = Image.open(ent)
                img_hd = extrair_qualidade_maxima(img)
                
                tool1, tool2 = st.columns(2)
                with tool1: zoom = st.checkbox("🔍 Zoom Analítico", value=True)
                with tool2: map_iris = st.checkbox("🗺️ Jensen/Batelo Overlay")
                
                if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
                if map_iris: img_hd = aplicar_mapa_iridologico(img_hd)
                
                st.image(img_hd, caption="Processamento Multiespectral Sentinel", use_container_width=True)

            if st.button("⚡ GENERATE HARVARD EXECUTIVE REPORT"):
                # Cálculo de IMC Interno (Somente para o Relatório)
                imc_info = "Não calculado"
                if peso_p > 0 and altura_p > 0:
                    imc_val = peso_p / (altura_p ** 2)
                    imc_info = f"{imc_val:.2f}"
                
                st.success(f"Dossiê HBS para {nome_p} estruturado com sucesso.")
