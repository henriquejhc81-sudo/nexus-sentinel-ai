"""
=============================================================================
🛡️ NEXUS OMNICORE v6.0 - ARCHITECTURE & SECURITY ENGINE
=============================================================================
Fusão: Sentinel (Security/UI) + Aether (MoE/RAG) + Genesis (Multimodal Ingestion)
=============================================================================
"""

import streamlit as st
import pandas as pd
import io, re, time, logging
import concurrent.futures
from PIL import Image
import sqlite3 # Para MVP, migrar para SQLAlchemy no roadmap
from datetime import datetime

# Importações de IA
try:
    from groq import Groq
    import google.generativeai as genai
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ImportError as e:
    st.error(f"Erro de dependência. Execute: pip install -r requirements.txt. Detalhe: {e}")

# --- CONFIGURAÇÃO E DESIGN CYBER-SENTINEL ---
st.set_page_config(page_title="Nexus OmniCore v6.0", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050a18; color: #e0e0e0; }
    .stButton>button { 
        background: linear-gradient(135deg, #A51C30 0%, #ff5252 100%); 
        color: #fff; font-weight: 800; border-radius: 8px; border: none; transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(165, 28, 48, 0.4);
    }
    .status-box { 
        padding: 15px; border-radius: 10px; background: #0b0e14; 
        border: 1px solid #1e3a8a; border-left: 5px solid #00c853;
        margin-bottom: 20px; font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. MÓDULO DE SEGURANÇA E LGPD ---
def pii_anonymizer(texto):
    """Filtro avançado de PII."""
    if not texto: return texto
    # Mascara CPF e CNPJ
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF OMITIDO]', texto)
    texto = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ OMITIDO]', texto)
    # Mascara Emails
    texto = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[EMAIL OMITIDO]', texto)
    # Proteção básica contra Prompt Injection (escapando delimitadores)
    texto = texto.replace("```", "'''")
    return texto

# --- 2. CÓRTEX DE INGESTÃO OMNIVERSAL ---
def omni_extractor(arquivos_upados, gemini_key):
    """Extração segura limitando tamanho em memória."""
    texto_extraido = ""
    if not arquivos_upados: return texto_extraido
    
    for arquivo in arquivos_upados:
        # Prevenção contra Zip Bombs/Arquivos gigantes (> 10MB)
        if arquivo.size > 10 * 1024 * 1024:
            st.warning(f"Arquivo {arquivo.name} excedeu 10MB. Ignorado por segurança.")
            continue
            
        file_bytes = arquivo.getvalue()
        filename = arquivo.name.lower()
        
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(file_bytes))
                texto_extraido += f"\n--- {arquivo.name} ---\n{df.to_string(index=False)}"
            elif filename.endswith('.txt'):
                texto_extraido += f"\n--- {arquivo.name} ---\n{file_bytes.decode('utf-8', errors='ignore')}"
            elif filename.endswith(('.png', '.jpg', '.jpeg')):
                imagem_pil = Image.open(io.BytesIO(file_bytes))
                if gemini_key:
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(["Extraia o texto focado em falhas técnicas/dados.", imagem_pil])
                    texto_extraido += f"\n--- IMAGEM: {arquivo.name} ---\n{response.text}"
            else:
                st.info(f"Formato de {arquivo.name} requer bibliotecas adicionais (ex: PyPDF2/docx2txt).")
        except Exception as e:
            logging.error(f"Erro na extração de {arquivo.name}: {e}")
            st.error(f"Falha ao processar {arquivo.name}.")
            
    return pii_anonymizer(texto_extraido)

