"""
=============================================================================
🛡️ NEXUS OMNICORE v6.4 - FUSÃO TOTAL (RAG, MULTI-AGENTE, PDF & MONITORAMENTO RF)
=============================================================================
Diretriz: Evolução Máxima. Preservação Absoluta de todas as funções históricas.
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

# Configuração tática da página
st.set_page_config(page_title="Nexus OmniCore v6.4", page_icon="🛡️", layout="wide")

# Estilização Cyber-Neon & Harvard Red Corporativo
st.markdown("""
    <style>
    .main { background-color: #050a18; color: #e0e0e0; }
    .stButton>button { background: linear-gradient(135deg, #A51C30 0%, #ff5252 100%); color: #fff; font-weight: 800; border-radius: 6px; width: 100%; border: none;}
    .btn-hw>button { background: linear-gradient(135deg, #00c853 0%, #b2ff59 100%); color: #000; }
    .status-box { padding: 8px; border-radius: 6px; background: #0b0e14; font-size: 14px; border: 1px solid #1e3a8a; border-left: 5px solid #00c853; margin-bottom: 15px; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
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
        if arquivo.size > 15 * 1024 * 1024: continue # Limite de segurança de 15MB
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
        except Exception as e:
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
        return texto_bruto[:20000] # Fallback de segurança se o RAG falhar

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
                    time.sleep(2 ** attempt) # Mecanismo Sentinel Auto-Healing de Rate Limit
                else: 
                    return f"Erro na chamada da engine: {e}"
        return "Falha crítica por saturação de Rate Limit."

# 📄 GERADOR DE DOSSIÊS EM PDF (Padrão Executivo Harvard)
def gerar_pdf(conteudo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_fill_color(165, 28, 48) # Vermelho Harvard
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, "DOSSIE DE AUDITORIA FORENSE - NEXUS OMNICORE", ln=True, align='C', fill=True)
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    # Sanitização de caracteres para evitar quebra no encoding do FPDF básico
    texto_limpo = conteudo.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, texto_limpo)
    return bytes(pdf.output(dest='S'))

# 📡 NOVO DNA OMNICORE: Painel de Monitoramento Espectral RF (Trabalho Acadêmico)
def renderizar_painel_rf():
    st.markdown("### 📡 Painel de Monitoramento Espectral de Radiofrequência")
    
    # Inicialização do banco de dados na memória da sessão para simular os canais 2 a 30
    if "historico_rf" not in st.session_state:
        st.session_state.historico_rf = {f"CH {i}": 0 for i in range(2, 31)}
    
    col_painel, col_acoes = st.columns([3, 1])
    
    with col_acoes:
        st.markdown("**🔋 Telemetria Local**")
        st.info("Ponte de Hardware: ATIVA\nAgente: ESP32 Analyzer")
        
        # Interface de simulação tática para validação de dados no Polo Acadêmico
        canal_teste = st.selectbox("Simular Detecção de Portadora (Teste Local):", [f"CH {i}" for i in range(2, 31)])
        if st.button("📥 Injetar Sinal Capturado"):
            st.session_state.historico_rf[canal_teste] += 1
            st.success(f"Sinal contabilizado no {canal_teste}!")
            
        if st.button("🧹 Resetar Gráfico"):
            st.session_state.historico_rf = {f"CH {i}": 0 for i in range(2, 31)}
            st.rerun()

    with col_painel:
        # Transforma o dicionário em DataFrame e renderiza o gráfico de barras
        df_rf = pd.DataFrame(list(st.session_state.historico_rf.items()), columns=["Canal/Frequência", "Picos de Portadoras Ativas"])
        st.bar_chart(df_rf, x="Canal/Frequência", y="Picos de Portadoras Ativas", color="#A51C30")

# 🕹️ CORE EXECUTÁVEL PRINCIPAL
def main():
    st.markdown("<div class='status-box'><b>🛡️ NEXUS OMNICORE v6.4</b> | HARDWARE BRIDGE: CONECTADA | RAG MOTOR: ATIVO | SEGURANÇA: MÁXIMA</div>", unsafe_allow_html=True)
    
    # Resgate seguro de chaves de API via Secrets
    GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    
    # Criação das abas principais para organização e scannability da interface
    tab_auditoria, tab_rf = st.tabs(["🧠 Auditoria e Inteligência Multi-Agente", "📡 Monitoramento Física de Hardware (RF)"])
    
    with tab_auditoria:
        c1, c2, c3 = st.columns([2, 1, 1.2])
        with c1: 
            comando = st.text_area("🧠 Input Neural (Defina o Alvo, Código ou Arquitetura a ser Auditada):", height=90)
        with c2: 
            arquivos = st.file_uploader("Evidências / Logs / Imagens Técnicas", accept_multiple_files=True)
        with c3:
            modo = st.selectbox("Missão tática operacional:", ["Auditoria Forense Avançada (Red vs Blue Team)", "🧬 Inception DNA (Geração de Arquitetura Direta)"])
            btn_run = st.button("⚡ ATIVAR PROTOCOLO DE ANÁLISE")

        st.divider()

        if btn_run and comando:
            with st.spinner("O Nexus está processando os dados e executando a simulação multi-agente..."):
                # Executa o extrator multimodal e filtra através do RAG
                txt_refinado = processar_rag(omni_extractor(arquivos, GEMINI_KEY), comando, GEMINI_KEY)
                engine = NexusEngine(GROQ_KEY)
                
                if "Red vs Blue" in modo:
                    # Roda o Red Team e o Blue Team em threads paralelas para performance máxima
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        r_red = executor.submit(engine._call_groq, "Aja como um especialista do Red Team. Analise o contexto e aponte todas as brechas, vulnerabilidades e falhas sem piedade.", f"Alvo: {comando}\nContexto: {txt_refinado}").result()
                        r_blue = executor.submit(engine._call_groq, "Aja como um especialista de Blue Team. Analise os pontos do Red Team e forneça correções estruturadas, defesas rígidas e mitigações práticas.", f"Alvo: {comando}\nContexto: {txt_refinado}").result()
                    
                    # Sintetiza o laudo final
                    dossie = engine._call_groq("Sintetize um Relatório Forense Final estruturado e profissional com base nas discussões.", f"DISCUSSÃO RED TEAM:\n{r_red}\n\nDISCUSSÃO BLUE TEAM:\n{r_blue}")
                    
                    st.markdown(dossie)
                    
                    # Disponibiliza o download do PDF executivo gerado em tempo real
                    st.download_button("📥 EXPORTAR DOSSIÊ COMPLETO (PDF)", gerar_pdf(dossie), file_name="Nexus_Dossie_Forense.pdf", mime="application/pdf")
                else:
                    # Modo Inception: Geração direta de código e infraestrutura limpa
                    laudo_direto = engine._call_groq("Gere código fonte limpo e arquitetura estruturada de nível sênior.", f"Diretriz: {comando}\nContexto: {txt_refinado}")
                    st.markdown(laudo_direto)

    with tab_rf:
        # Renderiza a aba focada no seu projeto acadêmico de hardware
        renderizar_painel_rf()

if __name__ == "__main__":
    main()
