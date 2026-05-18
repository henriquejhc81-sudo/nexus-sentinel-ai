"""
=============================================================================
🛡️ NEXUS OMNICORE v6.3 - RAG ENGINE & PDF EXPORT
=============================================================================
Fusão Total: Multi-Agente + Extrator PDF/RAG + Gerador de Dossiê
=============================================================================
"""

import streamlit as st
import io, re, time
import concurrent.futures
from PIL import Image

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
    st.error(f"Erro de dependência. Detalhe: {e}")

st.set_page_config(page_title="Nexus OmniCore v6.3", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050a18; color: #e0e0e0; }
    .stButton>button { background: linear-gradient(135deg, #A51C30 0%, #ff5252 100%); color: #fff; font-weight: 800; border-radius: 6px; width: 100%; border: none;}
    .btn-hw>button { background: linear-gradient(135deg, #00c853 0%, #b2ff59 100%); color: #000; }
    .status-box { padding: 8px; border-radius: 6px; background: #0b0e14; font-size: 14px; border: 1px solid #1e3a8a; border-left: 5px solid #00c853; margin-bottom: 15px; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)

def pii_anonymizer(texto):
    if not texto: return texto
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF PROTEGIDO]', texto)
    texto = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ PROTEGIDO]', texto)
    return texto.replace("```", "'''")

def omni_extractor(arquivos_upados, gemini_key):
    texto_extraido = ""
    if not arquivos_upados: return texto_extraido
    for arquivo in arquivos_upados:
        if arquivo.size > 15 * 1024 * 1024: continue
        file_bytes = arquivo.getvalue()
        name = arquivo.name.lower()
        try:
            if name.endswith('.txt') or name.endswith('.csv'): texto_extraido += f"\n{file_bytes.decode('utf-8', errors='ignore')}"
            elif name.endswith('.pdf'): texto_extraido += "\n".join([p.extract_text() for p in PyPDF2.PdfReader(io.BytesIO(file_bytes)).pages if p.extract_text()])
            elif name.endswith('.docx'): texto_extraido += docx2txt.process(io.BytesIO(file_bytes))
            elif name.endswith(('.png', '.jpg')) and gemini_key:
                genai.configure(api_key=gemini_key)
                texto_extraido += genai.GenerativeModel('gemini-1.5-flash').generate_content(["Extraia texto técnico.", Image.open(io.BytesIO(file_bytes))]).text
        except: pass
    return pii_anonymizer(texto_extraido)

def processar_rag(texto_bruto, comando, gemini_key):
    if not gemini_key or len(texto_bruto) < 5000: return texto_bruto
    try:
        chunks = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300).split_text(texto_bruto)
        db = FAISS.from_texts(chunks, GoogleGenerativeAIEmbeddings(google_api_key=gemini_key, model="models/embedding-001"))
        return "\n...\n".join([d.page_content for d in db.similarity_search(comando, k=5)])
    except: return texto_bruto[:20000]

class NexusEngine:
    def __init__(self, groq_key): self.groq_key = groq_key
    def _call_groq(self, system, prompt, retries=3):
        if not self.groq_key: return "API Key ausente."
        client = Groq(api_key=self.groq_key)
        for attempt in range(retries):
            try: return client.chat.completions.create(messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}], model="llama-3.3-70b-versatile", temperature=0.2).choices[0].message.content
            except Exception as e:
                if "429" in str(e): time.sleep(2 ** attempt)
                else: return f"Erro: {e}"
        return "Falha de Rate Limit."

def gerar_pdf(conteudo):
    """Gera um PDF elegante do Dossiê para exportação."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_fill_color(165, 28, 48)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, "DOSSIE DE AUDITORIA FORENSE - NEXUS", ln=True, align='C', fill=True)
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    # Limpa caracteres não suportados pelo FPDF básico
    texto_limpo = conteudo.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, texto_limpo)
    return bytes(pdf.output(dest='S'))

def main():
    st.markdown("<div class='status-box'><b>NEXUS v6.3</b> | RAG: ON | PDF EXPORT: ON | DNA: INCEPTION</div>", unsafe_allow_html=True)
    GROQ_KEY, GEMINI_KEY = st.secrets.get("GROQ_API_KEY", ""), st.secrets.get("GEMINI_API_KEY", "")
    
    c1, c2, c3, c4 = st.columns([2, 1, 1.2, 1])
    with c1: comando = st.text_area("🧠 Input Neural (Defina o Alvo ou Arquitetura):", height=90)
    with c2: arquivos = st.file_uploader("Evidências", accept_multiple_files=True)
    with c3:
        modo = st.selectbox("Missão:", ["Auditoria Forense (Red/Blue Team)", "🧬 Inception DNA (Arquitetura)"])
        btn_run = st.button("⚡ ATIVAR PROTOCOLO")
    with c4:
        st.markdown("<div style='margin-top: 32px;'></div><span class='btn-hw'>", unsafe_allow_html=True)
        if st.button("🔌 Local Bridge (Standby)"): st.warning("Conecte o equipamento e inicie o script local em Python.")
        st.markdown("</span>", unsafe_allow_html=True)

    st.divider()

    if btn_run and comando:
        with st.spinner("Processando Inteligência..."):
            txt_refinado = processar_rag(omni_extractor(arquivos, GEMINI_KEY), comando, GEMINI_KEY)
            engine = NexusEngine(GROQ_KEY)
            
            if "Red/Blue" in modo:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    r_red = executor.submit(engine._call_groq, "Aja como Red Team. Ataque sem piedade.", f"Alvo: {comando}\nContexto: {txt_refinado}").result()
                    r_blue = executor.submit(engine._call_groq, "Aja como Blue Team. Defenda a arquitetura.", f"Alvo: {comando}\nContexto: {txt_refinado}").result()
                dossie = engine._call_groq("Sintetize um Relatório Forense Final detalhado.", f"RED:\n{r_red}\n\nBLUE:\n{r_blue}")
                
                st.markdown(dossie)
                st.download_button("📥 EXPORTAR DOSSIÊ (PDF)", gerar_pdf(dossie), file_name="Nexus_Dossie.pdf", mime="application/pdf")
            else:
                st.markdown(engine._call_groq("Gere código e arquitetura estruturada.", f"Diretriz: {comando}\nContexto: {txt_refinado}"))

if __name__ == "__main__":
    main()
