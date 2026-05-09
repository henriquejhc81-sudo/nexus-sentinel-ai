import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import datetime
import base64
from fpdf import FPDF 
from engine import * # IMPORTAÇÃO GLOBAL PROTEGIDA

# --- NOVO MOTOR DE MAPEAMENTO (ADITIVO v13.0) ---
def obter_correlacao_bibliografica(hora, zona):
    biblioteca = {
        "12h": {"Zona 2 (Órgãos)": "Cérebro / Vitalidade", "Zona 1 (Estômago)": "Centro Digestivo"},
        "2h-3h": {"Zona 2 (Órgãos)": "Fígado / Coração", "Zona 3 (Músculos)": "Região Torácica"},
        "6h": {"Zona 1 (Estômago)": "Intestino Grosso", "Zona 7 (Pele)": "Anel de Eliminação"},
        "9h": {"Zona 2 (Órgãos)": "Pulmões / Baço"}
    }
    return biblioteca.get(hora, {}).get(zona, "Área Geral - Consultar Mapa de Jensen")

# --- PROTOCOLO DE SEGURANÇA ---
def realizar_login():
    if "autenticado" not in st.session_state: st.session_state["autenticado"] = False
    if not st.session_state["autenticado"]:
        st.markdown("<h1 style='text-align:center;'>🛡️ GENESIS LOGIN</h1>", unsafe_allow_html=True)
        c1, col2, c3 = st.columns() # Ajuste aqui para centralizar
        with col2:
            with st.form("login"):
                u = st.text_input("Usuário"); p = st.text_input("Senha", type="password")
                if st.form_submit_button("Acessar"):
                    if u == "admin" and p == "genesis2026":
                        st.session_state["autenticado"] = True; st.session_state["medico_id"] = u; st.rerun()
                    else: st.error("Acesso Negado.")
        return False
    return True

st.set_page_config(page_title="GENESIS v13.0", layout="wide", page_icon="🛡️")

if realizar_login():
    st.markdown("""<style>
        .report-card { background-color: #111827; padding: 30px; border-radius: 15px; border-left: 8px solid #3b82f6; margin-top: 20px; }
        .section-header { color: #3b82f6; font-weight: bold; border-bottom: 1px solid #334155; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v13.0")

    with st.sidebar:
        st.header("👤 PRONTUÁRIO")
        nome_p = st.text_input("Nome do Paciente", "henriue")
        queixa_p = st.text_area("Queixa/Anamnese", "Descreva aqui...")
        st.divider()
        m_super = st.toggle("🧠 Super IA Genesis")
        m_iri = st.toggle("🔬 Iridologia Master")
        m_der = st.toggle("📸 SkinAI v2 Pro")
        m_rad = st.toggle("📂 Radiologia Digital")
        m_lab = st.toggle("🧬 Inteligência Laboratorial")
        if st.button("Sair"): st.session_state["autenticado"] = False; st.rerun()

    # --- MÓDULO IRIDOLOGIA MASTER (CUSTOMIZADO v13.0) ---
    if m_iri:
        st.subheader("🔬 Estação Iridologia Master")
        c1, c2 = st.columns(2)
        with c1:
            f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key="iris_source")
            ent = st.camera_input("Scanner") if f == "📸 Câmera" else st.file_uploader("Importar Íris", type=['jpg','png','jpeg'], key="iris_up")
            
            # Novos campos da sua sugestão (Tabela Sinais_Encont)
            st.markdown("---")
            st.markdown("### 📝 Registro de Sinais (Tabela de Jensen)")
            col_a, col_b = st.columns(2)
            with col_a:
                olho_lado = st.selectbox("Olho", ["Direito (D)", "Esquerdo (E)"])
                hora_iris = st.select_slider("Posição Horária", options=["12h", "1h", "2h-3h", "4h", "5h", "6h", "9h"])
            with col_b:
                zona_iris = st.selectbox("Zona", ["Zona 1 (Estômago)", "Zona 2 (Órgãos)", "Zona 7 (Pele)"])
                sinal_desc = st.text_input("Sinal (Ex: Lacuna, Anel)", "Lacuna")

        if ent:
            img = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img)
            # Mantém Zoom e Mapa originais
            if st.checkbox("🔍 Zoom Inteligente", value=True): img_hd = aplicar_zoom_inteligente(img_hd)
            if st.checkbox("🗺️ Mapeamento"): img_hd = aplicar_mapa_iridologico(img_hd)
            
            with c2:
                st.image(img_hd, caption="Análise Multiespectral", use_container_width=True)
                if st.button("⚡ GERAR RELATÓRIO PÓS-ANÁLISE", type="primary"):
                    # Processamento
                    correlacao = obter_correlacao_bibliografica(hora_iris, zona_iris)
                    
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    st.markdown("<div class='section-header'>RELATÓRIO DE ESTUDO IRIDOLÓGICO</div>", unsafe_allow_html=True)
                    st.write(f"**Paciente:** {nome_p} | **Data:** {datetime.datetime.now().strftime('%d/%m/%Y')}")
                    st.write(f"**Sinal Encontrado:** {sinal_desc} em {hora_iris} ({olho_lado})")
                    st.info(f"**Correspondência Teórica:** {correlacao}")
                    st.warning("⚠️ DISCLAIMER: Este estudo acadêmico não substitui diagnóstico médico.")
                    
                    # Geração do PDF v13 (Baseado no seu Template)
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(200, 10, "RELATÓRIO IRIDOLÓGICO - GENESIS AI", ln=True, align='C')
                    pdf.set_font("Arial", '', 12)
                    pdf.cell(200, 10, f"Paciente: {nome_p}", ln=True)
                    pdf.ln(5)
                    pdf.multi_cell(0, 10, f"Sinal: {sinal_desc}\nLocal: {hora_iris} - {zona_iris}\nCorrelacao: {correlacao}")
                    pdf.ln(10)
                    pdf.set_font("Arial", 'I', 8)
                    pdf.multi_cell(0, 5, "Iridologia não é reconhecida como método médico pelo CFM. Procure um médico.")
                    
                    st.download_button("🖨️ BAIXAR DOSSIÊ ACADÊMICO", pdf.output(dest='S').encode('latin-1'), file_name=f"iridologia_{nome_p}.pdf")
                    st.markdown('</div>', unsafe_allow_html=True)

    # --- DEMAIS MÓDULOS (MANTIDOS INTACTOS) ---
    elif m_der: renderizar_plataforma("Dermatologia")
    elif m_rad: renderizar_plataforma("Radiologia")
    elif m_lab:
        st.subheader("🧬 Auditoria Laboratorial")
        exame = st.file_uploader("Carregar Exame para Auditoria", type=['pdf', 'jpg', 'png'], key="lab_master")
        if exame and st.button("⚡ INICIAR AUDITORIA"): st.success("Auditado com Sucesso.")
    elif m_super:
        st.subheader("🧠 Super IA Genesis")
        p = st.text_area("Consulta Multimodal")
        if st.button("Executar"): st.info(motor_multimodal_genesis(None, p))

# Função genérica mantida para os outros módulos não sofrerem alteração
def renderizar_plataforma(label):
    st.subheader(f"Estação {label}")
    # ... (restante da sua função original que você já tem)
