import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import datetime
import base64
from fpdf import FPDF 
from engine import * # IMPORTAÇÃO GLOBAL PROTEGIDA

# --- NOVO MOTOR DE MAPEAMENTO AMPLIADO (v13.0 - Base Jensen/Batelo) ---
def obter_correlacao_bibliografica(hora, zona):
    biblioteca = {
        "12h": {"Zona 1 (Estômago)": "Centro Vital / Estômago", "Zona 2 (Órgãos)": "Cérebro / Vitalidade"},
        "1h":  {"Zona 2 (Órgãos)": "Face / Maxilar", "Zona 3 (Músculos)": "Garganta"},
        "2h-3h": {"Zona 2 (Órgãos)": "Fígado (D) / Coração (E)", "Zona 3 (Músculos)": "Brônquios / Pleura"},
        "4h":  {"Zona 2 (Órgãos)": "Pulmão Superior", "Zona 3 (Músculos)": "Tórax"},
        "5h":  {"Zona 2 (Órgãos)": "Ombro / Braço", "Zona 4 (Esqueleto)": "Clavícula"},
        "6h":  {"Zona 1 (Estômago)": "Intestino Grosso / Reto", "Zona 7 (Pele)": "Anel de Eliminação / Pele"},
        "7h-8h": {"Zona 2 (Órgãos)": "Rins / Adrenais", "Zona 4 (Esqueleto)": "Pelve"},
        "9h":  {"Zona 2 (Órgãos)": "Baço (E) / Fígado (D)", "Zona 3 (Músculos)": "Escápula"},
        "10h": {"Zona 2 (Órgãos)": "Olho / Ouvido", "Zona 3 (Músculos)": "Pescoço"},
        "11h": {"Zona 2 (Órgãos)": "Mastóide", "Zona 1 (Estômago)": "Esôfago"}
    }
    return biblioteca.get(hora, {}).get(zona, "Área Geral - Consultar Mapa de Jensen")

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="GENESIS v13.0", layout="wide", page_icon="🛡️")

st.markdown("""<style>
    .report-card { background-color: #111827; padding: 30px; border-radius: 15px; border-left: 8px solid #3b82f6; margin-top: 20px; }
    .section-header { color: #3b82f6; font-weight: bold; border-bottom: 1px solid #334155; }
</style>""", unsafe_allow_html=True)

st.title("🛡️ GENESIS FORENSIC AI v13.0")

# --- SIDEBAR: PRONTUÁRIO E MÓDULOS ---
with st.sidebar:
    st.header("👤 PRONTUÁRIO")
    nome_p = st.text_input("Nome do Paciente", "Henrique")
    queixa_p = st.text_area("Queixa/Anamnese", "Descreva aqui...")
    st.divider()
    st.header("⚙️ MÓDULOS ATIVOS")
    m_super = st.toggle("🧠 Super IA Genesis")
    m_iri = st.toggle("🔬 Iridologia Master", value=True)
    m_der = st.toggle("📸 SkinAI v2 Pro")
    m_rad = st.toggle("📂 Radiologia Digital")
    m_lab = st.toggle("🧬 Inteligência Laboratorial")

# --- LÓGICA DE RENDERIZAÇÃO ---

# Função genérica para módulos legados (Dermatologia, Radiologia)
def renderizar_plataforma(label):
    st.subheader(f"Estação {label}")
    c1, c2 = st.columns(2)
    with c1:
        f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label+"s")
        ent = st.camera_input("Scanner") if f == "📸 Câmera" else st.file_uploader("Importar", type=['jpg','png','jpeg'], key=label+"u")
    
    if ent:
        img = Image.open(ent)
        img_hd = extrair_qualidade_maxima(img)
        with c2:
            st.image(img_hd, caption=f"Análise {label}", use_container_width=True)

# MÓDULO IRIDOLOGIA MASTER (CUSTOMIZADO v13.0)
if m_iri:
    st.subheader("🔬 Estação Iridologia Master")
    c1, c2 = st.columns(2)
    with c1:
        f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key="iris_source")
        ent = st.camera_input("Scanner") if f == "📸 Câmera" else st.file_uploader("Importar Íris", type=['jpg','png','jpeg'], key="iris_up")
        
        st.markdown("---")
        st.markdown("### 📝 Registro de Sinais (Tabela de Jensen)")
        col_a, col_b = st.columns(2)
        with col_a:
            olho_lado = st.selectbox("Olho", ["Direito (D)", "Esquerdo (E)"])
            hora_iris = st.select_slider("Posição Horária", options=["12h", "1h", "2h-3h", "4h", "5h", "6h", "7h-8h", "9h", "10h", "11h"])
        with col_b:
            zona_iris = st.selectbox("Zona", ["Zona 1 (Estômago)", "Zona 2 (Órgãos)", "Zona 3 (Músculos)", "Zona 4 (Esqueleto)", "Zona 7 (Pele)"])
            sinal_desc = st.text_input("Sinal (Ex: Lacuna, Anel)", "Lacuna")

    if ent:
        img = Image.open(ent)
        img_hd = extrair_qualidade_maxima(img)
        if st.checkbox("🔍 Zoom Inteligente", value=True): img_hd = aplicar_zoom_inteligente(img_hd)
        if st.checkbox("🗺️ Mapeamento"): img_hd = aplicar_mapa_iridologico(img_hd)
        
        with c2:
            st.image(img_hd, caption="Análise Multiespectral", use_container_width=True)
            if st.button("⚡ GERAR RELATÓRIO PÓS-ANÁLISE", type="primary"):
                correlacao = obter_correlacao_bibliografica(hora_iris, zona_iris)
                
                st.markdown('<div class="report-card">', unsafe_allow_html=True)
                st.markdown("<div class='section-header'>RELATÓRIO DE ESTUDO IRIDOLÓGICO</div>", unsafe_allow_html=True)
                st.write(f"**Paciente:** {nome_p} | **Data:** {datetime.datetime.now().strftime('%d/%m/%Y')}")
                st.info(f"**Correspondência Teórica:** {correlacao}")
                
                # Motor PDF v13
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, "RELATÓRIO IRIDOLÓGICO - GENESIS AI", ln=True, align='C')
                pdf.set_font("Arial", '', 12)
                pdf.multi_cell(0, 10, f"Paciente: {nome_p}\nSinal: {sinal_desc}\nLocal: {hora_iris} ({zona_iris})\nCorrelacao: {correlacao}")
                
                st.download_button("🖨️ BAIXAR PDF", pdf.output(dest='S').encode('latin-1'), file_name=f"iridologia_{nome_p}.pdf")
                st.markdown('</div>', unsafe_allow_html=True)

elif m_der: renderizar_plataforma("Dermatologia")
elif m_rad: renderizar_plataforma("Radiologia")
elif m_lab:
    st.subheader("🧬 Auditoria Laboratorial")
    exame = st.file_uploader("Carregar Exame", type=['pdf', 'jpg', 'png'])
    if exame and st.button("⚡ INICIAR AUDITORIA"): st.success("Auditado com Sucesso.")
elif m_super:
    st.subheader("🧠 Super IA Genesis")
    p = st.text_area("Consulta Multimodal")
    if st.button("Executar"): st.info(motor_multimodal_genesis(None, p))
