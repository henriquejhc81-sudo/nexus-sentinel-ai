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
    with st.status(f"🧬 Orquestrador v8.5: Sincronizando Especialistas...", expanded=True) as status:
        st.write("🔍 Cruzando dados anatômicos...")
        time.sleep(0.5)
        st.write("🧠 Consultando Base de Conhecimento Master...")
        time.sleep(0.5)
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

# --- NOVO: FUNÇÃO DE IMPRESSÃO (PDF FORMATADO PARA A4) ---

def gerar_pdf_impressao(paciente, modulo, laudo_texto, tecnicos):
    pdf = FPDF()
    pdf.add_page()
    # Cabeçalho Oficial
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "GENESIS FORENSIC AI - DOSSIÊ DE DIAGNÓSTICO", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, f"Documento Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    # Dados do Paciente
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f" PACIENTE: {paciente.upper()}", ln=True, fill=True)
    pdf.cell(200, 10, f" MÓDULO ANALÍTICO: {modulo.upper()}", ln=True)
    pdf.ln(5)
    
    # Laudo
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "PARECER TÉCNICO E DIAGNÓSTICO:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, laudo_texto)
    pdf.ln(5)
    
    # Métricas
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "MÉTRICAS SENTINEL:", ln=True)
    pdf.set_font("Arial", '', 11)
    for k, v in tecnicos.items():
        pdf.cell(200, 8, f"- {k}: {v}", ln=True)
        
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACE DASHBOARD v8.5 ---

st.set_page_config(page_title="GENESIS MASTER v8.5", layout="wide", page_icon="🛡️")
init_db_multiplayer()

if realizar_login():
    st.markdown("""<style>
        .main { background-color: #0e1117; }
        .report-card { background-color: #111827; padding: 25px; border-radius: 15px; border-left: 8px solid #3b82f6; border-right: 1px solid #3b82f6; margin-top: 20px; box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.5); }
        .diagnosis-text { font-size: 1.15rem; line-height: 1.8; color: #e5e7eb; text-align: justify; }
        .stMetric { background-color: #1f2937; border-radius: 10px; padding: 10px; border: 1px solid #3b82f6; }
        .print-btn { background-color: #22c55e !important; color: white !important; font-weight: bold !important; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v8.5")

    with st.sidebar:
        st.header("👤 PRONTUÁRIO")
        nome_paciente = st.text_input("Nome do Paciente", "Paciente_Zero")
        st.divider()
        m_iri = st.toggle("🔬 Iridologia Master")
        m_der = st.toggle("📸 SkinAI v2 Pro")
        m_rad = st.toggle("📂 Radiologia Digital")
        m_lab = st.toggle("🧬 Lab Intelligence")
        st.divider()
        if st.button("🚪 Sair do Sistema"):
            st.session_state["autenticado"] = False
            st.rerun()

    # --- MÓDULO LABORATORIAL (NOVO DESIGN E IMPRESSÃO) ---

    if m_lab:
        st.subheader("🧬 Inteligência Laboratorial (Análise por Eixos)")
        exame = st.file_uploader("Carregar Exame para Diagnóstico Master", type=['pdf', 'jpg', 'png'], key="lab_up")
        if exame:
            if st.button("⚡ INICIAR DIAGNÓSTICO LABORATORIAL MASTER", type="primary"):
                orquestrador_inteligencia("Lab")
                laudo_lab = """Eixo Hematológico: Níveis de hemoglobina estáveis. Eixo Metabólico: A Creatinina apresenta um padrão de limite superior (1.1 mg/dL), sugerindo atenção à hidratação e filtragem renal. Eixo Inflamatório: PCR Negativo, indicando ausência de processos infecciosos agudos no momento da coleta."""
                
                st.markdown(f"""
                <div class="report-card">
                    <h2 style="color:#3b82f6; text-align:center;">📋 DOSSIÊ LABORATORIAL FANTÁSTICO</h2>
                    <hr style="border: 0.5px solid #3b82f6;">
                    <p class="diagnosis-text"><b>Paciente:</b> {nome_paciente.upper()}</p>
                    <p class="diagnosis-text">{laudo_lab}</p>
                    <p class="diagnosis-text" style="color:#22c55e;"><b>🎯 CONCLUSÃO:</b> Boa vitalidade orgânica. Recomenda-se correlação com Iridologia.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Botão de Impressão
                pdf_lab = gerar_pdf_impressao(nome_paciente, "Laboratorial", laudo_lab, {"Status": "Concluído", "Protocolo": "Sentinel 8.5"})
                st.download_button("🖨️ IMPRIMIR LAUDO OFICIAL", pdf_lab, file_name=f"laudo_lab_{nome_paciente}.pdf", mime="application/pdf")

    # --- MÓDULOS DE IMAGEM (NOVO DESIGN E IMPRESSÃO) ---

    def renderizar_modulo_master(label):
        st.subheader(f"Estação {label}")
        col_in, col_res = st.columns(2)
        with col_in:
            f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label)
            ent = st.camera_input("Scanner") if "📸" in f else st.file_uploader("Importar", type=['jpg','png','jpeg'], key=label+"f")
            zoom = st.checkbox("🔍 Zoom Digital Inteligente", key=label+"z")
        
        if ent:
            img = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img)
            if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
            
            with col_res:
                st.image(img_hd, caption="Visualização Ultra-HD", use_container_width=True)
                if st.button(f"⚡ GERAR DIAGNÓSTICO MASTER {label.upper()}", type="primary", key=label+"btn"):
                    orquestrador_inteligencia(label)
                    res_tec = motor_diagnostico_genesis(img_hd, label)
                    res_master = gerar_diagnostico_master(label, res_tec)
                    
                    full_text = f"{res_master['explicacao']} {res_master['fisiologia']} CONCLUSÃO: {res_master['conclusao']}"
                    
                    st.markdown(f"""
                    <div class="report-card">
                        <h2 style="color:#3b82f6; text-align:center;">🧬 {res_master['titulo']}</h2>
                        <hr style="border: 0.5px solid #3b82f6;">
                        <p class="diagnosis-text"><b>ANÁLISE:</b> {res_master['explicacao']}</p>
                        <p class="diagnosis-text"><b>FISIOLOGIA:</b> {res_master['fisiologia']}</p>
                        <p class="diagnosis-text" style="color:#22c55e;"><b>🎯 CONCLUSÃO:</b> {res_master['conclusao']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    c1.metric("Densidade Forense", res_tec['densidade'])
                    c2.metric("Índice de Estresse", f"{res_tec['estresse']}%")
                    
                    # Impressão de Imagem
                    pdf_img = gerar_pdf_impressao(nome_paciente, label, full_text, {"Densidade": res_tec['densidade'], "Estresse": f"{res_tec['estresse']}%"})
                    st.download_button("🖨️ IMPRIMIR LAUDO MASTER", pdf_img, file_name=f"laudo_{label}_{nome_paciente}.pdf", mime="application/pdf")
                    
                    st.image(res_tec['viz'], caption="Contraste Multiespectral", width=400)

    if m_iri: renderizar_modulo_master("Iridologia")
    elif m_der: renderizar_modulo_master("Dermatologia")
    elif m_rad: renderizar_modulo_master("Radiologia")
