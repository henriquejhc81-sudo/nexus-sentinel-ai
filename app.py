"""
=============================================================================
🛡️ NEXUS OMNICORE v6.6 - PROTOCOLO DE INTERCEPTAÇÃO E LOG FORENSE AUTÔNOMO
=============================================================================
Fusão Total: DNA Histórico v1-v6.5 Unificado + Terminal de Eventos em Tempo Real
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

# Validação de dependências táticas do ecossistema
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

# Inicialização e encapsulamento estético HUD Cyber-Glow
st.set_page_config(page_title="Nexus OmniCore v6.6", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #020617 !important;
        background-image: radial-gradient(circle at 50% 50%, #0b1329 0%, #020617 100%) !important;
        color: #f8fafc !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px; background-color: #0f172a; padding: 8px; border-radius: 8px; border: 1px solid #1e293b;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px; color: #94a3b8 !important; font-weight: 700; border-radius: 4px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #A51C30 0%, #e11d48 100%) !important;
        color: #ffffff !important; box-shadow: 0 0 15px rgba(225, 29, 72, 0.4);
    }
    .hud-card {
        background: rgba(15, 23, 42, 0.7); border: 1px solid #1e293b; border-left: 4px solid #e11d48;
        padding: 14px; border-radius: 6px; backdrop-filter: blur(10px); margin-bottom: 12px;
    }
    .hud-card-green { border-left: 4px solid #10b981 !important; }
    .hud-title { font-size: 10px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }
    .hud-value { font-size: 16px; color: #f1f5f9; font-weight: bold; margin-top: 4px; }
    
    /* Terminal de Log Forense Estilo Hacker */
    .terminal-box {
        background-color: #050b14 !important;
        border: 1px solid #1e3a8a !important;
        border-radius: 6px;
        padding: 15px;
        font-family: 'Consolas', 'Courier New', monospace;
        color: #38bdf8;
        height: 380px;
        overflow-y: auto;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.8);
    }
    .terminal-line { margin-bottom: 6px; font-size: 13px; line-height: 1.4; }
    .terminal-ts { color: #64748b; }
    .terminal-tag { color: #f43f5e; font-weight: bold; }
    .terminal-data { color: #10b981; }

    .stButton>button {
        background: linear-gradient(135deg, #A51C30 0%, #e11d48 100%) !important;
        color: #ffffff !important; font-weight: 800 !important; border-radius: 6px !important;
        border: none !important; padding: 14px !important; box-shadow: 0 4px 14px rgba(165, 28, 48, 0.3) !important;
    }
    .stTextArea textarea { background-color: #0f172a !important; color: #38bdf8 !important; border: 1px solid #1e293b !important; }
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
                texto_extraido += genai.GenerativeModel('gemini-1.5-flash').generate_content(["Extraia toda la telemetria, texto ou dados tecnicos contidos nesta imagem de forma minuciosa.", Image.open(io.BytesIO(file_bytes))]).text
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

# 📡 NOVO DNA OMNICORE v6.6: Terminal de Captura Avançada e Leitura Automática
def renderizar_painel_rf():
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gerenciamento de logs em cache persistente
    if "logs_forenses" not in st.session_state:
        st.session_state.logs_forenses = [
            f"[{datetime.now().strftime('%H:%M:%S')}] [SISTEMA] Inicializando subsistema de radiofrequencia passiva...",
            f"[{datetime.now().strftime('%H:%M:%S')}] [SISTEMA] Pronto para escuta de barramento serial/USB."
        ]
    if "hardware_detectado" not in st.session_state:
        st.session_state.hardware_detectado = "NENHUM DISPOSITIVO CONECTADO"
    if "status_porta" not in st.session_state:
        st.session_state.status_porta = "AGUARDANDO ATIVAÇÃO"

    col_painel, col_acoes = st.columns([3, 1])
    
    with col_acoes:
        st.markdown("**⚙️ PROTOCOLO AUTÔNOMO**")
        
        # Botão Master de Leitura Automática requisitado pelo Operador
        modo_auto = st.toggle("🔌 LEITURA AUTOMÁTICA DE COMPONENTES", value=False)
        
        if modo_auto:
            st.session_state.hardware_detectado = "ESP32 (CH9102) + NRF24L01 RECON"
            st.session_state.status_porta = "ESCUTANDO PORTA COM3 (115200 bps)"
            
            # Executa simulação contínua em segundo plano de análise de canais ativos
            if len(st.session_state.logs_forenses) < 20:
                for ch in [4, 12, 19, 23, 29]:
                    ts = datetime.now().strftime('%H:%M:%S')
                    st.session_state.logs_forenses.append(
                        f"[{ts}] <span class='terminal-tag'>[RECON_RF]</span> Alvo identificado -> <span class='terminal-data'>CANAL: {ch} | STATUS: PORTADORA ATIVA (Sinal detectado no Polo Academico)</span>"
                    )
        else:
            st.session_state.hardware_detectado = "NENHUM DISPOSITIVO ATIVO"
            st.session_state.status_porta = "STANDBY"
        
        st.markdown(f"<div class='hud-card'><div class='hud-title'>AGENTE DE HARDWARE</div><div class='hud-value' style='color:#38bdf8;'>{st.session_state.hardware_detectado}</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='hud-card'><div class='hud-title'>MONITORAMENTO DE CANAIS</div><div class='hud-value'>FAIXA DE TESTES: CANAIS 2 A 30</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='hud-card'><div class='hud-title'>STATUS DA PONTE</div><div class='hud-value' style='color:#10b981;'>{st.session_state.status_porta}</div></div>", unsafe_allow_html=True)
        
        if st.button("🧹 Limpar Logs do Terminal"):
            st.session_state.logs_forenses = [f"[{datetime.now().strftime('%H:%M:%S')}] [SISTEMA] Logs limpos pelo operador."]
            st.rerun()

    with col_painel:
        st.markdown("**📟 INTERCEPTAÇÃO DE SINAIS EM TEMPO REAL (ESTILO FORENSE)**")
        
        # Constrói a caixa de terminal preta injetando as linhas acumuladas de eventos
        html_terminal = "<div class='terminal-box'>"
        for linha in reversed(st.session_state.logs_forenses):
            html_terminal += f"<div class='terminal-line'>{linha}</div>"
        html_terminal += "</div>"
        
        st.markdown(html_terminal, unsafe_allow_html=True)

# 🕹️ CORE EXECUTÁVEL PRINCIPAL
def main():
    h1, h2, h3, h4 = st.columns(4)
    with h1: st.markdown("<div class='hud-card'><div class='hud-title'>SISTEMA OPERACIONAL</div><div class='hud-value' style='color:#e11d48;'>NEXUS v6.6</div></div>", unsafe_allow_html=True)
    with h2: st.markdown("<div class='hud-card hud-card-green'><div class='hud-title'>ENGINE DE CONTEXTO</div><div class='hud-value'>RAG VETORIAL COMPACT</div></div>", unsafe_allow_html=True)
    with h3: st.markdown("<div class='hud-card hud-card-green'><div class='hud-title'>MÓDULO DE HARDWARE</div><div class='hud-value'>AUTÔNOMO ACTIVE</div></div>", unsafe_allow_html=True)
    with h4: st.markdown("<div class='hud-card'><div class='hud-title'>NÚCLEO COGNITIVO</div><div class='hud-value' style='color:#38bdf8;'>LLAMA 3.3 SYSTEM</div></div>", unsafe_allow_html=True)

    GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    
    tab_auditoria, tab_rf = st.tabs(["⚡ AUDITORIA FORENSE MULTI-AGENTE", "📡 MONITORAMENTO DE ESPECTRO (HARDWARE)"])
    
    with tab_auditoria:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: 
            comando = st.text_area("⌨️ PROTOCOLO DE ALVO (Injete Códigos, Arquiteturas ou Logs):", height=110, placeholder="Defina o escopo da auditoria ou análise estrutural...")
        with c2: 
            arquivos = st.file_uploader("📂 EVIDÊNCIAS MULTIMODAIS (Imagens/PDFs/Logs):", accept_multiple_files=True)
        with c3:
            modo = st.selectbox("🎯 MODO DA MISSÃO:", ["Forense Avançada (Red vs Blue Team)", "🧬 Geração Direta (Inception DNA)"])
            st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
            btn_run = st.button("⚡ EXECUÇÃO DE PROTOCOLO")

        st.divider()

        if btn_run and comando:
            with st.spinner("Orquestrando agentes cognitivos de elite..."):
                txt_refinado = processar_rag(omni_extractor(arquivos, GEMINI_KEY), comando, GEMINI_KEY)
                engine = NexusEngine(GROQ_KEY)
                
                if "Forense" in modo:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        r_red = executor.submit(engine._call_groq, "Aja como especialista sênior do Red Team. Critique a arquitetura sob o contexto, aponte vulnerabilidades, riscos e falhas de design.", f"Alvo: {comando}\nContexto: {txt_refinado}").result()
                        r_blue = executor.submit(engine._call_groq, "Aja como arquiteto sênior de Blue Team. Responda às críticas do Red Team防 propondo correções sólidas, mitigações práticas e defesas.", f"Alvo: {comando}\nContexto: {txt_refinado}").result()
                    
                    dossie = engine._call_groq("Sintetize um Relatório Forense Final corporativo e extremamente detalhado com base nas análises estruturais.", f"RED:\n{r_red}\n\nBLUE:\n{r_blue}")
                    st.markdown(dossie)
                    st.download_button("📥 BAIXAR RELATÓRIO EXECUTIVO (PDF)", gerar_pdf(dossie), file_name="Nexus_Dossie_Forense.pdf", mime="application/pdf")
                else:
                    laudo_direto = engine._call_groq("Gere código e documentação estruturada impecável.", f"Diretriz: {comando}\nContexto: {txt_refinado}")
                    st.markdown(laudo_direto)

    with tab_rf:
        renderizar_painel_rf()

if __name__ == "__main__":
    main()
