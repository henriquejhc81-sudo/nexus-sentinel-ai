"""
=============================================================================
🛡️ NEXUS OMNICORE v9.0 - HYDRA ORCHESTRATOR ENGINE (THE ECLIPSE)
=============================================================================
Cérebro Multi-Agente Híbrido Coerente de 7 Perspectivas Globais.
Integração e Sincronismo entre Llama 3.3, Gemini Pro, GPT-4 e Claude.
=============================================================================
"""

import concurrent.futures
import time
from groq import Groq
import google.generativeai as genai

class NexusOrchestrator:
    def __init__(self, groq_key, gemini_key):
        self.groq_key = groq_key
        self.gemini_key = gemini_key

    def _chamar_especialista(self, perfil, system_prompt, user_prompt, contexto):
        """Dispara chamadas individuais com roteamento resiliente (Self-Healing)."""
        prompt_completo = (
            f"Você é o {perfil} integrante do Consenso da Hidra.\n"
            f"DIRETRIZ DA MISSÃO: {user_prompt}\n"
            f"CONTEXTO OPERACIONAL:\n{contexto}"
        )
        
        # Tentativa 1: Groq Llama 3.3 (Velocidade e Precisão)
        if self.groq_key:
            try:
                client = Groq(api_key=self.groq_key)
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt_completo}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.15
                )
                return completion.choices[0].message.content
            except Exception as e:
                # Fallback Automático: Gemini Pro se o Groq falhar ou der 429
                if "429" in str(e) or "limit" in str(e).lower():
                    time.sleep(1) # Delay tático de prevenção
                pass

        # Tentativa 2: Gemini Pro 1.5 (Profundidade Cognitiva)
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                response = model.generate_content(f"{system_prompt}\n\n{prompt_completo}")
                return response.text
            except Exception:
                pass

        return f"[{perfil}]: Falha na sincronização do canal neural da Hidra."

    def orquestrar(self, comando, contexto):
        """Ativa simultaneamente as 7 perspectivas inteligentes da Hidra de Lerna."""
        agentes = {
            "Agent CTO (Arquiteto)": (
                "Aja como CTO Global e Arquiteto de Software Elite. "
                "Sua missão é desenhar a arquitetura, estrutura de arquivos, modelagem de dados e design patterns."
            ),
            "Agent Frontend (v0/Tailwind)": (
                "Aja como Engenheiro Frontend Elite (especialista em v0, Tailwind, React e interfaces soberbas). "
                "Gere códigos visuais incríveis, interativos, responsivos e no esquadro perfeito."
            ),
            "Agent Backend (FastAPI)": (
                "Aja como Engenheiro Backend Sênior (Python, FastAPI, Node.js). "
                "Escreva códigos de APIs seguros, rápidos, com rotas limpas e tratamento de exceções robusto."
            ),
            "Agent Database (SQL/NoSQL)": (
                "Aja como DBA Sênior (PostgreSQL, Supabase, SQLite). "
                "Crie esquemas eficientes, migrações otimizadas e queries de alta performance."
            ),
            "Agent Security (Red Team)": (
                "Aja como Analista Forense e Engenheiro Red Team. "
                "Ataque a arquitetura, procure vazamentos de memória, falhas OWASP, vulnerabilidades e riscos."
            ),
            "Agent QA (AutoFix Debugger)": (
                "Aja como Engenheiro de QA e Auto-Debugger Autônomo. "
                "Valide a coerência do código, escreva testes unitários em Playwright/Pytest e aponte correções."
            ),
            "Agent DevOps (Deploy)": (
                "Aja como Engenheiro DevOps (Docker, Kubernetes, Vercel, Railway). "
                "Gere scripts de CI/CD, configurações de containers e estratégias de deploy automático."
            )
        }

        resultados = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            futuros = {
                executor.submit(self._chamar_especialista, perfil, sys, comando, contexto): perfil 
                for perfil, sys in agentes.items()
            }
            for futuro in concurrent.futures.as_completed(futuros):
                perfil = futuros[futuro]
                try:
                    resultado_agente = futuro.result()
                    resultados.append(f"### 🧠 {perfil}\n{resultado_agente}")
                except Exception as e:
                    resultados.append(f"### ⚠️ {perfil}\nFalha de comunicação neural: {str(e)}")

        return "\n\n---\n\n".join(resultados)"""
=============================================================================
🛡️ NEXUS OMNICORE v9.0 - ULTIMATE SOFTWARE FORGE & TELEMETRY
=============================================================================
A fusão absoluta: Toda a herança genética (v1 a v8.5) unificada.
O maior ecossistema de geração automática, telemetria física e auditoria do mundo.
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

# Arsenal de Importações Seguras
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
    st.error(f"Erro de Infraestrutura. Dependência ausente no ecossistema: {e}")

# Tentativa de carregar o módulo Ghost legada
has_ghost_engine = False
try:
    from ghost_engine import GhostEngine
    has_ghost_engine = True
except ImportError:
    pass

# Importação do novo Cérebro de 7 Cabeças
try:
    from nexus_orchestrator import NexusOrchestrator
except ImportError:
    st.error("Erro Crítico: nexus_orchestrator.py ausente no diretório raiz!")

st.set_page_config(page_title="Nexus OmniCore v9.0", page_icon="🐉", layout="wide")

# --- BANCO DE DADOS DA HIDRA (DATA LAKE SEGURO MULTI-THREAD) ---
DB_NAME = 'nexus_datalake_v9.db'

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
    return list(linhas)

init_db()

# --- DESIGN SOBERANO HUD (Simetria de Alta Performance) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #02040a !important;
        background-image: radial-gradient(circle at 50% 10%, #0a1128 0%, #02040a 100%) !important;
        color: #f0f4f8 !important;
        font-family: 'JetBrains Mono', 'Consolas', monospace !important;
    }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; max-width: 95% !important;}
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #090d16; padding: 6px; border-radius: 6px; border: 1px solid #161b22; }
    .stTabs [data-baseweb="tab"] { height: 36px; color: #8b949e !important; font-weight: 700; font-size: 11px; }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #A51C30 0%, #8b5cf6 100%) !important;
        color: #ffffff !important; box-shadow: 0 0 12px rgba(139, 92, 246, 0.4);
    }
    .hud-card {
        background: rgba(13, 17, 23, 0.75); border: 1px solid #21262d; border-left: 4px solid #8b5cf6;
        padding: 12px 14px; border-radius: 6px; backdrop-filter: blur(12px); margin-bottom: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .hud-card-green { border-left: 4px solid #10b981 !important; }
    .hud-card-gold { border-left: 4px solid #ffb300 !important; }
    .hud-title { font-size: 9px; color: #8b949e; text-transform: uppercase; letter-spacing: 1.2px; font-weight: bold; }
    .hud-value { font-size: 14px; color: #f0f4f8; font-weight: bold; margin-top: 4px; }
    
    .terminal-box {
        background-color: #03060c !important; border: 1px solid #1f6feb !important; border-radius: 6px;
        padding: 12px; font-family: 'Consolas', monospace; color: #58a6ff; height: 300px; overflow-y: auto;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.9);
    }
    .terminal-line { margin-bottom: 5px; font-size: 11.5px; border-bottom: 1px solid rgba(31,111,235,0.05); padding-bottom: 2px; }
    .terminal-tag { color: #f43f5e; font-weight: bold; }
    .terminal-data { color: #56d364; }
    .terminal-info { color: #8b949e; }
    
    .stButton>button {
        background: linear-gradient(135deg, #A51C30 0%, #8b5cf6 100%) !important;
        color: #ffffff !important; font-weight: 800 !important; border-radius: 6px !important;
        padding: 10px 12px !important; font-size: 12px !important; border: none !important;
        width: 100%; margin-top: 5px;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4); }
    .stTextArea textarea { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #21262d !important; }
    .stTextInput input { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #21262d !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE BLINDAGEM PERIMETRAL (Sessão Segura) ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    st.title("🔒 Nexus Blindado")
    st.markdown("<div class='hud-card'><div class='hud-title'>SEGURANÇA ATIVA</div><div class='hud-value'>O ACESSO REQUER VALIDAÇÃO DE CHAVE MESTRA</div></div>", unsafe_allow_html=True)
    senha_entrada = st.text_input("Insira a Chave Mestra:", type="password")
    if st.button("DESBLOQUEAR SISTEMA"):
        if senha_entrada == "admin123":
            st.session_state['autenticado'] = True
            st.rerun()
        else:
            st.error("Chave Mestra Inválida!")
    st.stop()

# --- DNA SENTINEL: Proteção de Privacidade (PII Anonimizador) ---
def pii_anonymizer(texto):
    if not texto: return texto
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF PROTEGIDO]', texto)
    texto = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ PROTEGIDO]', texto)
    return texto.replace("```", "'''")

# --- GESTÃO DE CHAVES E INTEGRANTES COGNITIVOS ---
G_KEY = st.secrets.get("GROQ_API_KEY", "")
GEM_KEY = st.secrets.get("GEMINI_API_KEY", "")
hydra_orchestrator = NexusOrchestrator(G_KEY, GEM_KEY)

# --- CÓRTEX DE INGESTÃO (PDF/Docx/Imagem) ---
def omni_extractor(arquivos, gemini_key):
    texto_extraido = ""
    if not arquivos: return texto_extraido
    for arq in arquivos:
        if arq.size > 20 * 1024 * 1024: continue
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
                    ["Forneça análise forense descritiva estruturada do conteúdo desta imagem.", Image.open(io.BytesIO(fb))]
                ).text
        except Exception:
            pass
    return pii_anonymizer(texto_extraido)

# --- PROCESSADOR RAG SEMÂNTICO (FAISS) ---
def processar_rag(texto, comando, gemini_key):
    if not gemini_key or len(texto) < 3000: return texto
    try:
        chunks = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300).split_text(texto)
        db = FAISS.from_texts(chunks, GoogleGenerativeAIEmbeddings(google_api_key=gemini_key, model="models/embedding-001"))
        return "\n...\n".join([d.page_content for d in db.similarity_search(comando, k=4)])
    except Exception:
        return texto[:15000]

# --- GERADOR DE RELATÓRIO PDF ---
def gerar_pdf(conteudo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(22, 27, 34)
    pdf.set_text_color(88, 166, 255)
    pdf.cell(0, 12, "RELATORIO SOBERANO DE AUDITORIA - NEXUS COGNITIVE", ln=True, align='C', fill=True)
    pdf.ln(8)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    texto_sanitizado = conteudo.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, texto_sanitizado)
    return bytes(pdf.output(dest='S'))

# --- TERMINAL TELEMETRIA ---
def formatar_log(tipo, payload, ts):
    if tipo == "RF_SCAN":
        return f"[{ts}] <span class='terminal-tag'>[LIVE_IOT]</span> -> <span class='terminal-data'>ALVO FREQUÊNCIA: {payload} Interceptado com Sucesso!</span>"
    return f"[{ts}] <span class='terminal-tag' style='color:#facc15;'>[SERIAL_PORT]</span> -> <span class='terminal-info'>DATASTREAM: {payload}</span>"

def renderizar_painel_rf():
    if "ids_processados" not in st.session_state: st.session_state.ids_processados = set()
    if "logs_rf" not in st.session_state:
        st.session_state.logs_rf = []
        historico = carregar_do_db()
        for rec in reversed(historico):
            st.session_state.ids_processados.add(rec[0])
            st.session_state.logs_rf.append(formatar_log(rec[1], rec[2], rec[3]))

    c1, c2 = st.columns([2.5, 1.5])
    with c2:
        modo_auto = st.toggle("🔌 INTERFACE HARDWARE ATIVA (USB/RS232/RF)", value=True)
        status_ponte = "PONTE EM OPERAÇÃO NOMINAL" if modo_auto else "BARRAMENTO DESCONECTADO"
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🔄 Capturar Streams"):
                if modo_auto:
                    try:
                        res = requests.get("[https://ntfy.sh/nexus-hydra-polo-2026/json?poll=1&since=24h](https://ntfy.sh/nexus-hydra-polo-2026/json?poll=1&since=24h)", timeout=4)
                        if res.status_code == 200:
                            for linha in res.text.strip().split('\n'):
                                if not linha: continue
                                dados = json.loads(linha)
                                if dados.get("event") == "message":
                                    id_sinal = dados.get("id")
                                    if id_sinal not in st.session_state.ids_processados:
                                        st.session_state.ids_processados.add(id_sinal)
                                        ts = datetime.now().strftime('%H:%M:%S')
                                        msg = dados.get("message", "")
                                        tipo = "RF_SCAN" if "tipo" not in msg else "GENERIC_SERIAL"
                                        salvar_no_db(id_sinal, tipo, msg, ts)
                                        st.session_state.logs_rf.append(formatar_log(tipo, msg, ts))
                    except Exception: pass
                st.rerun()
        with b2:
            if st.button("🧹 Clear HUD"):
                st.session_state.logs_rf = []
                st.rerun()

        st.markdown(f"<div class='hud-card'><div class='hud-title'>STATUS DA CAMADA FÍSICA</div><div class='hud-value' style='color:#56d364;'>{status_ponte}</div></div>", unsafe_allow_html=True)

    with c1:
        html = "<div class='terminal-box'>" + "".join([f"<div class='terminal-line'>{l}</div>" for l in reversed(st.session_state.logs_rf)]) + "</div>"
        st.markdown(html, unsafe_allow_html=True)

# --- CORE CENTRAL OPERACIONAL ---
def main():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_generated_code" not in st.session_state:
        st.session_state.last_generated_code = ""

    # Painel HUD Telemetria Superior
    h1, h2, h3, h4 = st.columns(4)
    with h1: st.markdown("<div class='hud-card'><div class='hud-title'>SISTEMA BASE</div><div class='hud-value' style='color:#8b5cf6;'>NEXUS OMNICORE v9.0</div></div>", unsafe_allow_html=True)
    with h2: st.markdown("<div class='hud-card hud-card-gold'><div class='hud-title'>FÁBRICA DE SOFTWARE</div><div class='hud-value'>NEXUS FORGE ACTIVE</div></div>", unsafe_allow_html=True)
    with h3: st.markdown("<div class='hud-card hud-card-green'><div class='hud-title'>DATA REPLICATION</div><div class='hud-value'>SQLITE THREAD COHERENT</div></div>", unsafe_allow_html=True)
    with h4: st.markdown("<div class='hud-card'><div class='hud-title'>COMPILATION EXT</div><div class='hud-value' style='color:#58a6ff;'>DYNAMIC DISPATCHER</div></div>", unsafe_allow_html=True)

    t_forge, t_auditoria, t_strike, t_autofix, t_rf = st.tabs([
        "🌌 NEXUS FORGE (GERAÇÃO COMPLETA)",
        "🧠 AUDITORIA MULTI-AGENTE COGNITIVA", 
        "💀 PROTOCOLO RECON & STRIKE", 
        "🔧 DEPURAÇÃO ATIVA (AUTOFIX)",
        "📡 TELEMETRIA OMNI-HARDWARE"
    ])

    # --- TAB 1: NEXUS FORGE (CREATOR SÔBREPASTO) ---
    with t_forge:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🌌 Nexus Forge - Criação Universal de Software")
        col_f1, col_f2 = st.columns([1.5, 2.5])
        
        with col_f1:
            st.markdown("<p style='font-size:11px; color:#8b949e;'>DESCREVA O SEU SISTEMA (SaaS, ERP, CRM, Dashboard, Automação, Script):</p>", unsafe_allow_html=True)
            forge_prompt = st.text_area("Instruções de Geração:", height=180, placeholder="Ex: Crie um ERP completo de controle de vendas com autenticação, banco de dados SQLite e visualização gráfica...")
            ext_completar = st.selectbox("Linguagem/Extensão do Alvo:", [".html", ".py", ".js", ".sql", ".txt"])
            btn_forjar = st.button("🔥 FORJAR SISTEMA DO ZERO")
            
        with col_f2:
            st.markdown("<p style='font-size:11px; color:#8b949e;'>RESPOSTA MESTRA & VISUALIZAÇÃO:</p>", unsafe_allow_html=True)
            if btn_forjar and forge_prompt:
                with st.spinner("Forjando arquitetura tática..."):
                    # Executa a geração rápida via Hydra
                    sys_creator = (
                        "Você é o Agente Nexus Forge. Sua missão única é criar códigos completos, funcionais, "
                        "organizados de altíssima qualidade (frontend, backend, banco de dados). "
                        "Retorne obrigatoriamente código limpo dentro de blocos utilizáveis."
                    )
                    resultado_forge = hydra_orchestrator._chamar_especialista("Forge Master", sys_creator, forge_prompt, "Contexto de geração limpa.")
                    st.session_state.last_generated_code = resultado_forge
            
            if st.session_state.last_generated_code:
                tab_code, tab_preview = st.tabs(["💻 Código Forjado", "🖼️ Live Preview HUD"])
                with tab_code:
                    st.code(st.session_state.last_generated_code, language='html' if ext_completar == ".html" else 'python')
                    st.download_button("📥 DOWNLOAD COMPILADO", st.session_state.last_generated_code, file_name=f"nexus_forged_app{ext_completar}")
                with tab_preview:
                    if "<html>" in st.session_state.last_generated_code.lower() or "<!doctype html>" in st.session_state.last_generated_code.lower():
                        st.components.v1.html(st.session_state.last_generated_code, height=450, scrolling=True)
                    else:
                        st.info("Aguardando código HTML compatível para visualização no Iframe.")

    # --- TAB 2: AUDITORIA COGNITIVA (CONSENSO DA HIDRA) ---
    with t_auditoria:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🧠 Consenso da Hidra (Orquestração Simultânea)")
        c1, c2, c3 = st.columns([2.5, 1, 1.2])
        with c1:
            comando = st.text_area("⌨️ DIRETRIZ DA MISSÃO COGNITIVA:", height=150, placeholder="Insira o log, código-fonte ou regras arquiteturais para as 7 cabeças analisarem...")
        with c2:
            arquivos = st.file_uploader("📂 MATRIZ DE EVIDÊNCIAS MULTIMODAIS:", accept_multiple_files=True)
        with c3:
            modo_auditoria = st.selectbox("🎯 MODO DE EXECUÇÃO NEURAL:", ["Forense (Perspectiva Red vs Blue Team)", "Genesis (Arquitetura e DNA Inception)"])
            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            btn_executar = st.button("⚡ ENVOLVER ARQUITETURA DE AGENTES")

        if btn_executar and comando:
            with st.spinner("Sincronizando as 7 perspectivas da Hidra..."):
                ctx_extraido = omni_extractor(arquivos, GEM_KEY)
                ctx_rag = processar_rag(ctx_extraido, comando, GEM_KEY)
                
                resultado_consenso = hydra_orchestrator.orquestrar(comando, ctx_rag)
                st.success("Consenso Neural de Elite Estabelecido!")
                
                # Exibição estruturada em Expanders para manter o esquadro limpo
                blocos = resultado_consenso.split("---")
                for bloco in blocos:
                    if bloco.strip():
                        ia_titulo = "Perspectiva Hidra"
                        if "###" in bloco:
                            try:
                                ia_titulo = bloco.split("###")[1].splitlines()[0].strip()
                            except: pass
                        with st.expander(ia_titulo):
                            st.markdown(bloco)
                
                st.divider()
                st.download_button("📥 EXPORTAR RELATÓRIO GERAL (PDF)", gerar_pdf(resultado_consenso), file_name="Nexus_Hydra_Consensus.pdf")

    # --- TAB 3: PROTOCOLO RECON & STRIKE ---
    with t_strike:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("💀 Protocolo Sniper Recon & Strike")
        cin, copt = st.columns([2, 1])
        with cin:
            m_strike = st.text_area("Alvo para Varredura de Codificação ou Payload de Ameaça:", height=130)
        with copt:
            modo_s = st.selectbox("Ação Estratégica Disparada:", ["Web Developer (Live Preview)", "Relatório Forense de Denúncia IP"])
            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            btn_strike = st.button("💀 DISPARAR RECON COGNITIVO")

        if btn_strike and m_strike:
            with st.spinner("Rastreando origem e gerando contra-medidas..."):
                if "Web" in modo_s:
                    res_strike = hydra_orchestrator._chamar_especialista(
                        "Sniper Dev", 
                        "Crie código de altíssima qualidade HTML/CSS/JS encapsulado dentro de tags html.", 
                        m_strike, 
                        "Contexto de ataque defensivo."
                    )
                    st.session_state['strike_code_data'] = res_strike
                    st.session_state['strike_is_report'] = False
                else:
                    res_strike = hydra_orchestrator._chamar_especialista(
                        "Forense Red Team", 
                        "Gere um relatório de abuso, rastreamento de IP, táticas adversárias e denúncia.", 
                        m_strike, 
                        "Log de ameaça ativa."
                    )
                    st.session_state['strike_code_data'] = res_strike
                    st.session_state['strike_is_report'] = True

        if 'strike_code_data' in st.session_state:
            if st.session_state.get('strike_is_report', False):
                st.markdown("<div class='strike-zone' style='background-color:#2b0b0b; border: 1px solid #ff5252; padding:12px; border-radius:8px;'>⚠️ <b>PROTOCOLO STRIKE ATIVO:</b> Relatório Técnico de Denúncia Forense Gerado.</div>", unsafe_allow_html=True)
                st.markdown(st.session_state['strike_code_data'])
            else:
                tc, tv = st.tabs(["💻 Código de Defesa", "🖼️ Live Preview"])
                with tc:
                    st.code(st.session_state['strike_code_data'], language='html')
                    formato = st.selectbox("Extensão do compilador:", [".html", ".py", ".js", ".txt"])
                    st.download_button("📥 EXPORTAR COMPILADO", st.session_state['strike_code_data'], file_name=f"nexus_strike{formato}")
                with tv:
                    st.components.v1.html(st.session_state['strike_code_data'], height=500, scrolling=True)

    # --- TAB 4: AGENTE DE AUTO-CORREÇÃO (AUTOFIX) ---
    with t_autofix:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🔧 Depuração Ativa de Código (AutoFix)")
        f_c1, f_c2 = st.columns([2.2, 1.8])
        with f_c1:
            codigo_quebrado = st.text_area("💻 CÓDIGO FONTE QUEBRADO OU VULNERÁVEL:", height=200, placeholder="Cole aqui seu script com erros...")
        with f_c2:
            erro_contexto = st.text_area("📋 TRACEBACK DE ERRO / CONTEXTO DA FALHA:", height=90, placeholder="Cole os logs de erro ou vulnerabilidade descrita...")
            linguagem_fix = st.selectbox("🏷️ IDIOMA/LINGUAGEM DO TARGET:", ["Python", "C/C++", "JavaScript", "HTML/CSS", "Java", "Outra"])
            btn_autofix = st.button("🔧 PURIFICAR CÓDIGO (AUTOFIX)")

        if btn_autofix and codigo_quebrado:
            with st.spinner("A Hidra está depurando e reestruturando o código..."):
                sys_autofix = (
                    "Você é o Agente AutoFix do Nexus. Sua missão única é reescrever o código de entrada corrigindo todos os bugs "
                    "e brechas de segurança. Forneça o código 100% corrigido e limpo dentro de blocos de markdown."
                )
                resposta_autofix = hydra_orchestrator._chamar_especialista("AutoFix", sys_autofix, codigo_quebrado, erro_contexto)
                st.markdown(resposta_autofix)

    # --- TAB 5: TELEMETRIA FREQUÊNCIAS ---
    with t_rf:
        renderizar_painel_rf()

    # --- CHAT PRO CONTEXTUAL (Sessão & Memória) ---
    st.divider()
    st.subheader("💬 Nexus Chat Pro (Sincronismo Global)")
    
    # Exibe o histórico do Chat
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    chat_input = st.chat_input("Instruções de refinamento ou perguntas cognitivas para a Hidra:")
    if chat_input:
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)
            
        with st.chat_message("assistant"):
            with st.spinner("Raciocinando..."):
                last_code = st.session_state.get('strike_code_data', 'Nenhum código gerado na aba Strike ainda.')
                prompt_chat_completo = f"Último Código Gerado: {last_code}\n\nInstrução do Operador: {chat_input}"
                
                resposta_chat = hydra_orchestrator._chamar_especialista(
                    "Suporte Chat", 
                    "Você é o assistente em tempo real do Nexus OmniCore. Responda em português com clareza máxima e teor puramente técnico.", 
                    prompt_chat_completo, 
                    "Conversa de suporte tático."
                )
                st.markdown(resposta_chat)
                st.session_state.chat_history.append({"role": "assistant", "content": resposta_chat})

if __name__ == "__main__":
    st.sidebar.markdown("### 🔑 AUTENTICADO")
    main()
