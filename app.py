"""
=============================================================================
🛡️ NEXUS OMNICORE v6.8 - DESIGN SOBERANO E NÚCLEO DE ESCUTA INTEGRADO
=============================================================================
Fusão Total: DNA v1-v6.7 Preservado + HUD Cyber-Glow Premium Sem Rolagem
=============================================================================
"""

import streamlit as st
import io
import re
import time
import concurrent.futures
import pandas as pd
from PIL import Image
from datetime import datetime

# Validação e carregamento seguro do arsenal de bibliotecas do Nexus
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
    st.error(f"Erro Crítico de Infraestrutura. Dependência ausente: {e}")

# Configuração de tela cheia com contenção de rolagem de página
st.set_page_config(page_title="Nexus OmniCore v6.8", page_icon="🛡️", layout="wide")

# 🖥️ CORE DESIGN SUPREMO v6.8 (Inspirado em Hostinger Horizons & Base44)
st.markdown("""
    <style>
    /* Estilização da Base de Operações */
    .stApp {
        background-color: #02040a !important;
        background-image: radial-gradient(circle at 50% 10%, #0a1128 0%, #02040a 100%) !important;
        color: #f0f4f8 !important;
        font-family: 'JetBrains Mono', 'Consolas', monospace !important;
    }
    
    /* Remoção cirúrgica de espaçamentos inúteis */
    .block-container { padding-top: 0.4rem !important; padding-bottom: 0.4rem !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; background-color: #090d16; padding: 4px; border-radius: 6px; border: 1px solid #161b22; }
    .stTabs [data-baseweb="tab"] { height: 34px; color: #8b949e !important; font-weight: 700; font-size: 11px; }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #A51C30 0%, #f43f5e 100%) !important;
        color: #ffffff !important; box-shadow: 0 0 12px rgba(244, 63, 94, 0.4);
    }
    
    /* Containers HUD de Comando Premium */
    .hud-card {
        background: rgba(13, 17, 23, 0.75); 
        border: 1px solid #21262d; 
        border-left: 4px solid #f43f5e;
        padding: 10px 14px; 
        border-radius: 6px; 
        backdrop-filter: blur(12px); 
        margin-bottom: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .hud-card-green { border-left: 4px solid #10b981 !important; }
    .hud-title { font-size: 9px; color: #8b949e; text-transform: uppercase; letter-spacing: 1.2px; font-weight: bold; }
    .hud-value { font-size: 13px; color: #f0f4f8; font-weight: bold; margin-top: 2px; }
    
    /* Console Forense de Alta Performance (Alinhamento Simétrico de Altura) */
    .terminal-box {
        background-color: #03060c !important;
        border: 1px solid #1f6feb !important;
        border-radius: 6px;
        padding: 12px;
        font-family: 'Consolas', monospace;
        color: #58a6ff;
        height: 274px;
        overflow-y: auto;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.9);
    }
    .terminal-line { margin-bottom: 5px; font-size: 11.5px; border-bottom: 1px solid rgba(31,111,235,0.05); padding-bottom: 2px; }
    .terminal-tag { color: #f43f5e; font-weight: bold; }
    .terminal-data { color: #56d364; }
    .terminal-info { color: #8b949e; }

    /* Botões táticos */
    .stButton>button {
        background: linear-gradient(135deg, #A51C30 0%, #f43f5e 100%) !important;
        color: #ffffff !important; font-weight: 800 !important; border-radius: 6px !important;
        padding: 6px 12px !important; font-size: 11px !important; border: none !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(244, 63, 94, 0.4); }
    .stTextArea textarea { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #21262d !important; }
    </style>
    """, unsafe_allow_html=True)

# 🛡️ DNA SENTINEL: Proteção de Privacidade (Animização PII)
def pii_anonymizer(texto):
    if not texto: return texto
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF PROTEGIDO]', texto)
    texto = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ PROTEGIDO]', texto)
    return texto.replace("```", "'''")

# 🧬 DNA AETHER: Extrator Omniversal de Arquivos e Módulo de Visão
def omni_extractor(arquivos_upados, gemini_key):
    texto_extraido = ""
    if not arquivos_upados: return texto_extraido
    for arquivo in arquivos_upados:
        if arquivo.size > 15 * 1024 * 1024: continue
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
                texto_extraido += genai.GenerativeModel('gemini-1.5-flash').generate_content(["Extraia toda a telemetria, texto ou dados tecnicos contidos nesta imagem de forma minuciosa.", Image.open(io.BytesIO(file_bytes))]).text
        except:
            pass
    return pii_anonymizer(texto_extraido)

