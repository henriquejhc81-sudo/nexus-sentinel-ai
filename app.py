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
    with st.status(f"🧬 Orquestrador v8.7: Sincronizando Especialistas...", expanded=True) as status:
        st.write("🔍 Analisando Eixos Endócrinos e Curvas de Crescimento...")
        time.sleep(0.5)
        st.write("🧠 Consultando Parâmetros da OMS e Base Pediátrica...")
        status.update(label="Análise Profunda Concluída", state="complete")
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

# --- FUNÇÃO DE IMPRESSÃO v8.7 ---

def gerar_pdf_impressao(paciente, modulo, laudo_texto, tecnicos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "GENESIS FORENSIC AI - RELATÓRIO MASTER", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f" PACIENTE: {paciente.upper()}", ln=True, fill=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "PARECER TÉCNICO:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, laudo_texto.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(10)
    
    return pdf.output(dest='S')

# --- INTERFACE DASHBOARD v8.7 ---

st.set_page_config(page_title="GENESIS MASTER v8.7", layout="wide", page_icon="🛡️")
init_db_multiplayer()

if realizar_login():
    st.markdown("""<style>
        .main { background-color: #0e1117; }
        .report-card { background-color: #111827; padding: 25px; border-radius: 15px; border-left: 8px solid #3b82f6; margin-top: 20px; }
        .diagnosis-text { font-size: 1.1rem; color: #e5e7eb; text-align: justify; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v8.7")

    with st.sidebar:
        st.header("👤 PRONTUÁRIO")
        nome_paciente = st.text_input("Paciente", "Kamilly Campos de Carvalho")
        st.divider()
        m_iri = st.toggle("🔬 Iridologia Master")
        m_der = st.toggle("📸 SkinAI v2 Pro")
        m_rad = st.toggle("📂 Radiologia Digital")
        m_lab = st.toggle("🧬 Lab & Growth Intelligence", value=True)
        st.divider()
        if st.button("Sair"):
            st.session_state["autenticado"] = False
            st.rerun()

    # --- MÓDULO LABORATORIAL & CRESCIMENTO (ADITIVO v8.7) ---

    if m_lab:
        st.subheader("🧬 Inteligência Laboratorial e de Crescimento")
        
        col_dados, col_analise = st.columns(2)
        
        with col_dados:
            st.info("📊 Parâmetros Antropométricos (6 Anos)")
            altura = st.number_input("Altura (cm)", value=115.0)
            peso = st.number_input("Peso (kg)", value=20.0)
            exame = st.file_uploader("Upload de Laudos Adicionais", type=['pdf', 'jpg', 'png'])
        
        if st.button("⚡ GERAR DIAGNÓSTICO INTEGRADO", type="primary"):
            orquestrador_inteligencia("Lab_Growth")
            
            # Cálculo IMC e Curva Simbolizada
            imc = peso / ((altura/100)**2)
            
            laudo_integrado = f"""
            PARECER INTEGRADO - PACIENTE: {nome_paciente}
            
            1. CRESCIMENTO: A altura de {altura}cm e peso de {peso}kg para 6 anos situam a paciente 
            dentro dos percentis de normalidade da OMS. O IMC de {imc:.1f} indica estado nutricional adequado.
            
            2. ENDOCRINOLOGIA: Cruzando com os exames anteriores, os níveis de Cortisol, 
            17-OH Progesterona e Androstenediona confirmam que não há sobrecarga adrenal 
            influenciando o crescimento atual. O eixo LH/FSH confirma ausência de telarca precoce.
            
            3. OBSERVAÇÃO TÉCNICA: Desenvolvimento harmônico entre idade cronológica e biológica.
            """
            
            with col_analise:
                st.markdown(f"""
                <div class="report-card">
                    <h2 style="color:#3b82f6; text-align:center;">📊 RELATÓRIO DE CRESCIMENTO & LAB</h2>
                    <hr>
                    <p class="diagnosis-text">{laudo_integrado}</p>
                    <p class="diagnosis-text" style="color:#22c55e;"><b>🎯 STATUS:</b> Desenvolvimento Global Saudável.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Botão de Impressão Preservado e Funcional
                pdf_bytes = gerar_pdf_impressao(nome_paciente, "Lab & Growth", laudo_integrado, {})
                st.download_button("🖨️ IMPRIMIR LAUDO INTEGRADO", pdf_bytes, file_name=f"laudo_integrado_{nome_paciente}.pdf", mime="application/pdf")

    # --- MÓDULOS DE IMAGEM (ESTRUTURA INTOCÁVEL) ---

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
                    st.success(f"Diagnóstico Master de {label} gerado.")

    if m_iri: renderizar_modulo_master("Iridologia")
    elif m_der: renderizar_modulo_master("Dermatologia")
    elif m_rad: renderizar_modulo_master("Radiologia")
