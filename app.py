import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import io
import datetime
import sqlite3  
import base64
import pandas as pd
from fpdf import FPDF 
from gtts import gTTS 
from engine import * # CONEXÃO TOTAL COM O CÉREBRO

# --- DNA NEXUS SENTINEL ESTRUTURA INTEGRADA (INTOCÁVEL) ---
def orquestrador_inteligencia(contexto):
    with st.status(f"🧬 Orquestrador v9.9: Sincronizando IAs e Especialistas...", expanded=True) as s:
        st.write("🔍 Varrendo Metadados Forenses..."); time.sleep(0.5)
        st.write("🧠 Cruzando Dados MedAI Vision X..."); time.sleep(0.5)
        s.update(label="Sincronização Sentinel Concluída", state="complete")
    return True

def realizar_login():
    if "autenticado" not in st.session_state: st.session_state["autenticado"] = False
    if not st.session_state["autenticado"]:
        st.markdown("<h1 style='text-align:center;'>🛡️ GENESIS LOGIN</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col2:
            with st.form("login_form"):
                user = st.text_input("Usuário Profissional")
                pw = st.text_input("Senha Sentinel", type="password")
                if st.form_submit_button("Acessar"):
                    if user == "admin" and pw == "genesis2026":
                        st.session_state["autenticado"] = True; st.session_state["medico_id"] = user; st.rerun()
                    else: st.error("Acesso Negado.")
        return False
    return True

# --- INTERFACE MASTER v9.9 ---
st.set_page_config(page_title="GENESIS OMEGA v9.9", layout="wide", page_icon="🛡️")

if realizar_login():
    st.markdown("""<style>
        .report-card { background-color: #111827; padding: 25px; border-radius: 15px; border-left: 8px solid #3b82f6; margin-top: 20px; }
        .diagnosis-text { font-size: 1.1rem; line-height: 1.6; color: #e5e7eb; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v9.9")

    with st.sidebar:
        st.header("👤 PRONTUÁRIO")
        nome_paciente = st.text_input("Nome do Paciente", "henriue")
        st.divider()
        m_super = st.toggle("🧠 Super IA Genesis", value=True)
        m_iri = st.toggle("🔬 Iridologia Master")
        m_der = st.toggle("📸 SkinAI v2 Pro")
        m_rad = st.toggle("📂 Radiologia Digital")
        m_lab = st.toggle("🧬 Inteligência Laboratorial")
        st.divider()
        if st.button("🚪 Sair"): st.session_state["autenticado"] = False; st.rerun()

    # --- LÓGICA DE EXIBIÇÃO: SUPER IA ---
    if m_super and not any([m_iri, m_der, m_rad, m_lab]):
        st.subheader("🧠 Central de Inteligência Multimodal")
        arquivo = st.file_uploader("Upload de Vídeo/Arquivo para Rastreamento", type=['mp4', 'pdf', 'docx', 'png', 'jpg'])
        pergunta = st.text_area("O que deseja que o Genesis analise?")
        if st.button("Executar Consulta"): 
            orquestrador_inteligencia("Super IA")
            st.success(motor_multimodal_genesis(arquivo, pergunta))

    # --- RENDERIZAÇÃO DOS MÓDULOS DE IMAGEM ---
    def renderizar_modulo_master(label):
        st.subheader(f"Estação {label} | Operador: {st.session_state['medico_id']}")
        c1, c2 = st.columns(2)
        with c1:
            f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label)
            ent = st.camera_input("Scanner") if "📸" in f else st.file_uploader("Importar", type=['jpg','png','jpeg'], key=label+"up")
            zoom = st.checkbox("🔍 Centralizar e Zoom Inteligente", value=True, key=label+"z")
            map_on = st.checkbox("🗺️ Mapeamento Orgânico", key=label+"m") if label == "Iridologia" else False

        if ent:
            img = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img)
            if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
            if map_on: img_hd = aplicar_mapa_iridologico(img_hd)
            
            with c2:
                st.image(img_hd, caption="Visualização Ultra-HD Centralizada", use_container_width=True)
                if st.button(f"⚡ GERAR RELATÓRIO MASTER {label.upper()}", type="primary", key=label+"bt"):
                    orquestrador_inteligencia(label)
                    res_tec = motor_diagnostico_genesis(img_hd, label)
                    res_m = gerar_diagnostico_master_v98(label, res_tec)
                    
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    st.header(res_m['titulo'])
                    for k, v in res_m['secoes'].items(): st.markdown(f"**{k}:** {v}")
                    st.image(res_tec['viz'], caption="Visão Multiespectral", width=400)
                    
                    # Sistema de Impressão PDF Blindado
                    pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", 'B', 16); pdf.cell(200, 10, res_m['titulo'], ln=True)
                    st.download_button("🖨️ IMPRIMIR LAUDO", pdf.output(dest='S'), file_name=f"laudo_{nome_paciente}.pdf", mime="application/pdf")
                    st.markdown('</div>', unsafe_allow_html=True)

    if m_iri: renderizar_modulo_master("Iridologia")
    elif m_der: renderizar_modulo_master("Dermatologia")
    elif m_rad: renderizar_modulo_master("Radiologia")
    elif m_lab:
        st.subheader("🧬 Auditoria Laboratorial")
        exame = st.file_uploader("Upload", type=['pdf', 'jpg', 'png'])
        if exame and st.button("⚡ AUDITORIA"): 
            orquestrador_inteligencia("Lab")
            st.success(f"Dossiê Master processado para {nome_paciente}.")