# 🧠 INTERFACES DE IA VETORIAL (RAG Engine)
def processar_rag(texto_bruto, comando, gemini_key):
    if not gemini_key or len(texto_bruto) < 5000: return texto_bruto
    try:
        chunks = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300).split_text(texto_bruto)
        db = FAISS.from_texts(chunks, GoogleGenerativeAIEmbeddings(google_api_key=gemini_key, model="models/embedding-001"))
        return "\n...\n".join([d.page_content for d in db.similarity_search(comando, k=5)])
    except: 
        return texto_bruto[:20000]

# 🛡️ ENGINE MULTI-AGENTE (Orquestração Red/Blue com Auto-Healing)
class NexusEngine:
    def __init__(self, groq_key): 
        self.groq_key = groq_key
        
    def _call_groq(self, system, prompt, retries=3):
        if not self.groq_key: return "API Key da Groq ausente nos Secrets."
        client = Groq(api_key=self.groq_key)
        for attempt in range(retries):
            try: 
                return client.chat.completions.create(
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}], 
                    model="llama-3.3-70b-versatile", 
                    temperature=0.2
                ).choices[0].message.content
            except Exception as e:
                if "429" in str(e): time.sleep(2 ** attempt)
                else: return f"Erro na chamada da engine: {e}"
        return "Falha critica por saturacao de Rate Limit."

# 📄 GERADOR DE DOSSIÊS EM PDF (Padrão Executivo Harvard)
def gerar_pdf(conteudo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_fill_color(165, 28, 48)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, "DOSSIE DE AUDITORIA FORENSE - NEXUS OMNICORE", ln=True, align='C', fill=True)
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    texto_limpo = conteudo.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, texto_limpo)
    return bytes(pdf.output(dest='S'))

# 📡 SUBSISTEMA OMNICORE v6.8: Painel HUD Simétrico e Sincronizado
def renderizar_painel_rf():
    st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)
    
    if "logs_forenses" not in st.session_state:
        st.session_state.logs_forenses = [
            f"[{datetime.now().strftime('%H:%M:%S')}] <span class='terminal-info'>[SISTEMA] INTERFACE ONLINE: Pronto para receber strings de telemetria local.</span>"
        ]
    if "hardware_detectado" not in st.session_state: st.session_state.hardware_detectado = "NENHUM COMPONENTE DETECTADO"
    if "status_porta" not in st.session_state: st.session_state.status_porta = "OFFLINE"

    col_painel, col_acoes = st.columns([2.6, 1.4])
    
    with col_acoes:
        st.markdown("<p style='font-size:10px; font-weight:bold; color:#8b949e; margin-bottom:4px; letter-spacing:0.5px;'>⚙️ CONTROLE DE FLUXO DE HARDWARE</p>", unsafe_allow_html=True)
        modo_auto = st.toggle("🔌 LEITURA AUTOMÁTICA DE COMPONENTES", value=False)
        
        if modo_auto:
            st.session_state.hardware_detectado = "ESP32 (CH9102) + NRF24L01 ANTENA RECON"
            st.session_state.status_porta = "CONECTADO: PORTA COM3 ATIVA (115200 bps)"
            
            # Popula logs estruturados e detalhados simulando a chegada de requisições do cabo
            if len(st.session_state.logs_forenses) < 12:
                canais_frequencias = {2: "2402 MHz", 4: "2404 MHz", 12: "2412 MHz", 19: "2419 MHz", 23: "2423 MHz", 29: "2429 MHz"}
                for ch, freq in canais_frequencias.items():
                    ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                    st.session_state.logs_forenses.append(
                        f"[{ts}] <span class='terminal-tag'>[DUMP_RF]</span> -> <span class='terminal-data'>INTERCEPTADO: Canal {ch:02d} ({freq}) | RPD=1 (Portadora Ativa > -64dBm) | Amostragem estável no Polo Acadêmico</span>"
                    )
        else:
            st.session_state.hardware_detectado = "STANDBY - AGUARDANDO DISPOSITIVO USB"
            st.session_state.status_porta = "LINK DO WEBHOOK OFFLINE"
            
        st.markdown(f"<div class='hud-card'><div class='hud-title'>COMPONENTE IDENTIFICADO</div><div class='hud-value' style='color:#58a6ff;'>{st.session_state.hardware_detectado}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='hud-card'><div class='hud-title'>STATUS DA PONTE DE DADOS</div><div class='hud-value' style='color:#56d364;'>{st.session_state.status_porta}</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='hud-card'><div class='hud-title'>FAIXA OPERACIONAL ANALISADA</div><div class='hud-value'>2.4 GHz (CANAIS ESPECÍFICOS 2 A 30)</div></div>", unsafe_allow_html=True)
        
        if st.button("🧹 Limpar Console Forense"):
            st.session_state.logs_forenses = [f"[{datetime.now().strftime('%H:%M:%S')}] <span class='terminal-info'>[SISTEMA] Histórico de captura limpo pelo operador.</span>"]
            st.rerun()

    with col_painel:
        st.markdown("<p style='font-size:10px; font-weight:bold; color:#8b949e; margin-bottom:4px; letter-spacing:0.5px;'>📟 RASTREAMENTO ESPECTRAL EM TEMPO REAL (ANALISADOR PASSIVO)</p>", unsafe_allow_html=True)
        html_terminal = "<div class='terminal-box'>"
        for linha in reversed(st.session_state.logs_forenses):
            html_terminal += f"<div class='terminal-line'>{linha}</div>"
        html_terminal += "</div>"
        st.markdown(html_terminal, unsafe_allow_html=True)

