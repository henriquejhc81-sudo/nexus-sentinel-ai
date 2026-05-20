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
from duckduckgo_search import DDGS

# =============================================================================
# 🛡️ ARSENAL DE DEPENDÊNCIAS (VERIFICAÇÃO DE INTEGRIDADE)
# =============================================================================
try:
    from groq import Groq
    import google.generativeai as genai
    import PyPDF2
    import docx2txt
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from fpdf import FPDF
except ImportError as e:
    st.error(f"Erro Crítico. Dependência ausente no ecossistema: {e}")

# Configuração Base do HUD Soberano
st.set_page_config(page_title="Nexus v8.3 Omni Evolution", page_icon="🐉", layout="wide")

# =============================================================================
# 🗄️ BANCO DE DADOS DA HIDRA (TRANSAÇÕES SEGURAS MULTI-THREAD)
# =============================================================================
DB_NAME = 'nexus_datalake_v8.db'

def init_db():
    with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS radar_logs 
                     (id_sinal TEXT PRIMARY KEY, tipo TEXT, payload TEXT, timestamp TEXT)''')
        conn.commit()

def salvar_no_db(id_sinal, tipo, payload, timestamp):
    with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO radar_logs (id_sinal, tipo, payload, timestamp) VALUES (?, ?, ?, ?)", 
                  (id_sinal, tipo, str(payload), timestamp))
        conn.commit()

def carregar_do_db():
    with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute("SELECT id_sinal, tipo, payload, timestamp FROM radar_logs ORDER BY timestamp DESC LIMIT 50")
        linhas = c.fetchall()
    return linhas

# Inicialização Autônoma do Data Lake
init_db()

# =============================================================================
# 🖥️ ARQUITETURA DE DESIGN ULTRA-CYBERPUNK (HUD CSS INJETADO)
# =============================================================================
st.markdown("""
    <style>
    .stApp { 
        background-color: #02040a !important;
        background-image: radial-gradient(circle at 50% 10%, #0a1128 0%, #02040a 100%) !important; 
        color: #f0f4f8 !important; 
        font-family: 'JetBrains Mono', 'Consolas', monospace !important;
    }
    .block-container { 
        padding-top: 2rem !important; 
        padding-bottom: 1rem !important;
        max-width: 95% !important;
    }
    .stTabs [data-baseweb="tab-list"] { 
        gap: 8px; 
        background-color: #090d16; 
        padding: 6px; 
        border-radius: 6px;
        border: 1px solid #161b22; 
    }
    .stTabs [data-baseweb="tab"] { 
        height: 36px; 
        color: #8b949e !important; 
        font-weight: 700; 
        font-size: 11px;
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(135deg, #A51C30 0%, #8b5cf6 100%) !important; 
        color: #ffffff !important;
        box-shadow: 0 0 12px rgba(139, 92, 246, 0.4); 
    }
    .hud-card { 
        background: rgba(13, 17, 23, 0.75);
        border: 1px solid #21262d; 
        border-left: 4px solid #8b5cf6; 
        padding: 12px 14px; 
        border-radius: 6px; 
        backdrop-filter: blur(12px); 
        margin-bottom: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2); 
    }
    .hud-card-green { 
        border-left: 4px solid #10b981 !important;
    }
    .hud-title { 
        font-size: 9px; 
        color: #8b949e; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
        font-weight: bold;
    }
    .hud-value { 
        font-size: 14px; 
        color: #f0f4f8; 
        font-weight: bold; 
        margin-top: 4px;
    }
    .terminal-box { 
        background-color: #03060c !important; 
        border: 1px solid #1f6feb !important; 
        border-radius: 6px; 
        padding: 12px;
        font-family: 'Consolas', monospace; 
        color: #58a6ff; 
        height: 280px; 
        overflow-y: auto; 
        box-shadow: inset 0 0 15px rgba(0,0,0,0.9);
    }
    .terminal-line { 
        margin-bottom: 5px; 
        font-size: 11.5px; 
        border-bottom: 1px solid rgba(31,111,235,0.05); 
        padding-bottom: 2px;
    }
    .terminal-tag { color: #f43f5e; font-weight: bold; }
    .terminal-data { color: #56d364; }
    .terminal-info { color: #8b949e; }
    
    .stButton>button { 
        background: linear-gradient(135deg, #A51C30 0%, #8b5cf6 100%) !important;
        color: #ffffff !important; 
        font-weight: 800 !important; 
        border-radius: 6px !important; 
        padding: 10px 12px !important; 
        font-size: 12px !important; 
        border: none !important;
        width: 100%; 
        margin-top: 5px; 
    }
    .stButton>button:hover { 
        transform: translateY(-1px); 
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    }
    .stTextArea textarea { 
        background-color: #0d1117 !important; 
        color: #58a6ff !important; 
        border: 1px solid #21262d !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 🛡️ DNA SENTINEL: ANONIMIZAÇÃO E EXTRATOR DE CONTEXTO OMNI
# =============================================================================
def pii_anonymizer(texto):
    if not texto: return texto
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF PROTEGIDO]', texto)
    texto = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ PROTEGIDO]', texto)
    return texto.replace("```", "'''")

