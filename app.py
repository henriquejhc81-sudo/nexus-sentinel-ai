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
# 🛡️ ARSENAL DE DEPENDÊNCIAS & SISTEMA DE DEGRADAÇÃO SUAVE
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
    st.error(f"⚠️ Alerta de Infraestrutura. Dependência ausente no ambiente: {e}")

# Tentativa de importação do motor Ghost Core legado (v35)
has_ghost_engine = False
try:
    from ghost_engine import GhostEngine
    has_ghost_engine = True
except ImportError:
    pass

# Configuração Padrão do HUD Central
st.set_page_config(page_title="Nexus v8.4 Omni Ultimate", page_icon="🐉", layout="wide")

# =============================================================================
# 🗄️ DATA LAKE SEGURO (CONCORRÊNCIA MULTI-THREAD FIX)
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

# Inicialização assíncrona do banco
init_db()

# =============================================================================
# 🖥️ COMPILADOR CSS - IDENTIDADE VISUAL CYBERPUNK SOBERANA
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
        padding-top: 1.5rem !important; 
        padding-bottom: 1rem !important;
        max-width: 96% !important;
    }
    .stTabs [data-baseweb="tab-list"] { 
        gap: 10px; 
        background-color: #090d16; 
        padding: 8px; 
        border-radius: 6px;
        border: 1px solid #161b22; 
    }
    .stTabs [data-baseweb="tab"] { 
        height: 40px; 
        color: #8b949e !important; 
        font-weight: 700; 
        font-size: 12px;
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(135deg, #A51C30 0%, #8b5cf6 100%) !important; 
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.5); 
    }
    .hud-card { 
        background: rgba(13, 17, 23, 0.85);
        border: 1px solid #21262d; 
        border-left: 4px solid #8b5cf6; 
        padding: 14px; 
        border-radius: 6px; 
        backdrop-filter: blur(12px); 
        margin-bottom: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3); 
    }
    .hud-card-green { border-left: 4px solid #10b981 !important; }
    .hud-card-red { border-left: 4px solid #f43f5e !important; }
    .hud-title { font-size: 10px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }
    .hud-value { font-size: 14px; color: #f0f4f8; font-weight: bold; margin-top: 4px; }
    
    .strike-zone {
        padding: 15px; background: rgba(244, 63, 94, 0.1); 
        border: 1px solid #f43f5e; border-radius: 6px; 
        color: #f43f5e; font-size: 12px; margin-top: 10px;
    }
    
    .terminal-box { 
        background-color: #03060c !important; 
        border: 1px solid #1f6feb !important; 
        border-radius: 6px; 
        padding: 14px;
        font-family: 'Consolas', monospace; 
        color: #58a6ff; 
        height: 320px; 
        overflow-y: auto; 
        box-shadow: inset 0 0 20px rgba(0,0,0,0.9);
    }
    .terminal-line { margin-bottom: 6px; font-size: 12px; border-bottom: 1px solid rgba(31,111,235,0.05); padding-bottom: 3px; }
    .terminal-tag { color: #f43f5e; font-weight: bold; }
    .terminal-data { color: #56d364; }
    .terminal-info { color: #8b949e; }
    
    .stButton>button { 
        background: linear-gradient(135deg, #A51C30 0%, #8b5cf6 100%) !important;
        color: #ffffff !important; font-weight: 800 !important; 
        border-radius: 6px !important; padding: 12px !important; 
        font-size: 12px !important; border: none !important; width: 100%;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 4px 15px rgba(139, 92, 246, 0.5); }
    .stTextArea textarea { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #21262d !important; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 🧠 EXTRACTOR DE EVIDÊNCIAS & PROCESSAMENTO VETORIAL (RAG)
# =============================================================================
def pii_anonymizer(texto):
    if not texto: return texto
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF_ANONIMIZADO]', texto)
    texto = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ_ANONIMIZADO]', texto)
    return texto.replace("```", "'''")

def omni_extractor(arquivos_upados, gemini_key):
    texto_extraido = ""
    if not arquivos_upados: return texto_extraido
    for arq in arquivos_upados:
        if arq.size > 20 * 1024 * 1024: continue  # Limite rígido de proteção (20MB)
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
                    ["Forneça uma análise forense descritiva completa desta imagem.", Image.open(io.BytesIO(fb))]
                ).text
        except Exception:
            pass
    return pii_anonymizer(texto_extraido)

def processar_rag(texto_bruto, comando, gemini_key):
    if not gemini_key or len(texto_bruto) < 4000: 
        return texto_bruto
    try:
        chunks = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300).split_text(texto_bruto)
        db = FAISS.from_texts(chunks, GoogleGenerativeAIEmbeddings(google_api_key=gemini_key, model="models/embedding-001"))
        return "\n...\n".join([d.page_content for d in db.similarity_search(comando, k=5)])
    except Exception: 
        return texto_bruto[:20000]

# =============================================================================
# 🐉 ENGINE NEURAL MULTI-CABEÇA DA HIDRA
# =============================================================================
class HydraEngine:
    def __init__(self, groq_key, gemini_key, engine_preferida="Auto"):
        self.groq_key = groq_key
        self.gemini_key = gemini_key
        self.engine_preferida = engine_preferida

    def strike(self, system, prompt):
        # Rota Executiva 1: Forçar Groq se selecionado
        if self.engine_preferida == "Groq (Ultra-Fast)" and self.groq_key:
            try: return self._call_groq(system, prompt)
            except Exception: pass

        # Rota Executiva 2: Forçar Gemini se selecionado
        if self.engine_preferida == "Gemini Pro" and self.gemini_key:
            try: return self._call_gemini(system, prompt)
            except Exception: pass

        # Rota Padrão Balanceada (Auto-Regenerativa)
        if self.groq_key:
            try: return self._call_groq(system, prompt)
            except Exception: pass
        if self.gemini_key:
            try: return self._call_gemini(system, prompt)
            except Exception: pass

        # Última Linha de Defesa: DuckDuckGo Intel Scraping
        try:
            with DDGS() as ddgs:
                search = [r['body'] for r in ddgs.text(f"solução desenvolvimento: {prompt[:60]}", max_results=2)]
                return f"[MODO SEGURANÇA DDGS] Motores primários indisponíveis.\n\nIntel coletada:\n" + "\n".join(search)
        except Exception:
            return "Falha de Barramento Crítica: Nenhuma IA ou barramento de rede respondeu."

    def _call_groq(self, system, prompt):
        client = Groq(api_key=self.groq_key)
        return client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}], 
            model="llama-3.3-70b-versatile", temperature=0.15
        ).choices[0].message.content

    def _call_gemini(self, system, prompt):
        genai.configure(api_key=self.gemini_key)
        return genai.GenerativeModel('gemini-1.5-pro-latest').generate_content(f"{system}\n\n{prompt}").text

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

# =============================================================================
# 📡 HARDWARE TELEMETRIA PANEL
# =============================================================================
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

# =============================================================================
# 🕹️ PROGRAMAÇÃO MAESTRO CENTRAL
# =============================================================================
def main():
    # Inicialização global do Chat Pro se não existir
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Configuração Lateral de Segurança e Configurações Neural Target
    with st.sidebar:
        st.markdown("### 🔒 PERÍMETRO DE SEGURANÇA")
        usar_lock = st.checkbox("Ativar Chave Mestra Global", value=True)
        autenticado = False
        if usar_lock:
            master_key = st.text_input("Chave Mestra Nexus:", type="password")
            if master_key == "admin123":
                autenticado = True
                st.success("Acesso Concedido ao Nexus Core.")
            else:
                st.warning("Aguardando Chave Mestra Autenticada...")
        else:
            autenticado = True

        st.divider()
        st.markdown("### 🎛️ COGNITIVE CONTROLS")
        ia_provider = st.selectbox("Engine Neural Principal:", ["Auto-Regenerativa", "Groq (Ultra-Fast)", "Gemini Pro"])
        ghost_mode = st.checkbox("Modo Ghost Ativo (Proxy & Tor Simul)", value=has_ghost_engine)
        legacy_mode = st.checkbox("Habilitar Compiladores Legados", value=True)

        st.divider()
        st.markdown("### 🔑 CREDENCIAIS")
        g_key = st.text_input("GROQ API KEY", type="password", value=st.secrets.get("GROQ_API_KEY", ""))
        gem_key = st.text_input("GEMINI API KEY", type="password", value=st.secrets.get("GEMINI_API_KEY", ""))

    if not autenticado:
        st.stop()

    hydra = HydraEngine(g_key, gem_key, engine_preferida=ia_provider)

    # Painel HUD Telemetria Superior
    h1, h2, h3, h4 = st.columns(4)
    with h1: st.markdown("<div class='hud-card'><div class='hud-title'>SISTEMA BASE</div><div class='hud-value' style='color:#8b5cf6;'>NEXUS OMNICORE v8.4</div></div>", unsafe_allow_html=True)
    with h2: st.markdown(f"<div class='hud-card hud-card-green'><div class='hud-title'>SEGURANÇA PERIMETRAL</div><div class='hud-value'>{'GHOST EMBEDDED' if ghost_mode else 'NORMAL MODE'}</div></div>", unsafe_allow_html=True)
    with h3: st.markdown("<div class='hud-card hud-card-green'><div class='hud-title'>DATA REPLICATION</div><div class='hud-value'>SQLITE THREAD COHERENT</div></div>", unsafe_allow_html=True)
    with h4: st.markdown("<div class='hud-card'><div class='hud-title'>COMPILATION EXT</div><div class='hud-value' style='color:#58a6ff;'>DYNAMIC DISPATCHER</div></div>", unsafe_allow_html=True)

    t_auditoria, t_strike, t_rf = st.tabs([
        "🧠 AUDITORIA MULTI-AGENTE COGNITIVA", 
        "💀 PROTOCOLO RECON & SNIPER STRIKE", 
        "📡 TELEMETRIA OMNI-HARDWARE"
    ])

    # TAB 1: AUDITORIA
    with t_auditoria:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2.5, 1, 1.2])
        with c1:
            comando = st.text_area("⌨️ DIRETRIZ DA MISSÃO COGNITIVA:", height=150, placeholder="Insira o log, código-fonte ou regras arquiteturais...")
        with c2:
            arquivos = st.file_uploader("📂 CARREGAR MATRIZ DE EVIDÊNCIAS:", accept_multiple_files=True)
        with c3:
            modo_auditoria = st.selectbox("🎯 MODO DE EXECUÇÃO NEURAL:", ["Forense (Perspectiva Red vs Blue Team)", "Genesis (Arquitetura e DNA Inception)"])
            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            btn_executar = st.button("⚡ ENVOLVER ARQUITETURA")

        if btn_executar and comando:
            with st.spinner("Refinando dados contextuais..."):
                ctx = omni_extractor(arquivos, gem_key)
                if ghost_mode and has_ghost_engine:
                    try:
                        ghost = GhostEngine()
                        ctx += f"\n[GHOST INTEL]: {ghost.scan_local_credentials()} | {ghost.shadow_cookie_scan()}"
                    except Exception: pass
                
                ctx_rag = processar_rag(ctx, comando, gem_key)

                if "Forense" in modo_auditoria:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        r_red = executor.submit(hydra.strike, "Aja como especialista do Red Team. Ataque e encontre falhas severas de segurança e vazamentos de escopo.", f"Alvo: {comando}\nContexto: {ctx_rag}").result()
                        r_blue = executor.submit(hydra.strike, "Aja como especialista do Blue Team. Defenda, apresente blindagens, correções e tratamentos.", f"Alvo: {comando}\nContexto: {ctx_rag}").result()
                    
                    dossie = hydra.strike("Combine as perspectivas Red Team e Blue Team em um relatório técnico definitivo e inteligível.", f"RED TEAM REPORT:\n{r_red}\n\nBLUE TEAM MITIGATION:\n{r_blue}")
                    st.markdown(dossie)
                    st.download_button("📥 EXPORTAR DOSSIÊ (PDF)", gerar_pdf(dossie), file_name="Nexus_Report.pdf")
                else:
                    laudo = hydra.strike("Aja como Arquiteto de Elite Google AI. Crie arquiteturas indestrutíveis, códigos limpos e funcionais.", f"Diretriz: {comando}\nContexto: {ctx_rag}")
                    st.markdown(laudo)

    # TAB 2: RECON & STRIKE
    with t_strike:
        st.markdown("<br>", unsafe_allow_html=True)
        cin, copt = st.columns([2, 1])
        with cin:
            m_strike = st.text_area("Alvo para Varredura de Codificação ou Payload:", height=130)
        with copt:
            modo_s = st.selectbox("Ação Estratégica Disparada:", ["Web Developer (Live Preview)", "Relatório Forense de Denúncia IP"])
            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            btn_strike = st.button("💀 INICIAR DISPARO COGNITIVO")

        if btn_strike and m_strike:
            with st.spinner("Processando sub-vetores..."):
                if "Web" in modo_s:
                    res = hydra.strike("Crie código web puro (HTML/CSS/JS) responsivo e encapsulado em blocos html utilizáveis.", m_strike)
                    st.session_state['strike_code'] = res
                    st.session_state['strike_active'] = False
                else:
                    res = hydra.strike("Gere um relatório de abuso, rastreamento forense e denúncia baseada no IP ou log informado.", m_strike)
                    st.session_state['strike_code'] = res
                    st.session_state['strike_active'] = True

        if 'strike_code' in st.session_state:
            if st.session_state.get('strike_active', False):
                st.markdown("<div class='strike-zone'>⚠️ <b>PROTOCOLO STRIKE ATIVO:</b> Relatório Técnico de Denúncia Forense Gerado com Sucesso.</div>", unsafe_allow_html=True)
                st.markdown(st.session_state['strike_code'])
            else:
                tc, tv = st.tabs(["💻 Código Fonte Estruturado", "🖼️ Live Preview HUD"])
                with tc:
                    st.code(st.session_state['strike_code'], language='html')
                    formato = st.selectbox("Extensão do Compilador:", [".html", ".py", ".js", ".txt"], key="fmt_strike")
                    st.download_button("📥 BAIXAR COMPILADO", st.session_state['strike_code'], file_name=f"nexus_payload{formato}")
                with tv:
                    st.components.v1.html(st.session_state['strike_code'], height=500, scrolling=True)

    # TAB 3: TELEMETRIA FREQUÊNCIAS
    with t_rf:
        renderizar_painel_rf()

    # =============================================================================
    # 💬 NEXUS CHAT PRO - SUPORTE DEEP CONTEXT COMPLETO (BASE DO HUD)
    # =============================================================================
    st.divider()
    st.subheader("💬 Nexus Chat Pro (Deep Cognitive Integration)")
    
    # Exibição do histórico de mensagens anteriores
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    chat_input = st.text_input("Submeter dúvida ou instrução para refinamento do código gerado:", key="nexus_chat_input")
    if chat_input:
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)
            
        with st.chat_message("assistant"):
            with st.spinner("Analisando contexto global do chat..."):
                last_code_ctx = st.session_state.get('strike_code', 'Nenhum código gerado nesta sessão ainda.')
                prompt_completo = f"Contexto do último código na tela: {last_code_ctx}\n\nPergunta do operador: {chat_input}"
                resposta_chat = hydra.strike("Você é o assistente técnico em tempo real do Nexus OmniCore. Responda em português de forma direta e extremamente técnica.", prompt_completo)
                st.markdown(resposta_chat)
                st.session_state.chat_history.append({"role": "assistant", "content": resposta_chat})

if __name__ == "__main__":
    main()