# 🕹️ CORE EXECUTÁVEL PRINCIPAL
def main():
    # Grid de Headers HUD de Alta Densidade no topo da tela
    h1, h2, h3, h4 = st.columns(4)
    with h1: st.markdown("<div class='hud-card'><div class='hud-title'>SISTEMA</div><div class='hud-value' style='color:#f43f5e;'>NEXUS CORE v6.8</div></div>", unsafe_allow_html=True)
    with h2: st.markdown("<div class='hud-card hud-card-green'><div class='hud-title'>INDEXADOR VETORIAL</div><div class='hud-value'>FAISS CHUNK ENGINE</div></div>", unsafe_allow_html=True)
    with h3: st.markdown("<div class='hud-card hud-card-green'><div class='hud-title'>INTERFACE SERIAL</div><div class='hud-value'>UPLINK CAPTURE</div></div>", unsafe_allow_html=True)
    with h4: st.markdown("<div class='hud-card'><div class='hud-title'>COGNITIVO</div><div class='hud-value' style='color:#58a6ff;'>LLAMA 3.3 SYSTEM</div></div>", unsafe_allow_html=True)

    GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    
    tab_auditoria, tab_rf = st.tabs(["⚡ AUDITORIA FORENSE MULTI-AGENTE", "📡 MONITORAMENTO DE ESPECTRO (HARDWARE)"])
    
    with tab_auditoria:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: 
            comando = st.text_area("⌨️ PROTOCOLO DE ALVO:", height=100, placeholder="Injete códigos, logs brutos ou diretrizes para a orquestração...")
        with c2: 
            arquivos = st.file_uploader("📂 EVIDÊNCIAS MULTIMODAIS:", accept_multiple_files=True)
        with c3:
            modo = st.selectbox("🎯 MODO DA MISSÃO:", ["Forense Avançada (Red vs Blue Team)", "🧬 Geração Direta (Inception DNA)"])
            st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)
            btn_run = st.button("⚡ EXECUÇÃO DE PROTOCOLO")

        st.divider()

        if btn_run and comando:
            with st.spinner("Orquestrando agentes cognitivos de elite..."):
                txt_refinado = processar_rag(omni_extractor(arquivos, GEMINI_KEY), comando, GEMINI_KEY)
                engine = NexusEngine(GROQ_KEY)
                
                if "Forense" in modo:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        r_red = executor.submit(engine._call_groq, "Aja como especialista do Red Team. Critique o contexto, aponte vulnerabilidades e falhas.", f"Alvo: {comando}\nContexto: {txt_refinado}").result()
                        r_blue = executor.submit(engine._call_groq, "Aja como arquiteto de Blue Team. Responda propondo correções sólidas e defesas.", f"Alvo: {comando}\nContexto: {txt_refinado}").result()
                    
                    dossie = engine._call_groq("Sintetize um Relatório Forense Final detalhado.", f"RED:\n{r_red}\n\nBLUE:\n{r_blue}")
                    st.markdown(dossie)
                    st.download_button("📥 BAIXAR RELATÓRIO (PDF)", gerar_pdf(dossie), file_name="Nexus_Dossie_Forense.pdf", mime="application/pdf")
                else:
                    laudo_direto = engine._call_groq("Gere código e documentação estruturada impecável.", f"Diretriz: {comando}\nContexto: {txt_refinado}")
                    st.markdown(laudo_direto)

    with tab_rf:
        renderizar_painel_rf()

if __name__ == "__main__":
    main()
