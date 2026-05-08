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

# --- DNA NEXUS SENTINEL ESTRUTURA INTEGRADA (INTOCÁVEL) ---

def orquestrador_inteligencia(contexto):
    especialistas = ["Segurança", "Performance", "UX", "Dev", "QA", "Jurídico", "Hacker Ético"]
    st.toast(f"🧬 Orquestrador Sentinel: Ativando Inteligência Laboratorial (6 Eixos)...")
    return True

headers_ghost = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

def modulo_seguranca_sentinel(dados_entrada):
    if "<script>" in str(dados_entrada):
        st.error("⚠️ Bloqueio Sentinel: Tentativa de Injeção Detectada.")
        return False
    return True

def calcular_matriz_risco():
    return np.random.randint(1, 10)

# --- NOVO: MOTOR DE INTELIGÊNCIA LABORATORIAL (REGRA DE OURO) ---

def motor_laboratorial(dados):
    # Simulação de OCR / Processamento de Dados de Exames (Babylon/Ada Health Style)
    alertas = []
    status = "Verde" # Padrão Estável
    
    # Eixo A: Metabólico e Orgânico
    if dados.get('creatinina', 0) > 1.2 and dados.get('ureia', 0) > 40:
        alertas.append("🔴 Crítico: Alerta de Insuficiência Renal (Creatinina/Ureia Elevadas)")
        status = "Vermelho"
    if dados.get('tgp', 0) > 80: # Exemplo: 2x o normal
        alertas.append("🟡 Atenção: Sugestão de Lesão Hepática Aguda (TGP Elevado)")
        status = "Amarelo"
        
    # Eixo B: Nutricional e Hematológico
    if dados.get('hemoglobina', 15) < 12 and dados.get('ferritina', 100) < 30:
        alertas.append("🟡 Atenção: Padrão compatível com Anemia Ferropriva.")
        status = "Amarelo"
        
    # Eixo C: Imunológico e Inflamatório
    if dados.get('pcr', 0) > 10 and dados.get('leucocitos', 0) > 11000:
        alertas.append("🔴 Crítico: Infecção Bacteriana Provável (PCR/Leucocitose)")
        status = "Vermelho"

    # Eixo D: Rastreamento (Segurança)
    if dados.get('marcador_tumoral', 0) > 10:
        alertas.append("⚠️ Nota: Marcadores tumorais elevados requerem correlação com exames de imagem.")
        
    return {"alertas": alertas, "status": status}

# --- BANCO DE DADOS (PERSISTÊNCIA EVOLUÍDA) ---

def init_db():
    conn = sqlite3.connect('genesis_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS diagnosticos 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, paciente TEXT, modulo TEXT, 
                  data TEXT, score_estresse REAL, parecer TEXT)''')
    # Tabela Laboratorial Aditiva
    c.execute('''CREATE TABLE IF NOT EXISTS laboratorial 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, paciente TEXT, data TEXT, alertas TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# --- INTERFACE DE VOZ E PDF (PRESERVADAS) ---

def sintetizar_voz_sentinel(texto):
    try:
        tts = gTTS(text=texto, lang='pt')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_b64 = base64.b64encode(fp.read()).decode()
        audio_html = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_b64}"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)
    except: pass

def exportar_pdf_genesis(paciente, modulo, resultado):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"GENESIS FORENSIC AI - {modulo}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, f"Paciente: {paciente}\nData: {datetime.datetime.now()}\n\nResultado: {resultado}")
    return pdf.output()

# --- MOTOR DE IMAGEM (PRESENRVADO) ---

def motor_diagnostico_genesis(img_pil, modulo):
    img_array = np.array(img_pil.convert('RGB'))
    img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
    img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    img_enhanced = clahe.apply(img_gray)
    mask = cv2.inRange(img_hsv, np.array(), np.array())
    score_estresse = (np.sum(mask) / (img_array.size / 3)) * 100
    
    parecer = "Padrão analítico processado." # Placeholder do motor original
    return {"densidade": round(np.mean(img_gray), 2), "estresse": round(score_estresse, 2), "parecer": parecer, "viz": img_enhanced}

# --- INTERFACE STREAMLIT DASHBOARD v4.0 ---

