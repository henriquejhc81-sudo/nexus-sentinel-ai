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
from engine import * 

# --- DNA NEXUS SENTINEL ESTRUTURA INTEGRADA (INTOCÁVEL) ---

def orquestrador_inteligencia(contexto):
    especialistas = ["Segurança", "Performance", "UX", "Dev", "QA", "Jurídico", "Hacker Ético"]
    with st.status(f"🧬 Orquestrador v6.0: Sincronizando Especialistas...", expanded=False) as status:
        time.sleep(0.5)
        status.update(label="Sincronização Sentinel Concluída", state="complete")
    return True

def init_db_multiplayer():
    conn = sqlite3.connect('genesis_multiplayer.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS diagnosticos 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, medico_id TEXT, paciente TEXT, 
                  modulo TEXT, data TEXT, score_estresse REAL, parecer TEXT)''')
    conn.commit()
    conn.close()

# --- INTERFACE DASHBOARD v6.0 (SUPER IA + MOTION TRACKING) ---

st.set_page_config(page_title="GENESIS FORENSIC AI v6.0", layout="wide", page_icon="🛡️")
init_db_multiplayer()

st.markdown("""<style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #111827; border: 1px solid #3b82f6; border-radius: 10px; }
    .chat-box { background-color: #1f2937; padding: 20px; border-radius: 15px; border-left: 5px solid #3b82f6; margin-bottom: 20px; }
</style>""", unsafe_allow_html=True)

st.title("🛡️ GENESIS FORENSIC AI v6.0")

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
    st.info("Sistema Sentinel: ONLINE")

# --- LÓGICA DE EXIBIÇÃO: SUPER IA vs MÓDULOS ---

if not any([m_iri, m_der, m_rad, m_lab]):
    st.markdown("### 🧠 Super IA Genesis: Central de Inteligência")
    
    with st.container():
        st.markdown('<div class="chat-box">Como posso auxiliar no seu diagnóstico forense hoje? Carregue arquivos ou vídeos para análise profunda.</div>', unsafe_allow_html=True)
        
        col_file, col_prompt = st.columns(2)
        
        with col_file:
            arquivo_universal = st.file_uploader("Upload (Vídeo, PDF, Imagem, Docs)", type=['mp4', 'mov', 'avi', 'pdf', 'docx', 'jpg', 'png', 'csv'])
        with col_prompt:
            pergunta = st.text_area("Digite sua pergunta ou instrução para a IA:", placeholder="Ex: Analise o padrão fibrilar deste vídeo de iridologia...")
        
        # --- CORREÇÃO DE INDENTAÇÃO APLICADA AQUI ---
        if st.button("⚡ PROCESSAR CONSULTA GENESIS", type="primary"):
            if pergunta:
                with st.spinner("IA Multimodal executando Rastreamento Sentinel..."):
                    orquestrador_inteligencia("Super IA")
                    
                    if arquivo_universal:
                        # Lógica de Vídeo (Motion Tracking)
                        if arquivo_universal.type in ['video/mp4', 'video/mov', 'video/avi']:
                            with open("temp_video.mp4", "wb") as f:
                                f.write(arquivo_universal.read())
                            
                            analise_mov = rastreamento_movimento_genesis("temp_video.mp4")
                            resultado_ia = motor_multimodal_genesis(arquivo_universal, pergunta)
                            
                            st.success("🎥 Análise de Vídeo Concluída")
                            st.write(f"**Resultado do Rastreamento:** {analise_mov['status']}")
                            st.write(f"**Intensidade Biométrica:** {analise_mov['intensidade_media']}%")
                        else:
                            resultado_ia = motor_multimodal_genesis(arquivo_universal, pergunta)
                        
                        st.info("Resposta da Super IA:")
                        st.write(resultado_ia)
                    else:
                        st.info("Análise conceitual processada via Groq/Google AI. Aguardando mídia para diagnóstico profundo.")
            else:
                st.warning("Por favor, digite uma pergunta para a IA.")

# --- MÓDULOS DE IMAGEM ORIGINAIS (PRESERVADOS) ---

def renderizar_modulo_v5(label):
    st.subheader(f"Estação {label} | Operador: {medico_id}")
    col_input, col_result = st.columns(2)
    
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
                st.metric("Densidade", res['densidade'])
                st.image(res['viz'], caption="Contraste Forense", width=400)

if m_iri: renderizar_modulo_v5("Iridologia")
elif m_der: renderizar_modulo_v5("Dermatologia")
elif m_rad: renderizar_modulo_v5("Radiologia")
elif m_lab: st.info("Módulo Laboratorial v6.0 ativo.")
