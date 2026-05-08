import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import datetime
import base64
from fpdf import FPDF 

# --- SNIPER: IMPORTAÇÃO EXPLÍCITA PARA ELIMINAR NAMEERROR ---
try:
    from engine import (
        extrair_qualidade_maxima, 
        aplicar_zoom_inteligente, 
        processar_camera_inteligente, 
        motor_diagnostico_genesis, 
        aplicar_mapa_iridologico,
        gerar_mega_laudo_iridologico
    )
except ImportError:
    st.error("Erro Crítico: Arquivo engine.py não encontrado no repositório GitHub.")

# --- PROTOCOLO DE SEGURANÇA E LOGIN ---
def realizar_login():
    if "autenticado" not in st.session_state: 
        st.session_state["autenticado"] = False
    
    if not st.session_state["autenticado"]:
        st.markdown("<h1 style='text-align:center;'>🛡️ GENESIS LOGIN</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col2:
            with st.form("login_form"):
                u = st.text_input("Usuário Profissional")
                p = st.text_input("Senha Sentinel", type="password")
                if st.form_submit_button("Acessar Sistema"):
                    if u == "admin" and p == "genesis2026":
                        st.session_state["autenticado"] = True
                        st.session_state["medico_id"] = u
                        st.rerun()
                    else:
                        st.error("Acesso Sentinel Negado.")
        return False
    return True

# --- INTERFACE DASHBOARD v11.1 ---
st.set_page_config(page_title="GENESIS v11.1", layout="wide", page_icon="🛡️")

if realizar_login():
    st.markdown("""<style>
        .report-card { background-color: #111827; padding: 30px; border-radius: 15px; border-left: 10px solid #3b82f6; margin-top: 25px; }
        .section-header { color: #3b82f6; font-weight: bold; font-size: 1.1rem; text-transform: uppercase; border-bottom: 1px solid #334155; }
        .diagnosis-text { font-size: 1.05rem; line-height: 1.6; color: #e5e7eb; padding: 10px 0; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v11.1")

    with st.sidebar:
        st.header("👤 PRONTUÁRIO MASTER")
        nome_p = st.text_input("Identificação do Paciente", "henriue")
        queixa_p = st.text_area("Queixa Principal", "Relato de fadiga...")
        st.divider()
        m_iri = st.toggle("🔬 Iridologia Master", value=True)
        m_der = st.toggle("📸 SkinAI v2 Pro")
        m_lab = st.toggle("🧬 Inteligência Laboratorial")
        if st.button("🚪 Sair"): st.session_state["autenticado"] = False; st.rerun()

    def renderizar_plataforma_v11(label):
        st.subheader(f"Estação de Auditoria: {label}")
        c1, c2 = st.columns(2)
        with c1:
            f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label+"s")
            ent = st.camera_input("Capturar") if f == "📸 Câmera" else st.file_uploader("Importar", type=['jpg','png','jpeg'], key=label+"u")
            zoom = st.checkbox("🔍 Zoom Inteligente (Auto-Focus)", value=True, key=label+"z")
            map_on = st.checkbox("🗺️ Mapeamento de Zonas", value=True, key=label+"m") if label == "Iridologia" else False

        if ent:
            img = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img)
            if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
            if map_on: img_hd = aplicar_mapa_iridologico(img_hd)
            
            with c2:
                st.image(img_hd, caption="Visualização Ultra-HD Centralizada", use_container_width=True)
                if st.button(f"⚡ GERAR DOSSIÊ MASTER", type="primary", key=label+"b"):
                    res_tec = motor_diagnostico_genesis(img_hd, label)
                    laudo = gerar_mega_laudo_iridologico(label, res_tec, queixa_p, nome_p)
                    
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    st.header(f"📋 {laudo['titulo']}")
                    for t, c in laudo['eixos'].items():
                        st.markdown(f"<div class='section-header'>{t}</div><div class='diagnosis-text'>{c}</div>", unsafe_allow_html=True)
                    st.image(res_tec['viz'], caption="Visão Multiespectral de Contraste", width=400)
                    
                    # Sistema de Impressão PDF Blindado
                    pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", 'B', 16); pdf.cell(200, 10, laudo['titulo'], ln=True, align='C')
                    pdf_output = pdf.output(dest='S')
                    if isinstance(pdf_output, str): pdf_output = pdf_output.encode('latin-1')
                    st.download_button("🖨️ IMPRIMIR LAUDO", pdf_output, file_name=f"genesis_{nome_p}.pdf", mime="application/pdf")
                    st.markdown('</div>', unsafe_allow_html=True)

    if m_iri: renderizar_plataforma_v11("Iridologia")
    elif m_der: renderizar_plataforma_v11("Dermatologia")
    elif m_lab: st.info("Módulo Laboratorial ativo.")