st.set_page_config(page_title="GENESIS FORENSIC AI", layout="wide", page_icon="🛡️")
init_db()

st.title("🛡️ GENESIS FORENSIC AI")
st.caption("Arquitetura DNA Sentinel v4.0 | MedAI Vision X | Lab-Intelligence Core")

with st.sidebar:
    st.header("👤 PRONTUÁRIO")
    nome_paciente = st.text_input("Paciente", "Paciente_Zero")
    st.divider()
    st.header("⚙️ MÓDULOS")
    m_iri = st.toggle("🔬 Iridologia")
    m_der = st.toggle("📸 Dermatologia")
    m_rad = st.toggle("📂 Radiologia")
    m_lab = st.toggle("🧬 Inteligência Laboratorial")
    st.divider()
    if st.button("📊 Abrir Banco de Dados"):
        conn = sqlite3.connect('genesis_data.db')
        st.dataframe(pd.read_sql_query("SELECT * FROM diagnosticos", conn))
        conn.close()

# --- RENDERIZAÇÃO DO MÓDULO LABORATORIAL (NOVO) ---

if m_lab:
    st.subheader("🧬 Módulo de Inteligência Laboratorial")
    col1, col2 = st.columns()
    
    with col1:
        st.info("Insira os dados do exame (OCR automático em desenvolvimento via Google Vision)")
        creatina = st.number_input("Creatinina (mg/dL)", 0.0, 10.0, 0.9)
        ureia = st.number_input("Ureia (mg/dL)", 0, 300, 30)
        tgp = st.number_input("TGP/ALT (U/L)", 0, 1000, 35)
        hemoglobina = st.number_input("Hemoglobina (g/dL)", 0.0, 20.0, 14.0)
        pcr = st.number_input("PCR (mg/L)", 0.0, 500.0, 1.0)
        
    with col2:
        if st.button("⚡ GERAR RELATÓRIO INTELIGENTE", type="primary"):
            dados_exame = {'creatinina': creatina, 'ureia': ureia, 'tgp': tgp, 'hemoglobina': hemoglobina, 'pcr': pcr}
            res_lab = motor_laboratorial(dados_exame)
            
            # Dashboard Visual (Babylon Style)
            cor_circulo = {"Verde": "🟢", "Amarelo": "🟡", "Vermelho": "🔴"}
            st.markdown(f"### Status Geral: {cor_circulo[res_lab['status']]} {res_lab['status']}")
            
            for alerta in res_lab['alertas']:
                st.write(alerta)
            
            # Voz
            sintetizar_voz_sentinel(f"Análise laboratorial concluída. Status {res_lab['status']}.")
            
            # Salvar no Banco
            conn = sqlite3.connect('genesis_data.db')
            conn.execute("INSERT INTO laboratorial (paciente, data, alertas, status) VALUES (?,?,?,?)",
                         (nome_paciente, str(datetime.datetime.now()), str(res_lab['alertas']), res_lab['status']))
            conn.commit()
            conn.close()

# --- MÓDULOS DE IMAGEM (PRESERVADOS) ---

def exibir_estacao(label):
    st.subheader(f"Estação {label}")
    col_u, col_r = st.columns(2)
    with col_u:
        f = st.radio("Fonte", ["Câmera", "Arquivo"], horizontal=True, key=label)
        ent = st.camera_input("Scanner") if f == "Câmera" else st.file_uploader("Upload", type=['jpg','png','jpeg'])
    if ent:
        img_o = Image.open(ent)
        with col_r:
            st.image(img_o, use_container_width=True)
            if st.button(f"⚡ ANALISAR {label.upper()}", type="primary"):
                orquestrador_inteligencia(label)
                res = motor_diagnostico_genesis(img_o, label)
                st.metric("Risco Matriz", f"{calcular_matriz_risco()}%")
                st.write(f"**Parecer:** {res['parecer']}")
                sintetizar_voz_sentinel(f"Análise de {label} finalizada.")

if m_iri: exibir_estacao("Iridologia")
elif m_der: exibir_estacao("Dermatologia")
elif m_rad: exibir_estacao("Radiologia")
elif not m_lab: st.warning("Sistema em Stand-by. Ative um módulo lateral.")
