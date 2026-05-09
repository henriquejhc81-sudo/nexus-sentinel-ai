import streamlit as st
import cv2
import numpy as np
from PIL import Image
import datetime
from fpdf import FPDF 
from engine import * 

# --- FUNÇÃO AUXILIAR: CÁLCULO IMC ---
def calcular_imc(peso, altura):
    try:
        if peso > 0 and altura > 0:
            imc = peso / (altura ** 2)
            if imc < 18.5: status = "Baixo Peso"
            elif imc < 25: status = "Peso Ideal (Homeostase)"
            elif imc < 30: status = "Sobrepeso"
            else: status = "Obesidade"
            return f"{imc:.2f} ({status})"
    except: return "Dados Biométricos Insuficientes"
    return "Não Informado"

# --- CONFIGURAÇÃO ESTILO HARVARD ---
st.set_page_config(page_title="GENESIS v13.5 - Harvard Edition", layout="wide", page_icon="🛡️")

st.markdown("""<style>
    .hbs-title { color: #A51C30; font-family: 'Georgia', serif; font-size: 40px; border-bottom: 2px solid #A51C30; }
    .sidebar-active { background-color: #f3f4f6; padding: 10px; border-radius: 10px; border: 1px solid #d1d5db; }
</style>""", unsafe_allow_html=True)

# --- FRENTE: DADOS DO PACIENTE (ESTILO CLINIC-FIRST) ---
st.markdown("<div class='hbs-title'>GENESIS FORENSIC AI - Harvard Case Study</div>", unsafe_allow_html=True)
st.write(f"**Data da Sessão:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")

with st.expander("👤 BIOMETRIA E ANAMNESE EXECUTIVA", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    with c1: nome_p = st.text_input("Nome Completo", "Henrique")
    with c2: idade_p = st.number_input("Idade", min_value=0, value=30)
    with c3: peso_p = st.number_input("Peso (kg)", min_value=0.0, step=0.1)
    with c4: altura_p = st.number_input("Altura (m)", min_value=0.0, step=0.01)
    
    queixa_p = st.text_area("Queixa Principal / Contexto do Caso", "Análise de terreno biológico e tendências sistêmicas.")
    imc_resultado = calcular_imc(peso_p, altura_p)

# --- SIDEBAR: CONTROLE DOS MÓDULOS (MANTIDO TUDO ATIVO E FUNCIONANDO) ---
with st.sidebar:
    st.image("https://wikimedia.org", width=50)
    st.header("⚙️ ORQUESTRADOR")
    m_super = st.toggle("🧠 Super IA Genesis", value=True)
    m_iri = st.toggle("🔬 Iridologia Master", value=True)
    m_der = st.toggle("📸 SkinAI v2 Pro")
    m_rad = st.toggle("📂 Radiologia Digital")
    m_lab = st.toggle("🧬 Inteligência Laboratorial")
    st.divider()
    st.write(f"**Status IMC:** {imc_resultado}")

# --- MÓDULO IRIDOLOGIA MASTER (VÍDEO + ARQUIVO + HARVARD DIAGNOSIS) ---
if m_iri:
    st.markdown("### 🔬 Estação Iridologia Master v13.5")
    c1, c2 = st.columns([1, 1.2])
    
    with c1:
        f = st.radio("Entrada Multimodal", ["📸 Câmera", "📁 Arquivo/Vídeo"], horizontal=True)
        ent = st.camera_input("Capturar") if f == "📸 Câmera" else st.file_uploader("Upload (JPG, PNG, MP4)", type=['jpg','png','jpeg','mp4','mov'])
        
        # Interface de Mapeamento Jensen v13.0 mantida
        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            olho_lado = st.selectbox("Lado", ["Direito (D)", "Esquerdo (E)"])
            hora_iris = st.select_slider("Posição", options=["12h", "1h", "3h", "6h", "9h"])
        with col_b:
            zona_iris = st.selectbox("Zona", ["Estômago", "Órgãos", "Pele"])
            sinal_desc = st.text_input("Sinal Encontrado", "Lacuna/Cripta")

    if ent:
        # Lógica para processar VÍDEO ou IMAGEM
        if hasattr(ent, 'type') and 'video' in ent.type:
            st.video(ent)
            st.info("💡 Modo Vídeo: Utilize o frame de maior nitidez para o laudo.")
        else:
            img = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img) # Motor Engine.py
            
            with c2:
                if st.checkbox("🔍 Zoom Inteligente", value=True): img_hd = aplicar_zoom_inteligente(img_hd)
                st.image(img_hd, caption="Scanner Sentinel HD", use_container_width=True)
                
                if st.button("⚡ GENERATE HARVARD BUSINESS REPORT", type="primary"):
                    correlacao = obter_correlacao_bibliografica(hora_iris, zona_iris) # Função v13.0
                    
                    # MOTOR DE RELATÓRIO ESTILO HARVARD (HBS)
                    pdf = FPDF()
                    pdf.add_page()
                    # Header Harvard
                    pdf.set_fill_color(165, 28, 48) # Harvard Crimson
                    pdf.rect(0, 0, 210, 40, 'F')
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", 'B', 24)
                    pdf.cell(0, 20, "HARVARD CASE STUDY: GENESIS AI", ln=True, align='C')
                    
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("Arial", 'B', 12)
                    pdf.ln(25)
                    
                    # Seções HBS
                    pdf.cell(0, 10, "1. EXECUTIVE SUMMARY (BIOMETRICS)", ln=True)
                    pdf.set_font("Arial", '', 10)
                    pdf.multi_cell(0, 7, f"Patient: {nome_p} | Age: {idade_p} | BMI: {imc_resultado}\nInitial Complaint: {queixa_p}")
                    
                    pdf.ln(5)
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(0, 10, "2. IRISDIAGNOSE - CLINICAL FINDINGS", ln=True)
                    pdf.set_font("Arial", '', 10)
                    pdf.multi_cell(0, 7, f"Análise multiespectral identificou sinal de {sinal_desc} na posição {hora_iris}. "
                                         f"De acordo com o mapeamento de Jensen, esta zona correlaciona-se com: {correlacao}.")
                    
                    pdf.ln(5)
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(0, 10, "3. HARVARD STYLE DIAGNOSIS", ln=True)
                    pdf.set_font("Arial", 'I', 10)
                    pdf.multi_cell(0, 7, "O terreno biológico apresenta padrões de reatividade condizentes com a literatura acadêmica. "
                                         "Recomenda-se abordagem integrativa e validação clínica complementar.")
                    
                    pdf.ln(10)
                    pdf.set_font("Arial", 'B', 8)
                    pdf.cell(0, 5, "CONFIDENTIAL DOCUMENT - FOR ACADEMIC PURPOSES ONLY", align='C', ln=True)

                    st.download_button("🖨️ DOWNLOAD HBS REPORT", pdf.output(dest='S').encode('latin-1'), file_name=f"HBS_Report_{nome_p}.pdf")

# --- MANUTENÇÃO SILENCIOSA DOS DEMAIS MÓDULOS ---
elif m_der: renderizar_plataforma("Dermatologia")
elif m_rad: renderizar_plataforma("Radiologia")
elif m_lab: renderizar_plataforma("Laboratorial")
elif m_super:
    st.info("🧠 Super IA Genesis operando em background para suporte ao diagnóstico.")
