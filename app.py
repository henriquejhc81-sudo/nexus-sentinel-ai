import streamlit as st
import cv2
import numpy as np
from PIL import Image
import datetime
from fpdf import FPDF 
from engine import * 

# --- FUNÇÃO OCULTA: CÁLCULO IMC PARA O RELATÓRIO ---
def processar_biometria_relatorio(peso, altura):
    if peso > 0 and altura > 0:
        imc = peso / (altura ** 2)
        status = "Normal" if imc < 25 else "Observação Necessária"
        return f"{imc:.2f} ({status})"
    return "Dados não fornecidos"

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="IRIDOLOGIA E IRIDIAGNOSE", layout="wide", page_icon="🔬")

# CSS para alinhar com a identidade visual da imagem
st.markdown("""<style>
    .main-title { color: #A51C30; font-family: 'Arial', sans-serif; font-size: 32px; font-weight: bold; border-bottom: 3px solid #A51C30; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #A51C30; color: white; }
</style>""", unsafe_allow_html=True)

# --- TÍTULO PRINCIPAL (CORRIGIDO) ---
st.markdown("<div class='main-title'>IRIDOLOGIA E IRIDIAGNOSE</div>", unsafe_allow_html=True)
st.write(f"**Sessão Forense:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")

# --- BIOMETRIA SIMPLIFICADA (FRENTE DO SISTEMA) ---
with st.expander("👤 DADOS DO PACIENTE", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    with c1: nome_p = st.text_input("Nome Completo", "Henrique")
    with c2: idade_p = st.number_input("Idade", value=30)
    with c3: peso_p = st.number_input("Peso (kg)", format="%.2f")
    with c4: altura_p = st.number_input("Altura (m)", format="%.2f")
    queixa_p = st.text_area("Notas de Anamnese", placeholder="Descreva os sinais observados ou queixas...")

# --- SIDEBAR (CONTROLE DE MÓDULOS MANTIDO) ---
with st.sidebar:
    st.header("⚙️ ORQUESTRADOR")
    m_super = st.toggle("🧠 Super IA Genesis", value=True)
    m_iri = st.toggle("🔬 Iridologia Master", value=True)
    m_der = st.toggle("📸 SkinAI v2 Pro")
    m_rad = st.toggle("📂 Radiologia Digital")
    m_lab = st.toggle("🧬 Inteligência Laboratorial")
    st.divider()
    st.info("Sistema operando em Modo Full Analysis")

# --- MÓDULO IRIDOLOGIA MASTER (FOCO DA IMAGEM) ---
if m_iri:
    st.markdown("### 🔬 Estação Iridologia Master v13.5")
    c1, c2 = st.columns([1, 1.3])
    
    with c1:
        f = st.radio("Entrada Multimodal", ["📸 Câmera", "📁 Arquivo/Vídeo"], horizontal=True)
        ent = st.camera_input("Capturar") if f == "📸 Câmera" else st.file_uploader("Importar Mídia (Imagem/Vídeo)", type=['jpg','png','jpeg','mp4','mov'])
        
        # Mapeamento interativo para o diagnóstico de Harvard
        st.markdown("---")
        st.markdown("#### 🎯 Localização do Sinal")
        col_x, col_y = st.columns(2)
        with col_x:
            hora_sel = st.select_slider("Relógio de Jensen", options=["12h", "1h", "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "11h"])
            olho_sel = st.radio("Lado", ["Direito", "Esquerdo"], horizontal=True)
        with col_y:
            zona_sel = st.selectbox("Zona Alvo", ["Zona 1 (Digestiva)", "Zona 2 (Orgânica)", "Zona 7 (Dérmica)"])
            tipo_sinal = st.text_input("Tipo de Sinal", "Lacuna")

    if ent:
        with c2:
            # Processamento de Imagem HD (Lógica da Engine original)
            if hasattr(ent, 'type') and 'video' in ent.type:
                st.video(ent)
                img_display = None
            else:
                img_display = Image.open(ent)
                img_hd = extrair_qualidade_maxima(img_display)
                if st.checkbox("🔍 Aplicar Zoom Inteligente", value=True): img_hd = aplicar_zoom_inteligente(img_hd)
                if st.checkbox("🗺️ Overlay de Jensen"): img_hd = aplicar_mapa_iridologico(img_hd)
                st.image(img_hd, caption="Processamento Multiespectral Sentinel", use_container_width=True)

            # --- GERAÇÃO DE RELATÓRIO HARVARD / IRISDIAGNOSE ---
            if st.button("⚡ GERAR DIAGNÓSTICO IRISDIAGNOSE - HARVARD STYLE"):
                imc_calc = processar_biometria_relatorio(peso_p, altura_p)
                correlacao_txt = obter_correlacao_bibliografica(hora_sel, zona_sel)
                
                pdf = FPDF()
                pdf.add_page()
                # Cabeçalho Estilo Harvard
                pdf.set_fill_color(165, 28, 48)
                pdf.rect(0, 0, 210, 35, 'F')
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", 'B', 20)
                pdf.cell(0, 15, "IRISDIAGNOSE CLINICAL REPORT", ln=True, align='C')
                
                pdf.set_text_color(0, 0, 0)
                pdf.ln(25)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"ESTUDO DE CASO: {nome_p.upper()}", ln=True)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 7, f"Idade: {idade_p} anos | Biometria (IMC): {imc_calc}\nQueixa: {queixa_p}")
                
                pdf.ln(10)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, "ANÁLISE DE TERRENO BIOLÓGICO", ln=True)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 7, f"Sinal Identificado: {tipo_sinal} no olho {olho_sel} (Posição {hora_sel}).\n"
                                     f"Correspondência Técnica: {correlacao_txt}.\n"
                                     f"Diagnóstico Irisdiagnose: O padrão observado sugere reatividade na {zona_sel}, "
                                     "demandando acompanhamento preventivo e suporte nutricional específico.")
                
                pdf.ln(20)
                pdf.set_font("Arial", 'I', 8)
                pdf.multi_cell(0, 5, "Harvard Case Method Style - Genesis Forensic AI v13.5\n"
                                     "Este documento possui fins acadêmicos e informativos. Não substitui consulta médica.")
                
                st.download_button("🖨️ BAIXAR RELATÓRIO COMPLETO", pdf.output(dest='S').encode('latin-1'), file_name=f"Irisdiagnose_{nome_p}.pdf")

# --- MANTENDO OS DEMAIS MÓDULOS EM OPERAÇÃO SILENCIOSA ---
elif m_der: renderizar_plataforma("Dermatologia")
elif m_rad: renderizar_plataforma("Radiologia")
elif m_lab: renderizar_plataforma("Laboratorial")
elif m_super: st.info("Super IA Genesis ativa para suporte diagnóstico.")
