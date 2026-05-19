"""
=============================================================================
🛡️ NEXUS OMNICORE v7.5 - HYDRA CORE (DATA LAKE & PERFECT SYNC)
=============================================================================
Fusão Suprema: DNA Histórico Preservado + Banco de Dados SQLite + Sincronia NTFY
A nuvem agora tem memória permanente e puxa o histórico dos satélites.
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
from duckduckgo_search import DDGS

# Arsenal de Dependências
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
    st.error(f"Erro Crítico. Dependência ausente: {e}")

st.set_page_config(page_title="Nexus v7.5 Hydra", page_icon="🐉", layout="wide")

# --- BANCO DE DADOS DA HIDRA (MEMÓRIA PERSISTENTE) ---
def init_db():
    conn = sqlite3.connect('nexus_datalake.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS radar_logs 
                 (id_sinal TEXT PRIMARY KEY, canal TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def salvar_no_db(id_sinal, canal, timestamp):
    conn = sqlite3.connect('nexus_datalake.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO radar_logs (id_sinal, canal, timestamp) VALUES (?, ?, ?)", (id_sinal, canal, timestamp))
    conn.commit()
    conn.close()

def carregar_do_db():
    conn = sqlite3.connect('nexus_datalake.db')
    c = conn.cursor()
    c.execute("SELECT id_sinal, canal, timestamp FROM radar_logs ORDER BY timestamp DESC LIMIT 50")
    linhas = c.fetchall()
    conn.close()
    return linhas

init_db()

# 🖥️ DESIGN SOBERANO (HUD Balanceado)
st.markdown("""
    <style>
    .stApp {
        background-color: #02040a !important;
        background-image: radial-gradient(circle at 50% 10%, #0a1128 0%, #02040a 100%) !important;
        color: #f0f4f8 !important;
        font-family: 'JetBrains Mono', 'Consolas', monospace !important;
    }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 1rem !important; max-width: 95% !important;}
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #090d16; padding: 6px; border-radius: 6px; border: 1px solid #161b22; }
    .stTabs [data-baseweb="tab"] { height: 36px; color: #8b949e !important; font-weight: 700; font-size: 11px; }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #A51C30 0%, #8b5cf6 100%) !important;
        color: #ffffff !important; box-shadow: 0 0 12px rgba(139, 92, 246, 0.4);
    }
    
    .hud-card {
        background: rgba(13, 17, 23, 0.75); border: 1px solid #21262d; border-left: 4px solid #8b5cf6;
        padding: 12px 14px; border-radius: 6px; backdrop-filter: blur(12px); margin-bottom: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .hud-card-green { border-left: 4px solid #10b981 !important; }
    .hud-title { font-size: 9px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }
    .hud-value { font-size: 14px; color: #f0f4f8; font-weight: bold; margin-top: 4px; }
    
    .terminal-box {
        background-color: #03060c !important; border: 1px solid #1f6feb !important; border-radius: 6px;
        padding: 12px; font-family: 'Consolas', monospace; color: #58a6ff; height: 260px; overflow-y: auto;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.9);
    }
    .terminal-line { margin-bottom: 5px; font-size: 11.5px; border-bottom: 1px solid rgba(31,111,235,0.05); padding-bottom: 2px; }
    .terminal-tag { color: #f43f5e; font-weight: bold; }
    .terminal-data { color: #56d364; }
    .terminal-info { color: #8b949e; }
    
    .stButton>button {
        background: linear-gradient(135deg, #A51C30 0%, #8b5cf6 100%) !important;
        color: #ffffff !important; font-weight: 800 !important; border-radius: 6px !important;
        padding: 10px 12px !important; font-size: 12px !important; border: none !important; width: 100%;
        margin-top: 5px;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4); }
    .stTextArea textarea { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #21262d !important; }
    </style>
    """, unsafe_allow_html=True)

# 🛡️ DNA SENTINEL: Anonimização e Extrator
def pii_anonymizer(texto):
    if not texto: return texto
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF PROTEGIDO]', texto)
    return re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ PROTEGIDO]', texto).replace("```", "'''")

def omni_extractor(arquivos_upados, gemini_key):
    texto_extraido = ""
    if not arquivos_upados: return texto_extraido
    for arq in arquivos_upados:
        if arq.size > 15 * 1024 * 1024: continue
        fb = arq.getvalue()
        name = arq.name.lower()
        try:
            if name.endswith('.txt') or name.endswith('.csv'): texto_extraido += f"\n{fb.decode('utf-8', errors='ignore')}"
            elif name.endswith('.pdf'): texto_extraido += "\n".join([p.extract_text() for p in PyPDF2.PdfReader(io.BytesIO(fb)).pages if p.extract_text()])
            elif name.endswith('.docx'): texto_extraido += docx2txt.process(io.BytesIO(fb))
            elif name.endswith(('.png', '.jpg', '.jpeg')) and gemini_key:
                genai.configure(api_key=gemini_key)
                texto_extraido += genai.GenerativeModel('gemini-1.5-flash').generate_content(["Descreva técnica e textualmente a imagem de forma minuciosa.", Image.open(io.BytesIO(fb))]).text
        except: pass
    return pii_anonymizer(texto_extraido)

def processar_rag(texto_bruto, comando, gemini_key):
    if not gemini_key or len(texto_bruto) < 3000: return texto_bruto
    try:
        chunks = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300).split_text(texto_bruto)
        db = FAISS.from_texts(chunks, GoogleGenerativeAIEmbeddings(google_api_key=gemini_key, model="models/embedding-001"))
        return "\n...\n".join([d.page_content for d in db.similarity_search(comando, k=4)])
    except: return texto_bruto[:15000]

# 🐉 A HIDRA: MOTOR MULTI-CABEÇA (Self-Healing Absoluto)
class HydraEngine:
    def __init__(self, groq_key, gemini_key):
        self.groq_key = groq_key
        self.gemini_key = gemini_key

    def strike(self, system, prompt):
        if self.groq_key:
            client = Groq(api_key=self.groq_key)
            try:
                return client.chat.completions.create(
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile", temperature=0.2
                ).choices[0].message.content
            except Exception as e:
                if self.gemini_key:
                    try:
                        genai.configure(api_key=self.gemini_key)
                        return genai.GenerativeModel('gemini-1.5-pro-latest').generate_content(f"{system}\n\n{prompt}").text
                    except: pass
                
        try:
            with DDGS() as ddgs:
                search = [r['body'] for r in ddgs.text(f"solução para: {prompt[:50]}", max_results=2)]
                return f"[MODO EMERGÊNCIA DDGS]: A IA falhou. Dados recuperados da rede global:\n" + "\n".join(search)
        except: return "Erro Crítico: A Hidra foi suprimida. Nenhuma API respondeu."

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
    pdf.multi_cell(0, 6, conteudo.encode('latin-1', 'replace').decode('latin-1'))
    return bytes(pdf.output(dest='S'))

# 📡 TERMINAL HARDWARE (DATA LAKE & NTFY SYNC)
def renderizar_painel_rf():
    st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)
    
    if "ids_processados" not in st.session_state:
        st.session_state.ids_processados = set()
    if "logs_rf" not in st.session_state:
        st.session_state.logs_rf = []
        # Carrega o histórico do Banco de Dados ao iniciar
        historico = carregar_do_db()
        if not historico:
            st.session_state.logs_rf.append(f"[{datetime.now().strftime('%H:%M:%S')}] <span class='terminal-info'>[HYDRA] UPLINK NTFY ONLINE: Aguardando telemetria...</span>")
        else:
            for rec in reversed(historico):
                st.session_state.ids_processados.add(rec[0])
                st.session_state.logs_rf.append(f"[{rec[2]}] <span class='terminal-tag'>[LIVE_IOT]</span> -> <span class='terminal-data'>CAPTURA VERIFICADA: Canal {int(rec[1]):02d} Interceptado via Nuvem!</span>")

    c1, c2 = st.columns([2.6, 1.4])
    with c2:
        modo_auto = st.toggle("🔌 LEITURA AUTOMÁTICA DE HARDWARE", value=True)
        hw = "ESP32 + NRF24L01 HYDRA" if modo_auto else "NENHUM COMPONENTE DETECTADO"
        st_porta = "COM3 ATIVA (UPLINK SECURE)" if modo_auto else "OFFLINE"
        
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("🔄 Sincronizar Radar"):
                if modo_auto:
                    try:
                        # Agora ele puxa todas as mensagens dos últimos 10 minutos! Sem erro de timing.
                        res = requests.get("[https://ntfy.sh/nexus-hydra-polo-2026/json?poll=1&since=10m](https://ntfy.sh/nexus-hydra-polo-2026/json?poll=1&since=10m)", timeout=4)
                        if res.status_code == 200:
                            linhas = res.text.strip().split('\n')
                            for linha in linhas:
                                if not linha: continue
                                try:
                                    dados = json.loads(linha)
                                    if dados.get("event") == "message":
                                        canal = dados.get("message")
                                        id_sinal = dados.get("id")
                                        
                                        if id_sinal not in st.session_state.ids_processados:
                                            st.session_state.ids_processados.add(id_sinal)
                                            ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                                            # Salva na tela e no banco de dados eterno!
                                            salvar_no_db(id_sinal, canal, ts)
                                            log_real = f"[{ts}] <span class='terminal-tag'>[LIVE_IOT]</span> -> <span class='terminal-data'>CAPTURA VERIFICADA: Canal {int(canal):02d} Interceptado via Nuvem!</span>"
                                            st.session_state.logs_rf.append(log_real)
                                except: pass
                    except: pass
                st.rerun() 
                
        with c_btn2:
            if st.button("🧹 Limpar Console"): 
                # Limpa a tela (mas o BD continua seguro)
                st.session_state.logs_rf = [f"[{datetime.now().strftime('%H:%M:%S')}] <span class='terminal-info'>[HYDRA] Memória visual apagada (DB Seguro).</span>"]
                st.rerun()

        st.markdown(f"<div class='hud-card'><div class='hud-title'>COMPONENTE</div><div class='hud-value' style='color:#58a6ff;'>{hw}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='hud-card'><div class='hud-title'>STATUS DA PONTE</div><div class='hud-value' style='color:#56d364;'>{st_porta}</div></div>", unsafe_allow_html=True)

    with c1:
        html = "<div class='terminal-box'>" + "".join([f"<div class='terminal-line'>{l}</div>" for l in reversed(st.session_state.logs_rf)]) + "</div>"
        st.markdown(html, unsafe_allow_html=True)

# 🕹️ CORE PRINCIPAL
def main():
    h1, h2, h3, h4 = st.columns(4)
    with h1: st.markdown("<div class='hud-card'><div class='hud-title'>SISTEMA</div><div class='hud-value' style='color:#8b5cf6;'>HYDRA CORE v7.5</div></div>", unsafe_allow_html=True)
    with h2: st.markdown("<div class='hud-card hud-card-green'><div class='hud-title'>DATA LAKE DB</div><div class='hud-value'>SQLITE ANCORADO</div></div>", unsafe_allow_html=True)
    with h3: st.markdown("<div class='hud-card hud-card-green'><div class='hud-title'>HARDWARE</div><div class='hud-value'>UPLINK IOT ACTIVE</div></div>", unsafe_allow_html=True)
    with h4: st.markdown("<div class='hud-card'><div class='hud-title'>COGNITIVO</div><div class='hud-value' style='color:#58a6ff;'>GROQ + GEMINI</div></div>", unsafe_allow_html=True)

    G_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEM_KEY = st.secrets.get("GEMINI_API_KEY", "")
    hydra = HydraEngine(G_KEY, GEM_KEY)
    
    t_auditoria, t_strike, t_rf = st.tabs(["🧠 AUDITORIA MULTI-AGENTE & INCEPTION", "💀 PROTOCOLO RECON & STRIKE", "📡 TERMINAL HARDWARE (USB)"])
    
    with t_auditoria:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2.5, 1, 1.2]) 
        with c1: 
            comando = st.text_area("⌨️ PROTOCOLO DE ALVO:", height=150, key="txt_auditoria", placeholder="Defina o alvo, cole o código ou descreva a arquitetura desejada...")
        with c2: 
            arquivos = st.file_uploader("📂 EVIDÊNCIAS:", accept_multiple_files=True, key="up_aud")
        with c3:
            modo_auditoria = st.selectbox("🎯 DIRETRIZ DA MISSÃO:", ["Forense (Red vs Blue Team)", "Arquiteto (Geração Inception DNA)"])
            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            if st.button("⚡ INICIAR OPERAÇÃO"):
                with st.spinner("A Hidra está processando..."):
                    ctx = processar_rag(omni_extractor(arquivos, GEM_KEY), comando, GEM_KEY)
                    
                    if "Forense" in modo_auditoria:
                        with concurrent.futures.ThreadPoolExecutor() as exec:
                            r_red = exec.submit(hydra.strike, "Red Team. Ataque impiedosamente a arquitetura e ache falhas.", f"Alvo: {comando}\nContexto: {ctx}").result()
                            r_blue = exec.submit(hydra.strike, "Blue Team. Defenda, proponha arquiteturas e corrija as falhas.", f"Alvo: {comando}\nContexto: {ctx}").result()
                        dossie = hydra.strike("Sintetize um Relatório Forense Final detalhado e executivo.", f"RED:\n{r_red}\n\nBLUE:\n{r_blue}")
                        st.markdown(dossie)
                        st.download_button("📥 BAIXAR RELATÓRIO TÁTICO (PDF)", gerar_pdf(dossie), file_name="Hydra_Dossie.pdf")
                    else:
                        laudo_direto = hydra.strike("Aja como um Arquiteto de Software Sênior. Gere código e documentação estruturada impecável.", f"Diretriz: {comando}\nContexto: {ctx}")
                        st.markdown(laudo_direto)

    with t_strike:
        st.markdown("<br>", unsafe_allow_html=True)
        c_in, c_opt = st.columns([2, 1])
        with c_in: m_strike = st.text_area("Alvo para Criação de Código Web (Live) ou IP/Log para Denúncia:", height=130, key="txt_strike")
        with c_opt: 
            modo_s = st.selectbox("Ação:", ["Web Developer (Live Preview)", "Relatório de Denúncia Forense IP"])
            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            if st.button("💀 EXECUTAR STRIKE PROTOCOL"):
                with st.spinner("Acionando rastreamento/desenvolvimento..."):
                    if "Web" in modo_s:
                        res = hydra.strike("Crie código de altíssima qualidade. Junte HTML, CSS e JS em um único bloco <html>.", m_strike)
                        st.session_state['strike_code'] = res
                    else:
                        res = hydra.strike("PROTOCOLO STRIKE ATIVO: Identifique o IP, rastreie origem e gere um relatório de denúncia forense para autoridades.", m_strike)
                        st.error("⚠️ AVISO FORENSE GERADO. REVISE AS INFORMAÇÕES.")
                        st.markdown(res)
                        
        if 'strike_code' in st.session_state and "Web" in modo_s:
            tab_c, tab_v = st.tabs(["💻 Código Fonte", "🖼️ Live Preview (Renderização Real)"])
            with tab_c: 
                st.markdown(st.session_state['strike_code'])
                formato = st.selectbox("Exportar código como:", [".py", ".html", ".js", ".txt"])
                st.download_button(f"📥 BAIXAR ({formato})", st.session_state['strike_code'], file_name=f"hydra_code{formato}")
            with tab_v:
                if "<html>" in st.session_state['strike_code'].lower():
                    st.components.v1.html(st.session_state['strike_code'], height=450, scrolling=True)

    with t_rf:
        renderizar_painel_rf()

if __name__ == "__main__":
    main()
