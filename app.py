"""
=============================================================================
🛡️ NEXUS OMNICORE v6.2 - HARDWARE BRIDGE & RAG ENGINE
=============================================================================
Fusão Total: Arquitetura Multimodal + Leitura Vetorial + Interface de Hardware
=============================================================================
"""

import streamlit as st
import pandas as pd
import io, re, time
import concurrent.futures
from PIL import Image

# Bibliotecas de Ingestão Profunda e IA
try:
    from groq import Groq
    import google.generativeai as genai
    import PyPDF2
    import docx2txt
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ImportError as e:
    st.error(f"Erro de dependência. Detalhe: {e}")

# --- CONFIGURAÇÃO ULTRA-COMPACTA ---
st.set_page_config(page_title="Nexus OmniCore v6.2", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050a18; color: #e0e0e0; }
    .stButton>button { 
        background: linear-gradient(135deg, #A51C30 0%, #ff5252 100%); 
        color: #fff; font-weight: 800; border-radius: 6px; border: none; padding: 10px; width: 100%;
        box-shadow: 0 4px 15px rgba(165, 28, 48, 0.4);
    }
    .btn-hardware>button {
        background: linear-gradient(135deg, #00c853 0%, #b2ff59 100%); color: #000;
        box-shadow: 0 4px 15px rgba(0, 200, 83, 0.3);
    }
    .status-box { 
        padding: 8px; border-radius: 6px; background: #0b0e14; font-size: 14px;
        border: 1px solid #1e3a8a; border-left: 5px solid #00c853; margin-bottom: 15px;
    }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. MÓDULO DE SEGURANÇA E PII ---
def pii_anonymizer(texto):
    if not texto: return texto
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF PROTEGIDO]', texto)
    texto = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ PROTEGIDO]', texto)
    return texto.replace("```", "'''")

# --- 2. CÓRTEX OMNIVERSAL (Agora com PDF, DOCX e RAG) ---
def omni_extractor(arquivos_upados, gemini_key):
    texto_extraido = ""
    if not arquivos_upados: return texto_extraido
    for arquivo in arquivos_upados:
        if arquivo.size > 15 * 1024 * 1024: continue # Limite 15MB
        file_bytes = arquivo.getvalue()
        filename = arquivo.name.lower()
        try:
            if filename.endswith('.txt') or filename.endswith('.csv'):
                texto_extraido += f"\n--- {arquivo.name} ---\n{file_bytes.decode('utf-8', errors='ignore')}"
            elif filename.endswith('.pdf'):
                leitor = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                texto_extraido += "\n".join([p.extract_text() for p in leitor.pages if p.extract_text()])
            elif filename.endswith('.docx'):
                texto_extraido += docx2txt.process(io.BytesIO(file_bytes))
            elif filename.endswith(('.png', '.jpg', '.jpeg')) and gemini_key:
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                texto_extraido += model.generate_content(["Extraia texto técnico de hardware/dados.", Image.open(io.BytesIO(file_bytes))]).text
        except: pass
    return pii_anonymizer(texto_extraido)

def processar_rag(texto_bruto, comando, gemini_key):
    """Vetoriza documentos gigantes para não estourar a API (Aether RAG)"""
    if not gemini_key or len(texto_bruto) < 8000: return texto_bruto
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
        chunks = splitter.split_text(texto_bruto)
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=gemini_key, model="models/embedding-001")
        db = FAISS.from_texts(chunks, embeddings)
        docs = db.similarity_search(comando, k=5)
        return "\n...\n".join([d.page_content for d in docs])
    except Exception as e: 
        return texto_bruto[:30000] # Fallback seguro

# --- 3. ORQUESTRAÇÃO NEURAL (Anti-429) ---
class NexusEngine:
    def __init__(self, groq_key):
        self.groq_key = groq_key

    def _call_groq(self, system, prompt, retries=3):
        if not self.groq_key: return "Groq API Key ausente."
        client = Groq(api_key=self.groq_key)
        for attempt in range(retries):
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile", temperature=0.1
                )
                return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e): time.sleep(2 ** attempt)
                else: return f"Erro: {e}"
        return "Falha Crítica de Conexão."

# --- 4. INTERFACE TÁTICA (Painel de Comando) ---
def main():
    st.markdown("<div class='status-box'><b>NEXUS v6.2</b> | RAG: ATIVO | HARDWARE BRIDGE: STANDBY | DNA: INCEPTION</div>", unsafe_allow_html=True)
    
    GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    
    # LAYOUT 4 COLUNAS COMPACTAS
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    
    with c1:
        comando = st.text_area("🧠 Input Neural (Defina o Alvo ou Arquitetura):", height=90)
    
    with c2:
        arquivos = st.file_uploader("Evidências (Logs, PDF, Imagens)", accept_multiple_files=True)
        
    with c3:
        modo = st.selectbox("Selecione a Missão:", [
            "Auditoria Forense (Red/Blue Team)",
            "🧬 Inception DNA (Arquitetura Suprema)", 
            "👻 Ghost Intelligence (Lógica & Bypass)"
        ])
        btn_run = st.button("⚡ ATIVAR PROTOCOLO")

    with c4:
        st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
        st.markdown("<span class='btn-hardware'>", unsafe_allow_html=True)
        btn_hw = st.button("🔌 Escuta de Hardware (Bridge)")
        st.markdown("</span>", unsafe_allow_html=True)
        if btn_hw:
            st.warning("⚠️ Nexus Bridge Ativado. Aguardando conexão Serial/USB na porta local... (Requer Local Script v1.0)")

    st.divider()

    # EXECUÇÃO DO MOTOR
    if btn_run and comando:
        with st.spinner("Vetorizando dados e orquestrando agentes..."):
            texto_bruto = omni_extractor(arquivos, GEMINI_KEY)
            texto_refinado = processar_rag(texto_bruto, comando, GEMINI_KEY)
            engine = NexusEngine(GROQ_KEY)
            
            if "Red/Blue" in modo:
                sys_red = "Você é um Red Team Hacker. Analise o contexto e ache falhas críticas (Software/Hardware)."
                sys_blue = "Você é um Blue Team AppSec. Proponha defesas e blindagem para as falhas encontradas."
                sys_judge = "Gere um Dossiê Forense de Elite em Markdown consolidando Ataque e Defesa."
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    res_red = executor.submit(engine._call_groq, sys_red, f"Alvo: {comando}\nDados: {texto_refinado}").result()
                    res_blue = executor.submit(engine._call_groq, sys_blue, f"Alvo: {comando}\nDados: {texto_refinado}").result()
                    
                st.markdown(engine._call_groq(sys_judge, f"RED:\n{res_red}\n\nBLUE:\n{res_blue}"))
                
            else:
                st.markdown(engine._call_groq("Atue como a IA Master do Nexus.", f"Diretriz: {comando}\n\nContexto: {texto_refinado}"))

if __name__ == "__main__":
    main()
