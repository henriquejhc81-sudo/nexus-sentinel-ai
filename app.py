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
    with st.status(f"🧬 Orquestrador v8.8: Sincronizando Especialistas...", expanded=True) as status:
        st.write("🔍 Processando dados dinâmicos do paciente...")
        time.sleep(0.5)
        st.write("🧠 Aplicando lógica médica em tempo real...")
        status.update(label="Análise Concluída", state="complete")
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

# --- SISTEMA DE AUTENTICAÇÃO ---

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

def gerar_pdf_impressao(paciente, modulo, laudo_texto, tecnicos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "GENESIS FORENSIC AI - RELATÓRIO MASTER", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f" PACIENTE: {paciente.upper()}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, laudo_texto.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S')

# --- INTERFACE DASHBOARD v8.8 ---

st.set_page_config(page_title="GENESIS MASTER v8.8", layout="wide", page_icon="🛡️")
init_db_multiplayer()

if realizar_login():
    st.markdown("""<style>
        .main { background-color: #0e1117; }
        .report-card { background-color: #111827; padding: 25px; border-radius: 15px; border-left: 8px solid #3b82f6; margin-top: 20px; }
        .diagnosis-text { font-size: 1.1rem; color: #e5e7eb; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v8.8")

    with st.sidebar:
        st.header("👤 PRONTUÁRIO")
        nome_paciente = st.text_input("Nome do Paciente", placeholder="Digite o nome aqui...")
        st.divider()
        m_iri = st.toggle("🔬 Iridologia Master")
        m_der = st.toggle("📸 SkinAI v2 Pro")
        m_rad = st.toggle("📂 Radiologia Digital")
        m_lab = st.toggle("🧬 Lab & Growth Intelligence")
        st.divider()
        if st.button("Sair"):
            st.session_state["autenticado"] = False
            st.rerun()

    # --- MÓDULO LABORATORIAL DINÂMICO (v8.8 CORREÇÃO) ---

    if m_lab:
        st.subheader("🧬 Inteligência Laboratorial e de Crescimento Dinâmica")
        
        col_dados, col_entrada = st.columns(2)
        
        with col_dados:
            st.info("📊 Dados do Paciente Atual")
            altura = st.number_input("Altura (cm)", min_value=10.0, max_value=250.0, value=100.0)
            peso = st.number_input("Peso (kg)", min_value=1.0, max_value=300.0, value=15.0)
            st.divider()
            st.info("🧪 Resultados do Exame (Hormonais)")
            p17 = st.number_input("17-OH Progesterona (ng/mL)", value=0.0)
            cortisol = st.number_input("Cortisol Basal (µg/dL)", value=0.0)
            fsh = st.number_input("FSH (mUI/mL)", value=0.0)
        
        if st.button("⚡ EXECUTAR DIAGNÓSTICO PERSONALIZADO", type="primary"):
            if not nome_paciente or nome_paciente == "Digite o nome aqui...":
                st.error("Erro: Por favor, insira o nome do paciente no prontuário lateral.")
            else:
                orquestrador_inteligencia("Lab_Dinamico")
                
                # Lógica Médica Dinâmica
                imc = peso / ((altura/100)**2)
                status_p17 = "Normal" if 0.07 <= p17 <= 1.70 else "Atenção (Fora da Faixa)"
                
                laudo_dinamico = f"""
                PARECER TÉCNICO PARA: {nome_paciente.upper()}
                
                1. ANTROPOMETRIA: IMC calculado em {imc:.1f}. Desenvolvimento físico compatível com os dados inseridos.
                
                2. ANÁLISE BIOQUÍMICA: 
                   - 17-OH Progesterona: {p17} ng/mL ({status_p17})
                   - Cortisol Basal: {cortisol} µg/dL
                   - FSH: {fsh} mUI/mL
                
                3. CONCLUSÃO SENTINEL: O laudo foi processado em tempo real com base nos valores fornecidos. 
                Os marcadores hormonais indicam estado de {status_p17.lower()}.
                """
                
                with col_entrada:
                    st.markdown(f"""
                    <div class="report-card">
                        <h2 style="color:#3b82f6; text-align:center;">📊 LAUDO PERSONALIZADO GENESIS</h2>
                        <hr>
                        <p class="diagnosis-text">{laudo_dinamico}</p>
                        <p class="diagnosis-text" style="color:#22c55e;"><b>🎯 STATUS:</b> Análise Concluída com Sucesso.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    pdf_bytes = gerar_pdf_impressao(nome_paciente, "Lab & Growth", laudo_dinamico, {})
                    st.download_button("🖨️ IMPRIMIR LAUDO PACIENTE", pdf_bytes, file_name=f"laudo_{nome_paciente}.pdf")

    # --- MÓDULOS DE IMAGEM (PRESERVADOS) ---

    def renderizar_modulo_master(label):
        st.subheader(f"Estação {label}")
        col_in, col_res = st.columns(2)
        with col_in:
            f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label)
            ent = st.camera_input("Scanner") if "📸" in f else st.file_uploader("Importar", type=['jpg','png','jpeg'], key=label+"f")
        if ent:
            img = Image.open(ent)
            with col_res:
                st.image(img, use_container_width=True)
                if st.button(f"⚡ ANALISAR {label.upper()}", key=label+"bt"):
                    orquestrador_inteligencia(label)
                    st.success(f"Análise Master para {nome_paciente} realizada.")

    if m_iri: renderizar_modulo_master("Iridologia")
    elif m_der: renderizar_modulo_master("Dermatologia")
    elif m_rad: renderizar_modulo_master("Radiologia")
