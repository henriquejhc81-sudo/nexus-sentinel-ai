"""
=============================================================================
🛡️ NEXUS OMNICORE v6.5 - CYBER-HUD THEME & ADVANCED SPECTRUM ENGINE
=============================================================================
Fusão Total: DNA v1-v6.4 Preservado + Interface Ultra-Competitiva de Elite
=============================================================================
"""

import streamlit as st
import io
import re
import time
import concurrent.futures
import pandas as pd
from PIL import Image

# Validação e carregamento seguro do arsenal de bibliotecas
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

# Configuração tática da página para modo Wide com injeção estética customizada
st.set_page_config(page_title="Nexus OmniCore v6.5", page_icon="🛡️", layout="wide")

# 🖥️ CORE DESIGN NEXUS v6.5: Transformação Completa de Layout (Inspirado em Base44 & Horizons)
st.markdown("""
    <style>
    /* Customização do Fundo e Container Principal */
    .stApp {
        background-color: #030712 !important;
        background-image: radial-gradient(circle at 50% 50%, #0f172a 0%, #030712 100%) !important;
        color: #f3f4f6 !important;
        font-family: 'JetBrains Mono', 'Courier New', Courier, monospace !important;
    }
    
    /* Abas Customizadas no Estilo Cyber-Glow */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #0b1329;
        padding: 8px 16px;
        border-radius: 8px;
        border: 1px solid #1e293b;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre;
        background-color: transparent;
        border-radius: 4px;
        color: #94a3b8 !important;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #A51C30 0%, #e11d48 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(225, 29, 72, 0.4);
    }
    
    /* Cards de Status (Militar HUD KPI) */
    .hud-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #1e293b;
        border-left: 4px solid #e11d48;
        padding: 12px;
        border-radius: 6px;
        backdrop-filter: blur(10px);
        margin-bottom: 10px;
    }
    .hud-card-green {
        border-left: 4px solid #10b981 !important;
    }
    .hud-title { font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }
    .hud-value { font-size: 18px; color: #f3f4f6; font-weight: bold; margin-top: 4px; }
    
    /* Botão de Disparo Supremo */
    .stButton>button {
        background: linear-gradient(135deg, #A51C30 0%, #e11d48 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: 1px;
        border-radius: 6px !important;
        border: none !important;
        padding: 14px 20px !important;
        box-shadow: 0 4px 14px rgba(165, 28, 48, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(225, 29, 72, 0.6) !important;
    }
    
    /* Ajustes em inputs e caixas de texto */
    .stTextArea textarea {
        background-color: #0b1329 !important;
        color: #38bdf8 !important;
        border: 1px solid #1e293b !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 🛡️ DNA SENTINEL: Motor de Proteção de Privacidade (Animização PII)
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
                texto_extraido += genai.GenerativeModel('gemini-1.5-flash').generate_content(["Extraia toda a telemetria, texto ou dados técnicos contidos nesta imagem de forma minuciosa.", Image.open(io.BytesIO(file_bytes))]).text
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
                if "429" in str(e): 
                    time.sleep(2 ** attempt)
                else: 
                    return f"Erro na chamada da engine: {e}"
        return "Falha crítica por saturação de Rate Limit."

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

# 📡 NOVO DNA OMNICORE: Painel de Monitoramento Espectral RF (Trabalho Acadêmico)
def renderizar_painel_rf():
    st.markdown("<br>", unsafe_allow_html=True)
    
    if "historico_rf" not in st.session_state:
        st.session_state.historico_rf = {f"CH {i}": 0 for i in range(2, 31)}
    
    col_painel, col_acoes = st.columns([3, 1])
    
    with col_acoes:
        st.markdown("<div class='hud-card'><div class='hud-title'>AGENTE DE HARDWARE</div><div class='hud-value' style='color:#10b981;'>ESP32 + NRF24L01</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='hud-card'><div class='hud-title'>STATUS DA PORTA</div><div class='hud-value' style='color:#38bdf8;'>UPLINK READY</div></div>", unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
        canal_teste = st.selectbox("Simular Detecção de Portadora (Teste Local):", [f"CH {i}" for i in range(2, 31)])
        if st.button("📥 Injetar Sinal Capturado"):
            st.session_state.historico_rf[canal_teste] += 1
            st.rerun()
            
        if st.button("🧹 Resetar Gráfico"):
            st.session_state.historico_rf = {f"CH {i}": 0 for i in range(2, 31)}
            st.rerun()

    with col_painel:
        df_rf = pd.DataFrame(list(st.session_state.historico_rf.items()), columns=["Canal", "Picos Ativos"])
        st.bar_chart(df_rf, x="Canal", y="Picos Ativos", color="#e11d48")

# 🕹️ CORE EXECUTÁVEL PRINCIPAL
def main():
    # 🏁 TOP HUD HEADERS (Estilo Palantir / Hostinger Horizons)
    h1, h2, h3, h4 = st.columns(4)
    with h1: st.markdown("<div class='hud-card'><div class='hud-title'>SISTEMA OPERACIONAL</div><div class='hud-value' style='color:#e11d48;'>NEXUS v6.5</div></div>", unsafe_allow_html=True)
    with h2: st.markdown("<div class='hud-card hud-card-green'><div class='hud-title'>ENGINE DE CONTEXTO</div><div class='hud-value'>RAG + VETORIAL</div></div>", unsafe_allow_html=True)
    with h3: st.markdown("<div class='hud-card hud-card-green'><div class='hud-title'>AUDITORIA MULTI-AGENTE</div><div class='hud-value'>ACTIVE LOCK</div></div>", unsafe_allow_html=True)
    with h4: st.markdown("<div class='hud-card'><div class='hud-title'>NUCLEO DE INTELIGENCIA</div><div class='hud-value' style='color:#38bdf8;'>LLAMA 3.3 ULTRA</div></div>", unsafe_allow_html=True)

    GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    
    tab_auditoria, tab_rf = st.tabs(["⚡ AUDITORIA FORENSE MULTI-AGENTE", "📡 MONITORAMENTO DE ESPECTRO (HARDWARE)"])
    
    with tab_auditoria:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: 
            comando = st.text_area("⌨️ PROTOCOLO DE ALVO (Injete Códigos, Arquiteturas ou Logs):", height=110, placeholder="Defina o escopo da auditoria ou análise estrutural...")
        with c2: 
            arquivos = st.file_uploader("📂 EVINDÊNCIAS MULTIMODAIS (Imagens/PDFs/Logs):", accept_multiple_files=True)
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
                        r_blue = executor.submit(engine._call_groq, "Aja como arquiteto sênior de Blue Team. Responda às críticas do Red Team propondo correções sólidas, mitigações práticas e defesas.", f"Alvo: {comando}\nContexto: {txt_refinado}").result()
                    
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
