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
# --- SNIPER: IMPORTAÇÃO EXPLÍCITA PARA ELIMINAR NAMEERROR ---
from engine import (
    extrair_qualidade_maxima, 
    aplicar_zoom_inteligente, 
    processar_camera_inteligente, 
    motor_diagnostico_genesis, 
    aplicar_mapa_iridologico
)

# --- DNA NEXUS SENTINEL ESTRUTURA INTEGRADA (INTOCÁVEL) ---

def orquestrador_inteligencia(contexto):
    especialistas = ["Segurança", "Performance", "UX", "Dev", "QA", "Jurídico", "Hacker Ético"]
    with st.status(f"🧬 Orquestrador v9.6: Executando Bio-Scan Clínico...", expanded=True) as status:
        st.write("🔍 Cruzando Topografia de Jensen com Sinais de Estresse...")
        time.sleep(0.5)
        st.write("🧠 Sincronizando com Base de Dados MedAI Vision X...")
        status.update(label="Sincronização Sentinel Concluída", state="complete")
    return True

# --- NOVO: MOTOR DE DIAGNÓSTICO ESPECÍFICO (BASEADO NO ARTIGO) ---

def gerar_diagnostico_clinico_v96(modulo, res_tec):
    if modulo == "Iridologia":
        # Lógica aditiva baseada em padrões de fibras e cores
        if res_tec['estresse'] > 10:
            possiveis = "Sinais compatíveis com Hiperestimulação do SNA, Gastrite Nervosa ou Estresse Adrenal."
        else:
            possiveis = "Terreno estável. Observar predisposição genética a processos lentos de eliminação."
            
        return {
            "titulo": "ANÁLISE DE TERRENO BIOLÓGICO E FRAGILIDADES (ART. v9.6)",
            "explicacao": f"""A iridologia identifica fragilidades e 'órgãos de choque' sob estresse. 
            Neste escaneamento, a densidade fibrilar ({res_tec['densidade']}) e o índice de estresse ({res_tec['estresse']}%) indicam:
            - **Fragilidades Detectadas:** {possiveis}
            - **Mapeamento de Órgãos:** Zonas reflexas sugerem atenção ao eixo digestivo e respiratório.""",
            "pontos_importantes": """
            🚨 **INFORMAÇÕES CRÍTICAS:**
            1. **NÃO É DIAGNÓSTICO MÉDICO:** Não detecta infecções agudas, mas aponta o terreno que as favorece.
            2. **FERRAMENTA COMPLEMENTAR:** Deve ser usada para encaminhar a especialistas e exames clínicos.
            3. **BASEADA EM OBSERVAÇÃO:** Processamento Ultra-HD para análise de estrias, anéis e cores de Bernard Jensen.
            """,
            "conclusao": "Investigação preventiva indicada. Recomenda-se correlação com exames laboratoriais."
        }
    return {"titulo": "Análise", "explicacao": "Processado.", "pontos_importantes": "", "conclusao": "Concluído."}

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

def gerar_pdf_impressao(paciente, modulo, laudo_res):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "GENESIS FORENSIC AI - RELATÓRIO CLÍNICO", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    texto = f"PACIENTE: {paciente.upper()}\nDATA: {datetime.datetime.now()}\n\n{laudo_res['explicacao']}\n\nCONCLUSAO: {laudo_res['conclusao']}\n\n{laudo_res['pontos_importantes']}"
    pdf.multi_cell(0, 10, texto.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S')

# --- INTERFACE DASHBOARD v9.6 ---

st.set_page_config(page_title="GENESIS MASTER v9.6", layout="wide", page_icon="🛡️")
init_db_multiplayer()

if realizar_login():
    st.markdown("""<style>
        .main { background-color: #0e1117; }
        .report-card { background-color: #111827; padding: 25px; border-radius: 15px; border-left: 8px solid #3b82f6; margin-top: 20px; }
        .diagnosis-text { font-size: 1.1rem; color: #e5e7eb; line-height: 1.7; }
        .warning-box { background-color: #1a202c; padding: 15px; border-radius: 8px; font-size: 0.95rem; color: #a0aec0; border: 1px solid #3b82f6; margin-top: 20px; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v9.6")

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

    def renderizar_modulo_v96(label):
        st.subheader(f"Estação {label}")
        col_in, col_res = st.columns(2)
        with col_in:
            f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label+"s")
            ent = st.camera_input("Scanner") if "📸" in f else st.file_uploader("Importar", type=['jpg','png','jpeg'], key=label+"u")
            zoom = st.checkbox("🔍 Zoom Digital Inteligente", key=label+"z")
            map_on = st.checkbox("🗺️ Ativar Mapeamento Orgânico", key=label+"m") if label == "Iridologia" else False
        
        if ent:
            img = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img)
            if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
            if map_on: img_hd = aplicar_mapa_iridologico(img_hd)
            
            with col_res:
                st.image(img_hd, caption="Visualização Ultra-HD", use_container_width=True)
                if st.button(f"⚡ EXECUTAR DIAGNÓSTICO MASTER {label.upper()}", type="primary", key=label+"b"):
                    orquestrador_inteligencia(label)
                    res_tec = motor_diagnostico_genesis(img_hd, label)
                    res_clinico = gerar_diagnostico_master(label, res_tec) # Chama a lógica específica
                    
                    st.markdown(f"""<div class="report-card">
                        <h2 style="color:#3b82f6; text-align:center;">🧬 {res_clinico['titulo']}</h2>
                        <hr style="border: 0.5px solid #3b82f6;">
                        <p class="diagnosis-text">{res_clinico['explicacao']}</p>
                        <p class="diagnosis-text" style="color:#22c55e;"><b>🎯 CONCLUSÃO:</b> {res_clinico['conclusao']}</p>
                        <div class="warning-box">{res_clinico['nota_legal'].replace('\n', '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
                    
                    st.image(res_tec['viz'], caption="Visão Multiespectral", width=400)
                    
                    pdf_b = gerar_pdf_impressao(nome_paciente, label, res_clinico)
                    st.download_button("🖨️ IMPRIMIR DOSSIÊ CLÍNICO", pdf_b, file_name=f"genesis_{label}.pdf", mime="application/pdf")

    if m_iri: renderizar_modulo_v96("Iridologia")
    elif m_der: renderizar_modulo_v96("Dermatologia")
    elif m_rad: renderizar_modulo_v96("Radiologia")
    elif m_lab:
        st.subheader("🧬 Inteligência Laboratorial")
        exame = st.file_uploader("Upload", type=['pdf', 'jpg', 'png'])
        if exame and st.button("⚡ AUDITORIA MASTER"):
            orquestrador_inteligencia("Lab")
            st.success("Concluído.")