# --- 3. ORQUESTRAÇÃO MULTI-AGENTE (MoE) ---
class NexusEngine:
    def __init__(self, groq_key, gemini_key):
        self.groq_key = groq_key
        self.gemini_key = gemini_key

    def _call_groq(self, system, prompt, retries=3):
        """Chamada resiliente com fallback nativo (Anti-429)."""
        if not self.groq_key: return "Groq API Key ausente."
        client = Groq(api_key=self.groq_key)
        for attempt in range(retries):
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.2
                )
                return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e):
                    time.sleep(2 ** attempt) # Exponential backoff
                else:
                    return f"Erro Groq: {e}"
        return "Falha de Rate Limit (429) após múltiplas tentativas."

    def run_red_blue_team(self, comando, contexto):
        """Simulação Acadêmica de Ataque e Defesa."""
        sys_red = "Você é um Auditor Forense (Red Team). Busque vulnerabilidades, falhas arquiteturais e brechas de segurança no contexto."
        sys_blue = "Você é um Engenheiro de AppSec (Blue Team). Proponha correções sólidas, protocolos de defesa e refatoração para as falhas."
        sys_judge = "Você é o Nexus Sentinel. Consolide a análise do Red e Blue Team em um 'Relatório Forense de Elite' em Markdown."
        
        full_prompt = f"ALVO DA ANÁLISE: {comando}\n\nEVIDÊNCIAS:\n{contexto}"
        
        # Processamento Paralelo via Groq (Alta Velocidade)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            fut_red = executor.submit(self._call_groq, sys_red, full_prompt)
            fut_blue = executor.submit(self._call_groq, sys_blue, full_prompt)
            
            res_red = fut_red.result()
            res_blue = fut_blue.result()
            
        sintese_prompt = f"--- RED TEAM (ATAQUE) ---\n{res_red}\n\n--- BLUE TEAM (DEFESA) ---\n{res_blue}"
        relatorio_final = self._call_groq(sys_judge, sintese_prompt)
        return relatorio_final, res_red, res_blue

# --- 4. INTERFACE E COMANDO ---
def main():
    st.title("⚡ Nexus OmniCore v6.0")
    st.markdown("<div class='status-box'><b>STATUS:</b> ULTRA-BLACK ACTIVED | <b>INCEPTION DNA:</b> ON | <b>MODO:</b> ACADÊMICO</div>", unsafe_allow_html=True)
    
    GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    
    if not GROQ_KEY or not GEMINI_KEY:
        st.error("⚠️ Configure suas chaves de API nos Secrets do Streamlit para iniciar a ignição.")
        return

    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("📥 Recon & Ingestion")
        comando = st.text_area("Vetor de Análise (Ex: Analise este código para SQLi):", height=150)
        arquivos = st.file_uploader("Evidências (Imagens, Códigos, Logs)", accept_multiple_files=True)
        modo = st.radio("Pipeline:", ["Red/Blue Team (Auditoria)", "Criação (Single Agent)"])
        btn_run = st.button("ATIVAR PROTOCOLO")

    with col2:
        st.subheader("🛡️ Strike Terminal")
        if btn_run and comando:
            with st.spinner("Analisando assinaturas e inicializando orquestração MoE..."):
                texto_extraido = omni_extractor(arquivos, GEMINI_KEY) if arquivos else "Nenhum arquivo providenciado."
                engine = NexusEngine(GROQ_KEY, GEMINI_KEY)
                
                if modo == "Red/Blue Team (Auditoria)":
                    relatorio, red, blue = engine.run_red_blue_team(comando, texto_extraido)
                    
                    tab_final, tab_red, tab_blue = st.tabs(["Dossiê Executivo", "Logs Red Team", "Logs Blue Team"])
                    with tab_final: st.markdown(relatorio)
                    with tab_red: st.markdown(red)
                    with tab_blue: st.markdown(blue)
                else:
                    # Rota simplificada para criação
                    sys_creator = "Você é o Nexus Sentinel. Gere soluções ou código seguro baseando-se no pedido."
                    resposta = engine._call_groq(sys_creator, f"{comando}\n\nContexto:\n{texto_extraido}")
                    st.markdown(resposta)
                    
            st.success("Análise forense concluída e anonimizada.")

if __name__ == "__main__":
    main()
