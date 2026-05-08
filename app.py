import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import datetime
import base64
from fpdf import FPDF 
from engine import * 

# --- PROTOCOLO SENTINEL (INTOCÁVEL) ---
def realizar_login():
    if "autenticado" not in st.session_state: st.session_state["autenticado"] = False
    if not st.session_state["autenticado"]:
        st.markdown("<h1 style='text-align:center;'>🛡️ GENESIS LOGIN</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with col2:
            with st.form("login"):
                u = st.text_input("Usuário"); p = st.text_input("Senha", type="password")
                if st.form_submit_button("Acessar"):
                    if u == "admin" and p == "genesis2026":
                        st.session_state["autenticado"] = True; st.session_state["medico_id"] = u; st.rerun()
                    else: st.error("Acesso Negado.")
        return False
    return True

st.set_page_config(page_title="GENESIS v11.0", layout="wide", page_icon="🛡️")

if realizar_login():
    st.markdown("""<style>
        .report-card { background-color: #111827; padding: 30px; border-radius: 15px; border-left: 10px solid #3b82f6; margin-top: 25px; }
        .section-header { color: #3b82f6; font-weight: bold; font-size: 1.1rem; text-transform: uppercase; margin-top: 15px; border-bottom: 1px solid #334155; }
        .diagnosis-text { font-size: 1.05rem; line-height: 1.6; color: #e5e7eb; padding: 10px 0; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v11.0")

    with st.sidebar:
        st.header("👤 PRONTUÁRIO MASTER")
        nome_paciente = st.text_input("Identificação do Paciente", "henriue")
        queixa_principal = st.text_area("Queixa Principal / Histórico", "Relato de estresse e fadiga...")
        st.divider()
        m_super = st.toggle("🧠 Super IA Genesis")
        m_iri = st.toggle("🔬 Iridologia Master", value=True)
        m_der = st.toggle("📸 SkinAI v2 Pro")
        m_rad = st.toggle("📂 Radiologia Digital")
        m_lab = st.toggle("🧬 Inteligência Laboratorial")
        if st.button("Sair"): st.session_state["autenticado"] = False; st.rerun()

    def renderizar_modulo_v11(label):
        st.subheader(f"Estação de Auditoria: {label}")
        c1, c2 = st.columns(2)
        with c1:
            f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label)
            ent = st.camera_input("Capturar") if f == "📸 Câmera" else st.file_uploader("Importar", type=['jpg','png','jpeg'], key=label+"up")
            zoom = st.checkbox("🔍 Centralizar e Zoom Inteligente", value=True, key=label+"z")
            map_on = st.checkbox("🗺️ Mapeamento Orgânico", value=True, key=label+"m") if label == "Iridologia" else False

        if ent:
            img = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img)
            if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
            if map_on: img_hd = aplicar_mapa_iridologico(img_hd)
            
            with c2:
                st.image(img_hd, caption="Registro Fotográfico de Alta Resolução", use_container_width=True)
                if st.button(f"⚡ GERAR DOSSIÊ COMPLETO {label.upper()}", type="primary", key=label+"bt"):
                    res_tec = motor_diagnostico_genesis(img_hd, label)
                    laudo = gerar_mega_laudo_iridologico(label, res_tec, queixa_principal, nome_paciente)
                    
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    st.header(f"📋 {laudo['titulo']}")
                    
                    for titulo, conteudo in laudo['eixos'].items():
                        st.markdown(f"<div class='section-header'>{titulo}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='diagnosis-text'>{conteudo}</div>", unsafe_allow_html=True)
                    
                    st.image(res_tec['viz'], caption="Visão Multiespectral de Contraste (Detecção de Lacunas)", width=400)
                    
                    # --- SISTEMA DE IMPRESSÃO MASTER PDF ---
                    pdf = FPDF()
                    pdf.add_page(); pdf.set_font("Arial", 'B', 16)
                    pdf.cell(200, 10, laudo['titulo'], ln=True, align='C')
                    pdf.set_font("Arial", '', 11)
                    full_txt = ""
                    for k, v in laudo['eixos'].items(): full_txt += f"\n{k}:\n{v}\n"
                    pdf.multi_cell(0, 10, full_txt.encode('latin-1', 'replace').decode('latin-1'))
                    
                    pdf_output = pdf.output(dest='S')
                    if isinstance(pdf_output, str): pdf_output = pdf_output.encode('latin-1')
                    
                    st.download_button("🖨️ IMPRIMIR LAUDO OFICIAL", pdf_output, file_name=f"genesis_laudo_{nome_paciente}.pdf", mime="application/pdf")
                    st.markdown('</div>', unsafe_allow_html=True)

    if m_iri: renderizar_modulo_v11("Iridologia")
    elif m_der: renderizar_modulo_v11("Dermatologia")
    elif m_rad: renderizar_modulo_v11("Radiologia")
    elif m_lab:
        st.subheader("🧬 Inteligência Laboratorial")
        exame = st.file_uploader("Upload do Exame", type=['pdf', 'jpg', 'png'])
        if exame and st.button("⚡ AUDITORIA"): st.success("Dossiê processado.")