def omni_extractor(arquivos_upados, gemini_key):
    texto_extraido = ""
    if not arquivos_upados: return texto_extraido
    for arq in arquivos_upados:
        if arq.size > 15 * 1024 * 1024: continue  # Proteção de estouro de buffer (15MB Limite)
        fb = arq.getvalue()
        name = arq.name.lower()
        try:
            if name.endswith('.txt') or name.endswith('.csv'): 
                texto_extraido += f"\n{fb.decode('utf-8', errors='ignore')}"
            elif name.endswith('.pdf'): 
                texto_extraido += "\n".join([p.extract_text() for p in PyPDF2.PdfReader(io.BytesIO(fb)).pages if p.extract_text()])
            elif name.endswith('.docx'): 
                texto_extraido += docx2txt.process(io.BytesIO(fb))
            elif name.endswith(('.png', '.jpg', '.jpeg')) and gemini_key:
                genai.configure(api_key=gemini_key)
                texto_extraido += genai.GenerativeModel('gemini-1.5-flash').generate_content(
                    ["Descreva técnica e textualmente a imagem para auditoria forense.", Image.open(io.BytesIO(fb))]
                ).text
        except Exception as e:
            pass
    return pii_anonymizer(texto_extraido)

def processar_rag(texto_bruto, comando, gemini_key):
    if not gemini_key or len(texto_bruto) < 3000: 
        return texto_bruto
    try:
        chunks = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300).split_text(texto_bruto)
        db = FAISS.from_texts(chunks, GoogleGenerativeAIEmbeddings(google_api_key=gemini_key, model="models/embedding-001"))
        return "\n...\n".join([d.page_content for d in db.similarity_search(comando, k=4)])
    except Exception: 
        return texto_bruto[:15000]

# =============================================================================
# 🐉 A HIDRA: MOTOR COGNITIVO MULTI-CABEÇA (AUTO-REGENERAÇÃO ABSOLUTA)
# =============================================================================
class HydraEngine:
    def __init__(self, groq_key, gemini_key):
        self.groq_key = groq_key
        self.gemini_key = gemini_key

    def strike(self, system, prompt):
        # Cabeça 1: Groq Llama 3.3 70B
        if self.groq_key:
            try:
                client = Groq(api_key=self.groq_key)
                return client.chat.completions.create(
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}], 
                    model="llama-3.3-70b-versatile", 
                    temperature=0.2
                ).choices[0].message.content
            except Exception:
                pass
        
        # Cabeça 2: Fallback Gemini Pro 1.5
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                return genai.GenerativeModel('gemini-1.5-pro-latest').generate_content(f"{system}\n\n{prompt}").text
            except Exception:
                pass
        
        # Cabeça 3: Contingência Total via Web Scraping / DDGS
        try:
            with DDGS() as ddgs:
                search = [r['body'] for r in ddgs.text(f"solução para: {prompt[:50]}", max_results=2)]
                return f"[MODO EMERGÊNCIA DDGS]: Sistemas cognitivos principais inacessíveis.\nDados recuperados de inteligência:\n" + "\n".join(search)
        except Exception: 
            return "Erro Crítico: A Hidra foi suprimida. Nenhuma API ou barramento de contingência respondeu."

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
    
    # Sanitização profunda de codificação para evitar falhas de compilação de fontes no PDF
    texto_limpo = conteudo.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, texto_limpo)
    return bytes(pdf.output(dest='S'))

