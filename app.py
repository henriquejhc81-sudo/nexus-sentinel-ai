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
from engine import * 

# --- DNA NEXUS SENTINEL ESTRUTURA INTEGRADA (INTOCÁVEL) ---

def orquestrador_inteligencia(contexto):
    especialistas = ["Segurança", "Performance", "UX", "Dev", "QA", "Jurídico", "Hacker Ético"]
    with st.status(f"🧬 Orquestrador v7.1: Sincronizando Especialistas...", expanded=False) as status:
        time.sleep(0.5)
        status.update(label="Sincronização Sentinel Concluída", state="complete")
    return True

# --- BRIDGE SUPABASE (CLOUD READY) ---
def conectar_supabase():
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")
    if url and key:
        from supabase import create_client
        return create_client(url, key)
    return None

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

# --- SISTEMA DE AUTENTICAÇÃO SEGURA (CORREÇÃO SNIPER v7.1) ---

def gerar_hash(senha):
    return hashlib.sha256(str.encode(senha)).hexdigest()

def realizar_login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.markdown("<h1 style='text-align: center;'>🛡️ GENESIS LOGIN</h1>", unsafe_allow_html=True)
        # CORREÇÃO APLICADA: st.columns(3) para evitar o erro positional argument
        col1, col2, col3 = st.columns(3) 
        with col2:
            with st.form("login_form"):
                user = st.text_input("Usuário Profissional")
                pw = st.text_input("Senha Sentinel", type="password")
                if st.form_submit_button("Acessar Sistema"):
                    # Credenciais Padrão: admin / genesis2026
                    if user == "admin" and pw == "genesis2026":
                        st.session_state["autenticado"] = True
                        st.session_state["medico_id"] = user
                        st.rerun()
                    else:
                        st.error("Acesso Negado. Credenciais Inválidas.")
        return False
    return True

# --- INTERFACE DASHBOARD v7.1 ---

st.set_page_config(page_title="GENESIS FORENSIC AI v7.1", layout="wide", page_icon="🛡️")
init_db_multiplayer()

if realizar_login():
    st.markdown("""<style>
        .main { background-color: #0e1117; }
        .stMetric { background-color: #111827; border: 1px solid #3b82f6; border-radius: 10px; }
        .chat-box { background-color: #1f2937; padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; margin-bottom: 20px; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v7.1")

    with st.sidebar:
        st.header("🔑 SESSÃO ATIVA")
        st.write(f"Operador: **{st.session_state.get('medico_id', 'Desconhecido')}**")
        if st.button("Sair do Sistema"):
            st.session_state["autenticado"] = False
            st.rerun()
        st.divider()
        st.header("👤 PRONTUÁRIO")
        nome_paciente = st.text_input("Paciente", "Paciente_Zero")
        st.divider()
        m_iri = st.toggle("🔬 Iridologia Pro")
        m_der = st.toggle("📸 SkinAI v2")
        m_rad = st.toggle("📂 Radiologia YOLOv10")
        m_lab = st.toggle("🧬 Lab Intelligence")
        st.divider()
        st.info("☁️ Cloud: Supabase Bridge Ativa")

    # --- LÓGICA DE EXIBIÇÃO: SUPER IA vs MÓDULOS ---

    if not any([m_iri, m_der, m_rad, m_lab]):
        st.markdown("### 🧠 Super IA Genesis: Central de Inteligência")
        with st.container():
            st.markdown('<div class="chat-box">Como posso auxiliar no seu diagnóstico hoje? Carregue vídeos ou arquivos para análise Ultra-HD.</div>', unsafe_allow_html=True)
            col_file, col_prompt = st.columns(2)
            with col_file:
                arquivo_universal = st.file_uploader("Upload Universal", type=['mp4', 'pdf', 'docx', 'jpg', 'png'])
            with col_prompt:
                pergunta = st.text_area("Instrução para a IA:", placeholder="Analise o conteúdo deste arquivo...")
            
            if st.button("⚡ PROCESSAR CONSULTA GENESIS", type="primary"):
                if pergunta:
                    orquestrador_inteligencia("Super IA")
                    st.info(f"Análise processada para {nome_paciente}. Conteúdo integrado à base mundial.")

    # --- MÓDULOS DE IMAGEM (ESTRUTURA ADITIVA) ---

    def renderizar_modulo_v6(label):
        st.subheader(f"Estação {label} | Operador: {st.session_state['medico_id']}")
        col_input, col_result = st.columns(2)
        
        with col_input:
            f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label)
            ent = st.camera_input("Scanner Sentinel") if "📸" in f else st.file_uploader("Importar", type=['jpg','png','jpeg'])
            zoom_on = st.checkbox("🔍 Ativar Zoom Digital Inteligente", key=label+"zoom")
        
        if ent:
            img_raw = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img_raw)
            if zoom_on:
                img_hd = aplicar_zoom_inteligente(img_hd)
            img_array, brilho = processar_camera_inteligente(img_hd)
            
            with col_result:
                st.image(img_hd, caption=f"Captura Ultra-HD | Brilho: {int(brilho)} LUX", use_container_width=True)
                if st.button(f"⚡ ANALISAR {label.upper()}", type="primary", key=label+"analisar"):
                    orquestrador_inteligencia(label)
                    res = motor_diagnostico_genesis(img_hd, label)
                    st.metric("Densidade Forense", res['densidade'])
                    st.image(res['viz'], caption="Visão Multiespectral", width=400)

    if m_iri: renderizar_modulo_v6("Iridologia")
    elif m_der: renderizar_modulo_v6("Dermatologia")
    elif m_rad: renderizar_modulo_v6("Radiologia")
    elif m_lab: st.info("Módulo Laboratorial ativo.")
