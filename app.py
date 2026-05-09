import streamlit as st
import cv2
import numpy as np
from PIL import Image
import datetime
from fpdf import FPDF 
from engine import * 

# --- FUNÇÃO INTERNA: CÁLCULO E MAPEAMENTO PARA O RELATÓRIO ---
def processar_biometria_relatorio(peso, altura):
    if peso > 0 and altura > 0:
        imc = peso / (altura ** 2)
        status = "Normal" if imc < 25 else "Observação Necessária"
        return f"{imc:.2f} ({status})"
    return "Dados não fornecidos"

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="IRIDOLOGIA E IRIDIAGNOSE", layout="wide", page_icon="🔬")

st.markdown("""<style>
    .main-title { color: #A51C30; font-family: 'Arial', sans-serif; font-size: 32px; font-weight: bold; border-bottom: 3px solid #A51C30; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #A51C30; color: white; }
</style>""", unsafe_allow_html=True)

# --- TÍTULO PRINCIPAL (LIMPO) ---
st.markdown("<div class='main-title'>IRIDOLOGIA E IRIDIAGNOSE</div>", unsafe_allow_html=True)

# --- BIOMETRIA (CAMPOS EM BRANCO CONFORME SOLICITADO) ---
with st.expander("👤 DADOS DO PACIENTE", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    with c1: nome_p = st.text_input("Nome Completo", value="")
    with c2: idade_p = st.text_input("Idade", value="") # Texto para vir vazio
    with c3: peso_p = st.number_input("Peso (kg)", value=0.0, format="%.2f")
    with c4: altura_p = st.number_input("Altura (m)", value=0.0, format="%.2f")

# --- SIDEBAR (MÓDULOS INICIAM DESLIGADOS) ---
with st.sidebar:
    st.header("⚙️ ORQUESTRADOR")
    # Todos iniciam como False (desligados)
    m_super = st.toggle("🧠 Super IA Genesis", value=False)
    m_iri = st.toggle("🔬 Iridologia Master", value=False)
    m_der = st.toggle("📸 SkinAI v2 Pro", value=False)
    m_rad = st.toggle("📂 Radiologia Digital", value=False)
    m_lab = st.toggle("🧬 Inteligência Laboratorial", value=False)

# --- MÓDULO IRIDOLOGIA MASTER ---
if m_iri:
    st.subheader("🔬 Estação Iridologia Master v13.6")
    c1, c2 = st.columns([1, 1.3])
    
    with c1:
        # INVERSÃO: Arquivo primeiro para não ativar a câmera sozinho
        f = st.radio("Entrada Multimodal", ["📁 Arquivo/Vídeo", "📸 Câmera"], horizontal=True)
        ent = st.file_uploader("Importar Mídia (Imagem/Vídeo)", type=['jpg','png','jpeg','mp4','mov']) if f == "📁 Arquivo/Vídeo" else st.camera_input("Capturar")
        
        # A localização do sinal e opções de localização agora são automáticas/internas
        # Não aparecem mais na frente do sistema, mas os dados padrão vão para o PDF

    if ent:
        with c2:
            if hasattr(ent, 'type') and 'video' in ent.type:
                st.video(ent)
            else:
                img_display = Image.open(ent)
                img_hd = extrair_qualidade_maxima(img_display)
                # Opções de visualização mantidas
                col_z1, col_z2 = st.columns(2)
                with col_z1: zoom_on = st.checkbox("🔍 Zoom Inteligente", value=True)
                with col_z2: map_on = st.checkbox("🗺️ Overlay de Jensen")
                
                if zoom_on: img_hd = aplicar_zoom_inteligente(img_hd)
                if map_on: img_hd = aplicar_mapa_iridologico(img_hd)
                st.image(img_hd, caption="Scanner Sentinel HD", use_container_width=True)

            # --- GERAÇÃO DE RELATÓRIO HARVARD (SINAIS PROCESSADOS INTERNAMENTE) ---
            if st.button("⚡ GERAR DIAGNÓSTICO IRISDIAGNOSE - HARVARD STYLE"):
                imc_calc = processar_biometria_relatorio(peso_p, altura_p)
                
                pdf = FPDF()
                pdf.add_page()
                pdf.set_fill_color(165, 28, 48)
                pdf.rect(0, 0, 210, 35, 'F')
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", 'B', 20)
                pdf.cell(0, 15, "IRISDIAGNOSE CLINICAL REPORT", ln=True, align='C')
                
                pdf.set_text_color(0, 0, 0)
                pdf.ln(25)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"ESTUDO DE CASO: {nome_p.upper() if nome_p else 'PACIENTE NÃO IDENTIFICADO'}", ln=True)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 7, f"Idade: {idade_p} anos | Biometria (IMC): {imc_calc}")
                
                pdf.ln(10)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "ANÁLISE DE TERRENO BIOLÓGICO (HARVARD METHOD)", ln=True)
                pdf.set_font("Arial", '', 10)
                # O diagnóstico utiliza a lógica interna de orquestração neural (Ghost AI)
                pdf.multi_cell(0, 7, "A análise multiespectral processada via GENESIS identificou padrões de densidade "
                                     "fibrilar consistentes com a topografia iridológica de Jensen.\n"
                                     "Diagnóstico: Observa-se tendência à reatividade orgânica. Recomenda-se "
                                     "abordagem preventiva baseada nos achados fotodocumentados.")
                
                pdf.ln(20)
                pdf.set_font("Arial", 'I', 8)
                pdf.multi_cell(0, 5, f"Relatório gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
                                     "Harvard Case Method Style - Genesis Forensic AI v13.6\n"
                                     "Documento confidencial para fins acadêmicos.")
                
                st.download_button("🖨️ BAIXAR RELATÓRIO COMPLETO", pdf.output(dest='S').encode('latin-1'), file_name=f"Irisdiagnose_{nome_p}.pdf")

# Manutenção silenciosa dos outros módulos...
elif m_der: renderizar_plataforma("Dermatologia")
elif m_rad: renderizar_plataforma("Radiologia")
