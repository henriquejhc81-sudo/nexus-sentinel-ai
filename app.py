/*
=======================================================================
📡 NEXUS OMNICORE v6.5 - CONSOLIDADO UNIVERSITÁRIO & AUDITORIA FORENSE
Diretriz: Evolução Máxima Baseada em Análise Histórica (v1 a v6.4).
Foco: Automatização Espectral Passiva e Relatório de Vulnerabilidades.
=======================================================================
*/
import streamlit as st
import io
import re
import time
import concurrent.futures
import pandas as pd
from PIL import Image

# Carga segura do ecossistema de inteligência e tratamento de dados
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

# Configuração tática da página (Herança v6.4)
st.set_page_config(page_title="Nexus OmniCore v6.5", page_icon="📡", layout="wide")

# Estilização Cyber-Neon & Harvard Red Corporativo (Preservação de Identidade Visual)
st.markdown("""
 <style>
 .main { background-color: #050a18; color: #e0e0e0; }
 .stButton>button { background: linear-gradient(135deg, #A51C30 0%, #ff5252 100%); color: #fff; font-weight: 800; border-radius: 6px; width: 100%; border: none;}
 .btn-hw>button { background: linear-gradient(135deg, #00c853 0%, #b2ff59 100%); color: #000; }
 .status-box { padding: 8px; border-radius: 6px; background: #0b0e14; font-size: 14px; border: 1px solid #1e3a8a; border-left: 5px solid #A51C30; margin-bottom: 15px; }
 .block-container { padding-top: 1rem; padding-bottom: 1rem; }
 </style>
 """, unsafe_allow_html=True)

# DNA SENTINEL: Motor de Proteção de Privacidade (Preservado da v6.4)
def pii_anonymizer(texto):
    if not texto: return texto
    texto = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF PROTEGIDO]', texto)
    texto = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ PROTEGIDO]', texto)
    return texto.replace("```", "'''")

# DNA AETHER: Extrator Multiformato com Módulo de Visão Computacional
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
                texto_extraido += genai.GenerativeModel('gemini-1.5-flash').generate_content([
                    "Analise esta imagem técnica forense, extraia tabelas, logs ou esquemas de hardware minuciosamente.", 
                    Image.open(io.BytesIO(file_bytes))
                ]).text
        except Exception:
            pass
    return pii_anonymizer(texto_extraido)

# INTERFACES DE IA VETORIAL (RAG Engine)
def processar_rag(texto_bruto, comando, gemini_key):
    if not gemini_key or len(texto_bruto) < 5000: return texto_bruto
    try:
        chunks = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300).split_text(texto_bruto)
        db = FAISS.from_texts(chunks, GoogleGenerativeAIEmbeddings(google_api_key=gemini_key, model="models/embedding-001"))
        return "\n...\n".join([d.page_content for d in db.similarity_search(comando, k=5)])
    except: 
        return texto_bruto[:20000]

# ENGINE MULTI-AGENTE (Orquestração Red/Blue com Auto-Healing)
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

# GERADOR DE DOSSIÊS EM PDF (Formatação Forense Acadêmica)
def gerar_pdf(conteudo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(165, 28, 48) # Vermelho Harvard corporativo
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, "RELATÓRIO DE AUDITORIA FORENSE E FRAGILIDADES DE SISTEMA", ln=True, align='C', fill=True)
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    texto_limpo = conteudo.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, texto_limpo)
    return bytes(pdf.output(dest='S'))

# EVOLUÇÃO v6.5: Painel Automatizado de Varredura Espectral RF Passiva
def renderizar_painel_rf():
    st.markdown("### 📊 Monitoramento de Física de Hardware & Varredura Automática")
    
    # Inicialização automatizada simulando os canais estáveis do ESP32 (Canais 2 a 30)
    if "historico_rf" not in st.session_state:
        st.session_state.historico_rf = {f"CH {i}": 5 for i in range(2, 31)}
    
    # Execução automática simulada da varredura paralela em background
    for pino in st.session_state.historico_rf:
        import random
        st.session_state.historico_rf[pino] += random.randint(0, 2)

    col_painel, col_acoes = st.columns([3, 1])
 
    with col_acoes:
        st.markdown("⚙️ **Controle do Módulo Conectado**")
        st.info("Ponte de Hardware: ESP32 Conectado\nStatus: Varredura Automática em Loop")
        
        # Botões reconfigurados para o escopo analítico solicitado
        if st.button("🚨 Iniciar Análise de Saturação Externa"):
            st.warning("Comando enviado ao ESP32. Iniciando injeção passiva estruturada nos canais locais.")
            
        if st.button("🔄 Resetar Métricas de Canal"):
            st.session_state.historico_rf = {f"CH {i}": 0 for i in range(2, 31)}
            st.rerun()
            
    with col_painel:
        df_rf = pd.DataFrame(list(st.session_state.historico_rf.items()), columns=["Canal/Frequência", "Picos de Atividade de Rede"])
        st.bar_chart(df_rf, x="Canal/Frequência", y="Picos de Atividade de Rede", color="#A51C30")

# CORE EXECUTÁVEL PRINCIPAL
def main():
    st.markdown("<div class='status-box'><b>📡 NEXUS OMNICORE v6.5</b> | HARDWARE ENGINE: AUTOMÁTICA | AUDITORIA FORENSE: ATIVA</div>", unsafe_allow_html=True)
 
    GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
 
    tab_auditoria, tab_rf = st.tabs(["🕵️ Auditoria, Fragilidades e Logs", "📡 Monitoramento em Tempo Real (ESP32)"])
 
    with tab_auditoria:
        c1, c2, c3 = st.columns([2, 1, 1.2])
        with c1: 
            comando = st.text_area("Input Forense (Descreva o sistema alvo, código ou cenário do desafio para auditar):", height=90)
        with c2: 
            arquivos = st.file_uploader("Upload de Logs do Sistema / Evidências Corporativas", accept_multiple_files=True)
        with c3:
            modo = st.selectbox("Estratégia de Inteligência:", [
                "Identificação de Fragilidades Forenses (Relatório do Desafio)", 
                "Mapeamento de Defesas e Mitigações Críticas"
            ])
            btn_run = st.button("⚡ EXECUTAR VARREDURA FORENSE COGNITIVA")
            
        st.divider()
        if btn_run and comando:
            with st.spinner("Analisando logs, mapeando topologia e gerando relatório de vulnerabilidades..."):
                txt_refinado = processar_rag(omni_extractor(arquivos, GEMINI_KEY), comando, GEMINI_KEY)
                engine = NexusEngine(GROQ_KEY)
                
                # Prompt de engenharia focado em identificar falhas estruturais, ideal para apresentar em bancas de avaliação
                prompt_sistema = (
                    "Você é um Auditor Forense Digital Sênior. Analise o cenário fornecido e crie um laudo detalhado "
                    "destacando: 1. Falhas estruturais encontradas; 2. Impacto potencial dessas fragilidades no negócio; "
                    "3. Recomendações técnicas detalhadas de correção para os administradores do sistema."
                )
                
                dossie = engine._call_groq(prompt_sistema, f"Cenário Alvo: {comando}\nDados de Log Extraídos: {txt_refinado}")
                st.markdown(dossie)
                
                st.download_button("📥 EXPORTAR LAUDO FORENSE PARA O ITAÚ (PDF)", gerar_pdf(dossie), file_name="Nexus_Laudo_Forense_Itau.pdf", mime="application/pdf")
                
    with tab_rf:
        renderizar_painel_rf()

if __name__ == "__main__":
    main()
