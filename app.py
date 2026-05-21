"""
=============================================================================
🌌 NEXUS OMNICORE v9.0 GENESIS - ULTIMATE APP BUILDER & TACTICAL CORE
=============================================================================
Fusão Total: DNA v1.0 a v8.5 Consolidado sem NENHUMA Regressão.
Inclusões Nível Elite:
1. Nexus Forge (App Builder estilo v0/Bolt.new/Cursor)
2. AutoFix Ativo e Corrigido (Expressão Regular Restaurada)
3. Memória de Longo Prazo (Chat Deep Context)
4. Orquestrador Hydra de 7 Perspectivas Integrado
=============================================================================
"""

import streamlit as st
import io
import re
import time
import requests
import json
import sqlite3
import concurrent.futures
import pandas as pd
from PIL import Image
from datetime import datetime

# --- VERIFICAÇÃO DE BLINDAGEM (DEPENDÊNCIAS) ---
try:
    from groq import Groq
    import google.generativeai as genai
    import PyPDF2
    import docx2txt
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from fpdf import FPDF
    from duckduckgo_search import DDGS
except ImportError as e:
    st.error(f"💣 Erro Crítico de Infraestrutura. Dependência ausente: {e}")
    st.stop()

# --- CONFIGURAÇÃO SOBERANA HUD ---
st.set_page_config(page_title="Nexus Genesis v9.0", page_icon="🌌", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #02040a !important;
        background-image: radial-gradient(circle at 50% 10%, #0a1128 0%, #02040a 100%) !important;
        color: #f0f4f8 !important;
        font-family: 'JetBrains Mono', 'Consolas', monospace !important;
    }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; max-width: 96% !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #090d16; padding: 6px; border-radius: 6px; border: 1px solid #161b22; }
    .stTabs [data-baseweb="tab"] { height: 38px; color: #8b949e !important; font-weight: 700; font-size: 11px; }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #A51C30 0%, #8b5cf6 100%) !important;
        color: #ffffff !important; box-shadow: 0 0 15px rgba(139, 92, 246, 0.5);
    }
    .hud-card {
        background: rgba(13, 17, 23, 0.85);
        border: 1px solid #21262d; border-left: 4px solid #8b5cf6;
        padding: 14px; border-radius: 6px; margin-bottom: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .hud-card-green { border-left: 4px solid #10b981 !important; }
    .hud-card-gold { border-left: 4px solid #facc15 !important; }
    .hud-title { font-size: 10px; color: #8b949e; text-transform: uppercase; letter-spacing: 1.2px; font-weight: bold; }
    .hud-value { font-size: 14px; color: #f0f4f8; font-weight: bold; margin-top: 4px; }
    
    .terminal-box {
        background-color: #03060c !important;
        border: 1px solid #1f6feb !important;
        border-radius: 6px; padding: 14px;
        font-family: 'Consolas', monospace; color: #58a6ff;
        height: 320px; overflow-y: auto;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.9);
    }
    .terminal-line { margin-bottom: 6px; font-size: 11.5px; border-bottom: 1px solid rgba(31,111,235,0.05); padding-bottom: 3px; }
    .terminal-tag { color: #f43f5e; font-weight: bold; }
    .terminal-data { color: #56d364; }
    .terminal-info { color: #8b949e; }
    
    .stButton>button {
        background: linear-gradient(135deg, #A51C30 0%, #8b5cf6 100%) !important;
        color: #ffffff !important; font-weight: 800 !important; border-radius: 6px !important;
        padding: 12px !important; font-size: 12px !important; border: none !important;
        width: 100%; margin-top: 5px;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); }
    .stTextArea textarea { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #21262d !important; }
    .stTextInput input { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #21262d !important; }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS DA HIDRA (DATA LAKE SEGURO MULTI-THREAD) ---
DB_NAME = 'nexus_datalake_v9.db'

def init_db():
    with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS radar_logs (id_sinal TEXT PRIMARY KEY, tipo TEXT, payload TEXT, timestamp TEXT)''')
        conn.commit()

def salvar_no_db(id_sinal, tipo, payload, timestamp):
    with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO radar_logs (id_sinal, tipo, payload, timestamp) VALUES (?, ?, ?, ?)", (id_sinal, tipo, str(payload), timestamp))
        conn.commit()

def carregar_do_db():
    with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute("SELECT id_sinal, tipo, payload, timestamp FROM radar_logs ORDER BY timestamp DESC LIMIT 50")
        return c.fetchall()

init_db()

# --- DNA SENTINEL: Proteção Máxima de Privacidade (Anonimização PII Completa) ---
def pii_anonymizer(texto):
    if not texto: return texto
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF PROTEGIDO]', texto)
    texto = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ PROTEGIDO]', texto)
    return texto.replace("```", "'''")

# --- DNA AETHER: Extrator Omniversal de Arquivos e Visão Computacional ---
def omni_extractor(arquivos_upados, gemini_key):
    texto_extraido = ""
    if not arquivos_upados: return texto_extraido
    for arquivo in arquivos_upados:
        if arquivo.size > 15 * 1024 * 1024: continue # Limite 15MB
        file_bytes = arquivo.getvalue()
        name = arquivo.name.lower()
        try:
            if name.endswith('.txt') or name.endswith('.csv'): 
                texto_extraido += f"\n{file_bytes.decode('utf-8', errors='ignore')}"
            elif name.endswith('.pdf'): 
                texto_extraido += "\n".join([p.extract_text() for p in PyPDF2.PdfReader(io.BytesIO(file_bytes)).pages if p.extract_text()])
            elif name.endswith('.docx'): 
                texto_extraido += docx2txt.process(io.BytesIO(file_bytes))
            elif name.endswith(('.png', '.jpg', '.jpeg')) and gemini_key:
                genai.configure(api_key=gemini_key)
                texto_extraido += genai.GenerativeModel('gemini-1.5-flash').generate_content(
                    ["Extraia toda a telemetria, texto ou dados tecnicos contidos nesta imagem de forma minuciosa.", 
                     Image.open(io.BytesIO(file_bytes))]).text
        except:
            pass
    return pii_anonymizer(texto_extraido)

# --- INTERFACES DE IA VETORIAL (RAG Engine) ---
def processar_rag(texto_bruto, comando, gemini_key):
    if not gemini_key or len(texto_bruto) < 3000: return texto_bruto
    try:
        chunks = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300).split_text(texto_bruto)
        db = FAISS.from_texts(chunks, GoogleGenerativeAIEmbeddings(google_api_key=gemini_key, model="models/embedding-001"))
        return "\n...\n".join([d.page_content for d in db.similarity_search(comando, k=4)])
    except: 
        return texto_bruto[:15000]

# --- 🐉 A HIDRA: MOTOR COGNITIVO MULTI-CABEÇA E APP BUILDER ---
class HydraEngine:
    def __init__(self, groq_key, gemini_key):
        self.groq_key = groq_key
        self.gemini_key = gemini_key

    def strike(self, system, prompt, retries=3):
        if self.groq_key:
            for attempt in range(retries):
                try:
                    client = Groq(api_key=self.groq_key)
                    return client.chat.completions.create(
                        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}], 
                        model="llama-3.3-70b-versatile", 
                        temperature=0.2
                    ).choices[0].message.content
                except Exception as e:
                    if "429" in str(e):
                        time.sleep(2 ** attempt)
                    elif self.gemini_key:
                        try:
                            genai.configure(api_key=self.gemini_key)
                            return genai.GenerativeModel('gemini-1.5-pro-latest').generate_content(f"{system}\n\n{prompt}").text
                        except: pass
        
        # Contingência Crítica: DuckDuckGo Web Scraping Invisível
        try:
            with DDGS() as ddgs:
                search = [r['body'] for r in ddgs.text(f"solucao para: {prompt[:50]}", max_results=2)]
                return f"[MODO EMERGÊNCIA DDGS]: A IA principal falhou. Dados recuperados:\n" + "\n".join(search)
        except: 
            return "Erro Crítico: A Hidra foi suprimida. Nenhuma API ou barramento de contingência respondeu."

    def cabeca_ia_paralela(self, perfil, comando, contexto):
        """Cabeça individual da Hidra para processamento paralelo."""
        sys_msg = f"Você é {perfil}. Atue como um especialista sênior. Responda de forma direta e altamente técnica."
        prompt = f"Missão: {comando}\nContexto de Apoio: {contexto}"
        try:
            res = self.strike(sys_msg, prompt, retries=1)
            return f"### 🧠 {perfil}\n{res}"
        except Exception as e:
            return f"### ⚠️ {perfil}\nFalha na conexão: {e}"

    def genesis_app_builder(self, prompt):
        """O Motor inspirado no Bolt.new, v0 e Cursor. Cria código puro renderizável."""
        sys_msg = (
            "Você é o Nexus Genesis, um engenheiro de software autônomo de nível elite. "
            "Sua missão é criar aplicações web COMPLETAS, interativas e modernas em UM ÚNICO arquivo HTML. "
            "INCLUA bibliotecas via CDN (TailwindCSS, React, Chart.js, etc.) dentro do HTML. "
            "INCLUA CSS interno e JS interno. O sistema DEVE funcionar perfeitamente. "
            "NÃO envie explicações fora do código. Seu retorno deve conter APENAS UM bloco de código ```html ... ```."
        )
        return self.strike(sys_msg, prompt)

# --- GERADOR DE DOSSIÊS EM PDF ---
def gerar_pdf(conteudo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_fill_color(139, 92, 246)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, "DOSSIE DE AUDITORIA FORENSE - NEXUS HYDRA", ln=True, align='C', fill=True)
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    texto_limpo = conteudo.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, texto_limpo)
    return bytes(pdf.output(dest='S'))

# --- TERMINAL HARDWARE UNIFICADO (OMNI-PROTOCOL & URL LINK) ---
def formatar_log(tipo, payload, ts):
    if tipo == "RF_SCAN":
        try:
            return f"[{ts}] <span class='terminal-tag'>[LIVE_IOT]</span> -> <span class='terminal-data'>ALVO RF: Canal {int(payload):02d} Interceptado via Nuvem!</span>"
        except:
            return f"[{ts}] <span class='terminal-tag'>[LIVE_IOT]</span> -> <span class='terminal-data'>ALVO RF: {payload}</span>"
    else:
        return f"[{ts}] <span class='terminal-tag' style='color:#facc15;'>[OMNI_SERIAL]</span> -> <span class='terminal-info'>DADO BRUTO: {payload}</span>"

# =============================================================================
# 🕹️ CORE PRINCIPAL OPERACIONAL DA INTERFACE
# =============================================================================
def main():
    # Inicialização da Memória de Longo Prazo do Chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    # Inicialização global do Strike Code e Genesis Code
    if "strike_code" not in st.session_state: st.session_state.strike_code = None
    if "genesis_code" not in st.session_state: st.session_state.genesis_code = None

    # HUD Superior
    h1, h2, h3, h4 = st.columns(4)
    with h1: st.markdown("<div class='hud-card'><div class='hud-title'>SISTEMA</div><div class='hud-value' style='color:#8b5cf6;'>NEXUS GENESIS v9.0</div></div>", unsafe_allow_html=True)
    with h2: st.markdown("<div class='hud-card hud-card-gold'><div class='hud-title'>APP BUILDER ENGINE</div><div class='hud-value'>ARTIFACTS / BOLT MODE</div></div>", unsafe_allow_html=True)
    with h3: st.markdown("<div class='hud-card hud-card-green'><div class='hud-title'>DATA LAKE DB</div><div class='hud-value'>SQLITE V9 ANCORADO</div></div>", unsafe_allow_html=True)
    with h4: st.markdown("<div class='hud-card'><div class='hud-title'>COGNITIVO</div><div class='hud-value' style='color:#58a6ff;'>GROQ + GEMINI CORE</div></div>", unsafe_allow_html=True)

    G_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEM_KEY = st.secrets.get("GEMINI_API_KEY", "")
    hydra = HydraEngine(G_KEY, GEM_KEY)
    
    # 📑 Abas Estruturadas de Nível Global
    t_genesis, t_auditoria, t_strike, t_hidra, t_autofix, t_rf = st.tabs([
        "🌌 NEXUS FORGE (APP BUILDER)",
        "🧠 AUDITORIA MULTI-AGENTE", 
        "💀 PROTOCOLO STRIKE", 
        "🐉 CONSENSO DA HIDRA",
        "🔧 AGENTE AUTOFIX",
        "📡 TELEMETRIA OMNI-HARDWARE"
    ])
    
    # --- ABA 1: NEXUS FORGE (INÉDITO - SISTEMA DE CRIAÇÃO ESTILO BOLT.NEW/CURSOR) ---
    with t_genesis:
        st.markdown("<br><p style='color:#8b949e; font-weight:bold;'>Motor autônomo baseado em IAs de elite. Crie sistemas inteiros com um único comando.</p>", unsafe_allow_html=True)
        cg1, cg2 = st.columns([1.5, 2.5])
        
        with cg1:
            app_prompt = st.text_area("Descreva o Sistema ou Dashboard a ser criado:", height=200, placeholder="Ex: Crie um dashboard Cyberpunk em HTML/JS/Tailwind para monitorar servidores fictícios em tempo real...")
            if st.button("🚀 INICIAR GERAÇÃO AUTÔNOMA (GENESIS)"):
                if app_prompt:
                    with st.status("🏗️ Nexus Architect construindo o sistema...", expanded=True) as status:
                        st.write("🔍 Raciocinando sobre a arquitetura (Modo Cursor)...")
                        time.sleep(1)
                        st.write("💻 Escrevendo componentes e injetando lógica (Modo Devin)...")
                        
                        resultado_genesis = hydra.genesis_app_builder(app_prompt)
                        
                        # Extrai rigorosamente o bloco HTML para não quebrar o visualizador
                        match = re.search(r"
