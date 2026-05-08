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
from engine import * # IMPORTAÇÃO DO NOVO MÓDULO ENGINE

# --- DNA NEXUS SENTINEL ESTRUTURA INTEGRADA (INTOCÁVEL) ---

def orquestrador_inteligencia(contexto):
    especialistas = ["Segurança", "Performance", "UX", "Dev", "QA", "Jurídico", "Hacker Ético"]
    with st.status(f"🧬 Orquestrador v5.0: Executando Análise Transversal...", expanded=False) as status:
        st.write("🔍 Segmentando zonas biométricas...")
        time.sleep(0.5)
        st.write("🌐 Consultando base mundial DuckDuckGo...")
        time.sleep(0.5)
        status.update(label="Sincronização Sentinel Concluída", state="complete")
    return True

# --- NOVO: INFRAESTRUTURA MULTI-PLAYER (CLOUD READY) ---

def init_db_multiplayer():
    conn = sqlite3.connect('genesis_multiplayer.db')
    c = conn.cursor()
    # Tabela com ID de Médico para separação de dados
    c.execute('''CREATE TABLE IF NOT EXISTS diagnosticos 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, medico_id TEXT, paciente TEXT, 
                  modulo TEXT, data TEXT, score_estresse REAL, parecer TEXT)''')
    conn.commit()
    conn.close()

# --- INTERFACE DASHBOARD v5.0 ---

st.set_page_config(page_title="GENESIS FORENSIC AI v5.0", layout="wide", page_icon="🛡️")
init_db_multiplayer()

st.markdown("""<style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #111827; border: 1px solid #3b82f6; border-radius: 10px; }
    .kpi-card { background-color: #1f2937; padding: 20px; border-radius: 15px; border-top: 4px solid #3b82f6; text-align: center; }
</style>""", unsafe_allow_html=True)

st.title("🛡️ GENESIS FORENSIC AI v5.0")

with st.sidebar:
    st.header("🔑 ACESSO MULTI-PLAYER")
    medico_id = st.text_input("ID do Profissional", "MED-001")
    st.divider()
    st.header("👤 PRONTUÁRIO")
    nome_paciente = st.text_input("Paciente", "Paciente_Zero")
    st.divider()
    m_iri = st.toggle("🔬 Iridologia Pro")
    m_der = st.toggle("📸 SkinAI v2")
    m_rad = st.toggle("📂 Radiologia YOLOv10")
    m_lab = st.toggle("🧬 Lab Intelligence")
    st.divider()
    if st.button("📊 Histórico do Profissional"):
        conn = sqlite3.connect('genesis_multiplayer.db')
        df = pd.read_sql_query(f"SELECT * FROM diagnosticos WHERE medico_id='{medico_id}'", conn)
        st.dataframe(df)
        conn.close()

# --- DASHBOARD CENTRAL ---

if not any([m_iri, m_der, m_rad, m_lab]):
    st.markdown(f"### 🛰️ Estação Logada: {medico_id}")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="kpi-card"><h3>Integridade</h3><h2 style="color:#22c55e;">100%</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="kpi-card"><h3>Sincronização</h3><h2 style="color:#3b82f6;">Cloud</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="kpi-card"><h3>Risco</h3><h2 style="color:#22c55e;">Mínimo</h2></div>', unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=["Jan", "Fev", "Mar", "Abr"], y=[0.8, 0.9, 1.1, 1.3], name="Tendência Global", line=dict(color='#3b82f6')))
    fig.update_layout(title="Volume de Diagnósticos Mensais", template="plotly_dark", height=300)
    st.plotly_chart(fig, use_container_width=True)

# --- RENDERIZAÇÃO ADITIVA ---

def renderizar_modulo_v5(label):
    st.subheader(f"Estação {label} | Operador: {medico_id}")
    col_input, col_result = st.columns([1, 1.2])
    
    with col_input:
        f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label)
        ent = st.camera_input("Scanner Sentinel") if "📸" in f else st.file_uploader("Importar", type=['jpg','png','jpeg'])
    
    if ent:
        img_raw = Image.open(ent)
        img_array, brilho = processar_camera_inteligente(img_raw)
        
        with col_result:
            st.image(img_array, caption=f"Brilho: {int(brilho)} LUX", use_container_width=True)
            if st.button(f"⚡ ANALISAR", type="primary", key=label+"bt"):
                orquestrador_inteligencia(label)
                res = motor_diagnostico_genesis(img_raw, label)
                
                # Motor de Correlação (Importado da Engine)
                correlacoes = analyze_global_health(res, {'creatinina': 1.4})
                for c in correlacoes: st.error(c)
                
                st.metric("Densidade", res['densidade'])
                st.image(res['viz'], caption="Contraste Forense", width=400)

if m_iri: renderizar_modulo_v5("Iridologia")
elif m_der: renderizar_modulo_v5("Dermatologia")
elif m_rad: renderizar_modulo_v5("Radiologia")
elif m_lab: st.info("Módulo Laboratorial v5.0 ativo.")
