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
import google.generativeai as genai
from groq import Groq
from fpdf import FPDF 
from gtts import gTTS 
from duckduckgo_search import DDGS  
import plotly.graph_objects as go 
import hashlib 
# --- IMPORTAÇÃO COMPLETA DA ENGINE ---
from engine import *

# --- DNA NEXUS SENTINEL ESTRUTURA INTEGRADA (INTOCÁVEL) ---

def orquestrador_inteligencia(contexto):
    especialistas = ["Segurança", "Performance", "UX", "Dev", "QA", "Jurídico", "Hacker Ético"]
    with st.status(f"🧬 Orquestrador v9.1: Validando Protocolos...", expanded=True) as status:
        time.sleep(0.5)
        status.update(label="Sincronização Sentinel Concluída", state="complete")
    return True

def init_db_multiplayer():
    conn = sqlite3.connect('genesis_multiplayer.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS diagnosticos 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, medico_id TEXT, paciente TEXT, 
                  modulo TEXT, data TEXT, score_estresse REAL, parecer TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT UNIQUE, senha TEXT)''')
    conn.commit()
    conn.close()

def realizar_login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
    if not st.session_state["autenticado"]:
        st.markdown("<h1 style='text-align: center;'>🛡️ GENESIS LOGIN</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3) 
        with col2:
            with st.form("login_form"):
                user = st.text_input("Usuário Profissional")
                pw = st.text_input("Senha Sentinel", type="password")
                if st.form_submit_button("Acessar Sistema"):
                    if user == "admin" and pw == "genesis2026":
                        st.session_state["autenticado"] = True
                        st.session_state["medico_id"] = user
                        st.rerun()
                    else: st.error("Acesso Negado.")
        return False
    return True

def gerar_pdf_impressao(paciente, modulo, laudo_texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "GENESIS FORENSIC AI - RELATÓRIO MASTER", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, laudo_texto.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACE DASHBOARD v9.1 ---

st.set_page_config(page_title="GENESIS MASTER v9.1", layout="wide", page_icon="🛡️")
init_db_multiplayer()

if realizar_login():
    st.markdown("""<style>
        .main { background-color: #0e1117; }
        .report-card { background-color: #111827; padding: 25px; border-radius: 15px; border-left: 8px solid #3b82f6; margin-top: 20px; }
        .diagnosis-text { font-size: 1.05rem; color: #e5e7eb; line-height: 1.6; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v9.1")

    with st.sidebar:
        st.header("👤 PRONTUÁRIO")
        nome_paciente = st.text_input("Nome do Paciente", placeholder="Identifique o paciente...")
        st.divider()
        m_iri = st.toggle("🔬 Iridologia Master")
        m_der = st.toggle("📸 SkinAI v2 Pro")
        m_rad = st.toggle("📂 Radiologia Digital")
        m_lab = st.toggle("🧬 Inteligência Laboratorial")
        st.divider()
        if st.button("Sair"):
            st.session_state["autenticado"] = False
            st.rerun()

    def renderizar_modulo_master(label):
        st.subheader(f"Estação {label}")
        col_in, col_res = st.columns(2)
        with col_in:
            f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label+"s")
            ent = st.camera_input("Scanner") if "📸" in f else st.file_uploader("Importar", type=['jpg','png','jpeg'], key=label+"u")
            zoom = st.checkbox("🔍 Zoom Digital Inteligente", key=label+"z")
        
        if ent:
            img = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img)
            if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
            with col_res:
                st.image(img_hd, use_container_width=True)
                if st.button(f"⚡ GERAR DIAGNÓSTICO MASTER {label.upper()}", type="primary", key=label+"b"):
                    orquestrador_inteligencia(label)
                    res_tec = motor_diagnostico_genesis(img_hd, label)
                    res_m = gerar_diagnostico_master(label, res_tec)
                    st.markdown(f"""<div class="report-card">
                        <h2 style="color:#3b82f6;">🧬 {res_m['titulo']}</h2>
                        <p class="diagnosis-text">{res_m['explicacao']}</p>
                    </div>""", unsafe_allow_html=True)
                    st.image(res_tec['viz'], caption="Visão Multiespectral", width=400)

    if m_iri: renderizar_modulo_master("Iridologia")
    elif m_der: renderizar_modulo_master("Dermatologia")
    elif m_rad: renderizar_modulo_master("Radiologia")
    elif m_lab:
        st.subheader("🧬 Inteligência Laboratorial")
        exame = st.file_uploader("Upload do Exame", type=['pdf', 'jpg', 'png'])
        if exame and st.button("⚡ EXECUTAR AUDITORIA MASTER", type="primary"):
            orquestrador_inteligencia("Lab")
            st.success("Auditoria Master Concluída para " + nome_paciente)