# =============================================================================
# 📡 TERMINAL HARDWARE (OMNI-PROTOCOL & LIVE IOT MONITOR)
# =============================================================================
def formatar_log(tipo, payload, ts):
    if tipo == "RF_SCAN":
        try:
            return f"[{ts}] <span class='terminal-tag'>[LIVE_IOT]</span> -> <span class='terminal-data'>ALVO RF: Canal {int(payload):02d} Interceptado via Nuvem!</span>"
        except Exception:
            return f"[{ts}] <span class='terminal-tag'>[LIVE_IOT]</span> -> <span class='terminal-data'>ALVO RF: {payload}</span>"
    else:
        return f"[{ts}] <span class='terminal-tag' style='color:#facc15;'>[OMNI_SERIAL]</span> -> <span class='terminal-info'>DADO BRUTO: {payload}</span>"

def renderizar_painel_rf():
    st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)
    
    if "ids_processados" not in st.session_state:
        st.session_state.ids_processados = set()
    if "logs_rf" not in st.session_state:
        st.session_state.logs_rf = []
        historico = carregar_do_db()
        if not historico:
            st.session_state.logs_rf.append(f"[{datetime.now().strftime('%H:%M:%S')}] <span class='terminal-info'>[HYDRA] UPLINK OMNI ONLINE: Escutando portas seriais e RF...</span>")
        else:
            for rec in reversed(historico):
                st.session_state.ids_processados.add(rec[0])
                st.session_state.logs_rf.append(formatar_log(rec[1], rec[2], rec[3]))

    c1, c2 = st.columns([2.6, 1.4])
    with c2:
        modo_auto = st.toggle("🔌 LEITURA UNIVERSAL DE HARDWARE", value=True)
        hw = "HUB MULTI-PROTOCOLO (RF/USB/RS232)" if modo_auto else "NENHUM COMPONENTE DETECTADO"
        st_porta = "COM ATIVA (UPLINK SECURE)" if modo_auto else "OFFLINE"
    
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("🔄 Sincronizar Radar"):
                if modo_auto:
                    try:
                        res = requests.get("[https://ntfy.sh/nexus-hydra-polo-2026/json?poll=1&since=24h](https://ntfy.sh/nexus-hydra-polo-2026/json?poll=1&since=24h)", timeout=5)
                        if res.status_code == 200:
                            linhas = res.text.strip().split('\n')
                            for linha in linhas:
                                if not linha: continue
                                try:
                                    dados_ntfy = json.loads(linha)
                                    if dados_ntfy.get("event") == "message":
                                        id_sinal = dados_ntfy.get("id")
                                        
                                        if id_sinal not in st.session_state.ids_processados:
                                            st.session_state.ids_processados.add(id_sinal)
                                            ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                                            
                                            try:
                                                payload_json = json.loads(dados_ntfy.get("message"))
                                                if isinstance(payload_json, dict) and "tipo" in payload_json:
                                                    tipo = payload_json.get("tipo", "GENERIC_SERIAL")
                                                    dado_real = payload_json.get("payload", "")
                                                else:
                                                    tipo = "RF_SCAN"
                                                    dado_real = dados_ntfy.get("message")
                                            except Exception:
                                                tipo = "RF_SCAN"
                                                dado_real = dados_ntfy.get("message")
                                            
                                            salvar_no_db(id_sinal, tipo, str(dado_real), ts)
                                            st.session_state.logs_rf.append(formatar_log(tipo, dado_real, ts))
                                except Exception: pass
                    except Exception: pass
                st.rerun() 
                
        with c_btn2:
            if st.button("🧹 Limpar Console"): 
                st.session_state.logs_rf = [f"[{datetime.now().strftime('%H:%M:%S')}] <span class='terminal-info'>[HYDRA] Memória visual apagada (DB Seguro).</span>"]
                st.rerun()

        st.markdown(f"<div class='hud-card'><div class='hud-title'>ARQUITETURA FÍSICA</div><div class='hud-value' style='color:#58a6ff;'>{hw}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='hud-card'><div class='hud-title'>STATUS DA PONTE</div><div class='hud-value' style='color:#56d364;'>{st_porta}</div></div>", unsafe_allow_html=True)

    with c1:
        html = "<div class='terminal-box'>" + "".join([f"<div class='terminal-line'>{l}</div>" for l in reversed(st.session_state.logs_rf)]) + "</div>"
        st.markdown(html, unsafe_allow_html=True)

# =============================================================================
# 🕹️ OPERAÇÃO CORE CENTRAL
# =============================================================================
def main():
    # Painel Dinâmico de Métricas HUD
    h1
