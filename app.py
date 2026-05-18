"""
=============================================================================
🛡️ NEXUS OMNICORE v6.1 - COMPACT ENGINE & VIBE CODING
=============================================================================
Fusão: Sentinel + Aether + Genesis | Layout Ultra-Compacto
=============================================================================
"""

import streamlit as st
import pandas as pd
import io, re, time, logging
import concurrent.futures
from PIL import Image
from datetime import datetime

# Importações de IA (Com a correção do Langchain)
try:
    from groq import Groq
    import google.generativeai as genai
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ImportError as e:
    st.error(f"Erro de dependência. Execute: pip install -r requirements.txt. Detalhe: {e}")

# --- CONFIGURAÇÃO E DESIGN ULTRA-COMPACTO ---
st.set_page_config(page_title="Nexus OmniCore v6.1", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050a18; color: #e0e0e0; }
    .stButton>button { 
        background: linear-gradient(135deg, #A51C30 0%, #ff5252 100%); 
        color: #fff; font-weight: 800; border-radius: 6px; border: none; padding: 10px; width: 100%;
        box-shadow: 0 4px 15px rgba(165, 28, 48, 0.4);
    }
    .status-box { 
        padding: 8px; border-radius: 6px; background: #0b0e14; font-size: 14px;
        border: 1px solid #1e3a8a; border-left: 5px solid #00c853; margin-bottom: 15px;
    }
    /* Compactando espaçamentos nativos do Streamlit */
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. MÓDULO DE SEGURANÇA E LGPD (Mantido intacto) ---
def pii_anonymizer(texto):
    if not texto: return texto
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF PROTEGIDO]', texto)
    texto = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ PROTEGIDO]', texto)
    texto = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[EMAIL PROTEGIDO]', texto)
    return texto.replace("```", "'''")

# --- 2. CÓRTEX DE INGESTÃO (Mantido intacto) ---
def omni_extractor(arquivos_upados, gemini_key):
    texto_extraido = ""
    if not arquivos_upados: return texto_extraido
    for arquivo in arquivos_upados:
        if arquivo.size > 10 * 1024 * 1024: continue
        file_bytes = arquivo.getvalue()
        filename = arquivo.name.lower()
        try:
            if filename.endswith('.txt') or filename.endswith('.csv'):
                texto_extraido += f"\n--- {arquivo.name} ---\n{file_bytes.decode('utf-8', errors='ignore')}"
            elif filename.endswith(('.png', '.jpg', '.jpeg')) and gemini_key:
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                texto_extraido += f"\n--- IMAGEM: {arquivo.name} ---\n" + model.generate_content(["Extraia texto técnico.", Image.open(io.BytesIO(file_bytes))]).text
        except: pass
    return pii_anonymizer(texto_extraido)

# --- 3. ORQUESTRAÇÃO MULTI-AGENTE (Evoluído) ---
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
                    model="llama-3.3-70b-versatile", temperature=0.2
                )
                return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e): time.sleep(2 ** attempt)
                else: return f"Erro Groq: {e}"
        return "Falha Anti-429 após múltiplas tentativas."

# --- 4. INTERFACE COMPACTA ---
def main():
    st.markdown("<div class='status-box'><b>NEXUS v6.1</b> | MOTOR: GROQ/GEMINI | STATUS: ONLINE | DNA: INCEPTION</div>", unsafe_allow_html=True)
    
    GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    
    if not GROQ_KEY or not GEMINI_KEY:
        st.warning("⚠️ Chaves de API não configuradas nos Secrets.")
        return

    # LAYOUT HORIZONTAL (Tudo em um bloco)
    c1, c2, c3 = st.columns([2, 1, 1])
    
    with c1:
        comando = st.text_area("Comando Tático (Vibe Coding, Auditoria ou Criação):", height=100)
    
    with c2:
        arquivos = st.file_uploader("Evidências (Opcional)", accept_multiple_files=True)
        
    with c3:
        modo = st.selectbox("Selecione a Missão:", [
            "Vibe Coding (Geração de Arquitetura & UX)", 
            "Auditoria Forense (Red/Blue Team)", 
            "Criação Rápida (Scripts/Lógica)"
        ])
        btn_run = st.button("🚀 INICIAR PROCESSAMENTO")

    st.divider()

    # ÁREA DE RESULTADO (Aparece apenas após processar)
    if btn_run and comando:
        with st.spinner("Decodificando intenção e orquestrando agentes..."):
            texto_extraido = omni_extractor(arquivos, GEMINI_KEY)
            engine = NexusEngine(GROQ_KEY)
            
            if "Red/Blue" in modo:
                sys_red = "Você é o Red Team. Critique e ache falhas extremas de segurança no código/ideia."
                sys_blue = "Você é o Blue Team. Defenda e corrija as falhas achadas pelo Red Team."
                sys_judge = "Sintetize a auditoria em um relatório Forense Markdown."
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    res_red = executor.submit(engine._call_groq, sys_red, comando).result()
                    res_blue = executor.submit(engine._call_groq, sys_blue, comando).result()
                    
                final = engine._call_groq(sys_judge, f"RED:\n{res_red}\n\nBLUE:\n{res_blue}")
                st.markdown(final)
                
            elif "Vibe Coding" in modo:
                sys_vibe = """Você é o Nexus Architect. Transforme a intenção do usuário em um plano técnico completo.
                Forneça: 1. Esquema de Banco de Dados. 2. Lógica de Backend (APIs). 3. Estrutura de UI/UX. 4. Regras de Segurança (RBAC)."""
                st.markdown(engine._call_groq(sys_vibe, f"Intenção: {comando}\nContexto: {texto_extraido}"))
                
            else:
                st.markdown(engine._call_groq("Atue como um programador sênior ultra-eficiente.", f"{comando}\n\n{texto_extraido}"))

if __name__ == "__main__":
    main()
