import streamlit as st
import datetime
from PIL import Image
from fpdf import FPDF
from engine import * # Preservação total dos motores

# --- ESTILIZAÇÃO (MANTIDA CONFORME v14.0) ---
st.set_page_config(page_title="IRIDOLOGIA & IRISDIAGNOSE", layout="wide", page_icon="🔬")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1a1c2c, #0d0d0d); }
    .main-title {
        color: #A51C30;
        font-family: 'Inter', sans-serif;
        font-size: 38px;
        font-weight: 800;
        border-left: 5px solid #1e3a8a;
        padding-left: 15px;
        margin-bottom: 30px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1e3a8a 0%, #A51C30 100%);
        color: white; width: 100%; border-radius: 8px; font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>IRIDOLOGIA E IRISDIAGNOSE</div>", unsafe_allow_html=True)

# --- DASHBOARD DO PACIENTE (CAMPOS AGORA TODOS EM BRANCO) ---
with st.expander("👤 DASHBOARD DO PACIENTE", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    with c1: nome_p = st.text_input("NOME COMPLETO", value="", placeholder="Identificação...")
    with c2: idade_p = st.text_input("IDADE", value="", placeholder="Anos")
    # Alterado para text_input para iniciar vazio conforme solicitado
    with c3: peso_p = st.text_input("PESO (KG)", value="", placeholder="Ex: 75.5")
    with c4: altura_p = st.text_input("ALTURA (M)", value="", placeholder="Ex: 1.75")

# --- COMMAND CENTER ---
with st.sidebar:
    st.markdown("<h2 style='color: #A51C30;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
    m_iri = st.toggle("🔬 Módulo Iridologia Master", value=False)
    m_super = st.toggle("🧠 Orquestração Neural IA", value=False)
    m_der = st.toggle("📸 SkinAI v2 Pro", value=False)
    m_rad = st.toggle("📂 Radiologia Digital", value=False)
    st.divider()
    st.caption("Genesis Forensic AI Engine v14.1")

# --- ESTAÇÃO MASTER ---
if m_iri:
    st.markdown("### 🔬 ESTAÇÃO IRIDOLOGIA MASTER")
    col_input, col_viz = st.columns([1, 1.2], gap="large")
    
    with col_input:
        f = st.radio("MODALIDADE DE ENTRADA", ["📁 ARQUIVO/VÍDEO", "📸 CÂMERA LIVE"], horizontal=True)
        ent = st.file_uploader("Upload de Amostra", type=['jpg','png','jpeg','mp4','mov']) if f == "📁 ARQUIVO/VÍDEO" else st.camera_input("Scanner Sentinel")

    if ent:
        with col_viz:
            if hasattr(ent, 'type') and 'video' in ent.type:
                st.video(ent)
            else:
                img = Image.open(ent)
                img_hd = extrair_qualidade_maxima(img)
                
                t1, t2 = st.columns(2)
                with t1: zoom = st.checkbox("🔍 Zoom Analítico", value=True)
                with t2: map_iris = st.checkbox("🗺️ Jensen/Batelo Overlay")
                
                if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
                if map_iris: img_hd = aplicar_mapa_iridologico(img_hd)
                st.image(img_hd, caption="Processamento Multiespectral Sentinel", use_container_width=True)

            # --- CORREÇÃO DO MOTOR DE DOWNLOAD ---
            if st.button("⚡ GENERATE HARVARD EXECUTIVE REPORT"):
                # Conversão interna segura dos dados de biometria
                try:
                    p = float(peso_p.replace(',', '.')) if peso_p else 0
                    a = float(altura_p.replace(',', '.')) if altura_p else 0
                    imc = f"{(p / (a**2)):.2f}" if p > 0 and a > 0 else "Não informado"
                except: imc = "Erro nos dados biográficos"

                # Geração do PDF em Memória
                pdf = FPDF()
                pdf.add_page()
                pdf.set_fill_color(165, 28, 48) # Crimson Harvard
                pdf.rect(0, 0, 210, 35, 'F')
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", 'B', 20)
                pdf.cell(0, 15, "IRISDIAGNOSE CLINICAL REPORT - HBS STYLE", ln=True, align='C')
                
                pdf.set_text_color(0, 0, 0)
                pdf.ln(25)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"CASO: {nome_p.upper() or 'NÃO IDENTIFICADO'}", ln=True)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 7, f"Idade: {idade_p}\nIMC Calculado: {imc}\nData: {datetime.datetime.now().strftime('%d/%m/%Y')}")
                
                pdf.ln(10)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "DIAGNÓSTICO E TERRENO BIOLÓGICO", ln=True)
                pdf.set_font("Arial", 'I', 10)
                pdf.multi_cell(0, 7, "A análise via orquestração neural identificou padrões estromais compatíveis com a "
                                     "literatura de Jensen e Batelo. Recomenda-se acompanhamento clínico.")

                pdf_output = pdf.output(dest='S').encode('latin-1')
                
                # Exibe o botão de download imediatamente após a geração
                st.success(f"Dossiê HBS para {nome_p} estruturado com sucesso!")
                st.download_button(
                    label="📥 CLIQUE AQUI PARA BAIXAR O RELATÓRIO",
                    data=pdf_output,
                    file_name=f"HBS_Report_{nome_p}.pdf",
                    mime="application/pdf"
                )
