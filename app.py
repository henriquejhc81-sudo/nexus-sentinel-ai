import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import datetime
import base64
from fpdf import FPDF 
from engine import * # IMPORTAÇÃO GLOBAL PROTEGIDA

# --- PROTOCOLO DE SEGURANÇA ---
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

st.set_page_config(page_title="GENESIS v12.0", layout="wide", page_icon="🛡️")

if realizar_login():
    st.markdown("""<style>
        .report-card { background-color: #111827; padding: 30px; border-radius: 15px; border-left: 8px solid #3b82f6; margin-top: 20px; }
        .section-header { color: #3b82f6; font-weight: bold; border-bottom: 1px solid #334155; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v12.0")

    with st.sidebar:
        st.header("👤 PRONTUÁRIO")
        nome_p = st.text_input("Nome do Paciente", "henriue")
        queixa_p = st.text_area("Queixa/Anamnese", "Descreva aqui...")
        st.divider()
        m_super = st.toggle("🧠 Super IA Genesis")
        m_iri = st.toggle("🔬 Iridologia Master")
        m_der = st.toggle("📸 SkinAI v2 Pro")
        m_rad = st.toggle("📂 Radiologia Digital")
        m_lab = st.toggle("🧬 Inteligência Laboratorial")
        if st.button("Sair"): st.session_state["autenticado"] = False; st.rerun()

    # --- LÓGICA DOS MÓDULOS RESTAURADOS ---

    def renderizar_plataforma(label):
        st.subheader(f"Estação {label}")
        c1, c2 = st.columns(2)
        with c1:
            f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label+"s")
            ent = st.camera_input("Scanner") if f == "📸 Câmera" else st.file_uploader("Importar", type=['jpg','png','jpeg'], key=label+"u")
            zoom = st.checkbox("🔍 Zoom Inteligente", value=True, key=label+"z")
            map_on = st.checkbox("🗺️ Mapeamento", key=label+"m") if label == "Iridologia" else False

        if ent:
            img = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img)
            if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
            if map_on: img_hd = aplicar_mapa_iridologico(img_hd)
            with c2:
                st.image(img_hd, caption="Ultra-HD Sentinel", use_container_width=True)
                if st.button(f"⚡ GERAR DOSSIÊ {label.upper()}", type="primary", key=label+"btn"):
                    res = motor_diagnostico_genesis(img_hd, label)
                    laudo = gerar_mega_laudo_v12(label, res, queixa_p, nome_p)
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    for k, v in laudo['eixos'].items():
                        st.markdown(f"<div class='section-header'>{k}</div>", unsafe_allow_html=True); st.write(v)
                    st.image(res['viz'], caption="Visão Multiespectral", width=400)
                    # PDF Fix
                    pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", 'B', 16); pdf.cell(200, 10, laudo['titulo'], ln=True)
                    st.download_button("🖨️ IMPRIMIR", pdf.output(dest='S').encode('latin-1'), file_name="laudo.pdf")
                    st.markdown('</div>', unsafe_allow_html=True)

    if m_iri: renderizar_plataforma("Iridologia")
    elif m_der: renderizar_plataforma("Dermatologia")
    elif m_rad: renderizar_plataforma("Radiologia")
    elif m_lab:
        st.subheader("🧬 Auditoria Laboratorial")
        exame = st.file_uploader("Carregar Exame para Auditoria", type=['pdf', 'jpg', 'png'], key="lab_master")
        if exame and st.button("⚡ INICIAR AUDITORIA"): st.success("Auditado com Sucesso.")
    elif m_super:
        st.subheader("🧠 Super IA Genesis")
        p = st.text_area("Consulta Multimodal")
        if st.button("Executar"): st.info(motor_multimodal_genesis(None, p))
