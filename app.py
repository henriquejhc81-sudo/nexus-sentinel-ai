import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import io
import datetime
import sqlite3  
import base64
from fpdf import FPDF 
from engine import *

# --- PROTOCOLO SENTINEL (INTOCÁVEL) ---
def realizar_login():
    if "autenticado" not in st.session_state: st.session_state["autenticado"] = False
    if not st.session_state["autenticado"]:
        st.markdown("<h1 style='text-align:center;'>🛡️ GENESIS LOGIN</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col2:
            with st.form("login"):
                u = st.text_input("Usuário")
                p = st.text_input("Senha", type="password")
                if st.form_submit_button("Acessar"):
                    if u == "admin" and p == "genesis2026":
                        st.session_state["autenticado"] = True; st.rerun()
                    else: st.error("Acesso Negado.")
        return False
    return True

# --- INTERFACE MASTER v9.8 ---
st.set_page_config(page_title="GENESIS MASTER v9.8", layout="wide")

if realizar_login():
    st.markdown("""<style>
        .report-card { background-color: #111827; padding: 25px; border-radius: 15px; border-left: 8px solid #3b82f6; margin-bottom: 20px; }
        .diagnosis-section { margin-bottom: 15px; font-size: 1.05rem; }
        .section-title { color: #3b82f6; font-weight: bold; border-bottom: 1px solid #3b82f6; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v9.8")

    with st.sidebar:
        nome_paciente = st.text_input("Nome do Paciente", placeholder="Nome completo...")
        m_iri = st.toggle("🔬 Iridologia Master")
        m_lab = st.toggle("🧬 Inteligência Laboratorial")
        if st.button("Sair"): st.session_state["autenticado"] = False; st.rerun()

    if m_iri:
        st.subheader("Estação de Iridologia Master")
        c1, c2 = st.columns(2)
        with c1:
            f = st.radio("Fonte", ["Câmera", "Arquivo"], horizontal=True)
            ent = st.camera_input("Scanner") if f == "Câmera" else st.file_uploader("Upload", type=['jpg','png','jpeg'])
            zoom = st.checkbox("🔍 Centralizar e Zoom Inteligente", value=True)
        
        if ent:
            img = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img)
            if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
            
            with c2:
                st.image(img_hd, caption="Visualização Ultra-HD Centralizada", use_container_width=True)
                if st.button("⚡ GERAR RELATÓRIO MASTER", type="primary"):
                    res_tec = motor_diagnostico_genesis(img_hd, "Iridologia")
                    res_m = gerar_diagnostico_master_v98("Iridologia", res_tec)
                    
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    st.header(f"📋 {res_m['titulo']}")
                    st.write(f"**PACIENTE:** {nome_paciente.upper()} | **DATA:** {datetime.datetime.now().strftime('%d/%m/%Y')}")
                    
                    for titulo, conteudo in res_m['secoes'].items():
                        st.markdown(f"<div class='diagnosis-section'><span class='section-title'>{titulo}</span><br>{conteudo}</div>", unsafe_allow_html=True)
                    
                    st.image(res_tec['viz'], caption="Visão Multiespectral de Contraste", width=400)
                    
                    # BOTÃO DE IMPRESSÃO
                    pdf = FPDF()
                    pdf.add_page(); pdf.set_font("Arial", 'B', 16); pdf.cell(200, 10, res_m['titulo'], ln=True, align='C')
                    pdf.set_font("Arial", '', 11)
                    txt = f"Paciente: {nome_paciente}\n" + "\n".join([f"{k}: {v}" for k, v in res_m['secoes'].items()])
                    pdf.multi_cell(0, 10, txt.encode('latin-1', 'replace').decode('latin-1'))
                    st.download_button("🖨️ IMPRIMIR LAUDO COMPLETO", pdf.output(dest='S'), file_name=f"genesis_{nome_paciente}.pdf", mime="application/pdf")
                    st.markdown('</div>', unsafe_allow_html=True)
