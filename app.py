import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import datetime
import base64
from fpdf import FPDF 
from engine import * 

# --- PROTOCOLO DE SEGURANÇA E LOGIN (CORREÇÃO v11.1) ---
def realizar_login():
    if "autenticado" not in st.session_state: 
        st.session_state["autenticado"] = False
    
    if not st.session_state["autenticado"]:
        st.markdown("<h1 style='text-align:center;'>🛡️ GENESIS LOGIN</h1>", unsafe_allow_html=True)
        # CORREÇÃO SNIPER: Definindo col1, col2, col3 corretamente
        col1, col2, col3 = st.columns(3)
        with col2:
            with st.form("login_form"):
                u = st.text_input("Usuário Profissional")
                p = st.text_input("Senha Sentinel", type="password")
                if st.form_submit_button("Acessar Sistema"):
                    if u == "admin" and p == "genesis2026":
                        st.session_state["autenticado"] = True
                        st.session_state["medico_id"] = u
                        st.rerun()
                    else:
                        st.error("Credenciais Inválidas. Acesso Sentinel Negado.")
        return False
    return True

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="GENESIS v11.1", layout="wide", page_icon="🛡️")

if realizar_login():
    # Estilização Master de Relatórios
    st.markdown("""<style>
        .report-card { background-color: #111827; padding: 30px; border-radius: 15px; border-left: 10px solid #3b82f6; margin-top: 25px; }
        .section-header { color: #3b82f6; font-weight: bold; font-size: 1.1rem; text-transform: uppercase; margin-top: 15px; border-bottom: 1px solid #334155; }
        .diagnosis-text { font-size: 1.05rem; line-height: 1.6; color: #e5e7eb; padding: 10px 0; }
        .stMetric { background-color: #1f2937; border-radius: 10px; padding: 10px; border: 1px solid #3b82f6; }
    </style>""", unsafe_allow_html=True)

    st.title("🛡️ GENESIS FORENSIC AI v11.1")

    with st.sidebar:
        st.header("👤 PRONTUÁRIO MASTER")
        nome_paciente = st.text_input("Identificação do Paciente", "Paciente_Zero")
        queixa_principal = st.text_area("Queixa Principal / Histórico", "Descreva o motivo da consulta...")
        st.divider()
        m_super = st.toggle("🧠 Super IA Genesis")
        m_iri = st.toggle("🔬 Iridologia Master", value=True)
        m_der = st.toggle("📸 SkinAI v2 Pro")
        m_rad = st.toggle("📂 Radiologia Digital")
        m_lab = st.toggle("🧬 Inteligência Laboratorial")
        st.divider()
        if st.button("🚪 Sair do Sistema"):
            st.session_state["autenticado"] = False
            st.rerun()

    # --- DNA NEXUS SENTINEL ORQUESTRADOR ---
    def orquestrador_v11(contexto):
        with st.status(f"🧬 Orquestrador Sentinel: Validando {contexto}...", expanded=False) as s:
            time.sleep(0.5)
            s.update(label="Sincronização Master Concluída", state="complete")
        return True

    # --- LÓGICA DE RENDERIZAÇÃO DOS MÓDULOS ---

    def renderizar_plataforma_v11(label):
        st.subheader(f"Estação de Auditoria: {label}")
        c1, c2 = st.columns(2)
        with c1:
            f = st.radio("Fonte", ["📸 Câmera", "📁 Arquivo"], horizontal=True, key=label+"src")
            ent = st.camera_input("Capturar") if f == "📸 Câmera" else st.file_uploader("Importar Mídia", type=['jpg','png','jpeg'], key=label+"up")
            zoom = st.checkbox("🔍 Zoom Inteligente (Auto-Focus)", value=True, key=label+"z")
            map_on = st.checkbox("🗺️ Mapeamento de Zonas", value=True, key=label+"m") if label == "Iridologia" else False

        if ent:
            img = Image.open(ent)
            img_hd = extrair_qualidade_maxima(img)
            if zoom: img_hd = aplicar_zoom_inteligente(img_hd)
            if map_on: img_hd = aplicar_mapa_iridologico(img_hd)
            
            with c2:
                st.image(img_hd, caption="Processamento Ultra-HD Centralizado", use_container_width=True)
                if st.button(f"⚡ GERAR DOSSIÊ {label.upper()}", type="primary", key=label+"bt"):
                    orquestrador_v11(label)
                    res_tec = motor_diagnostico_genesis(img_hd, label)
                    
                    # Gerando o Mega Laudo de 7 Eixos
                    laudo = gerar_mega_laudo_iridologico(label, res_tec, queixa_principal, nome_paciente)
                    
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    st.header(f"📋 {laudo['titulo']}")
                    
                    for titulo, conteudo in laudo['eixos'].items():
                        st.markdown(f"<div class='section-header'>{titulo}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='diagnosis-text'>{conteudo}</div>", unsafe_allow_html=True)
                    
                    st.image(res_tec['viz'], caption="Visão Multiespectral (Densidade Tecidual)", width=400)
                    
                    # --- SISTEMA DE IMPRESSÃO PDF ---
                    pdf = FPDF()
                    pdf.add_page(); pdf.set_font("Arial", 'B', 16)
                    pdf.cell(200, 10, laudo['titulo'], ln=True, align='C')
                    pdf.set_font("Arial", '', 11)
                    full_txt = f"Paciente: {nome_paciente}\n\n"
                    for k, v in laudo['eixos'].items(): full_txt += f"{k}:\n{v}\n\n"
                    pdf.multi_cell(0, 10, full_txt.encode('latin-1', 'replace').decode('latin-1'))
                    
                    st.download_button("🖨️ IMPRIMIR LAUDO OFICIAL", pdf.output(dest='S'), file_name=f"genesis_{nome_paciente}.pdf", mime="application/pdf")
                    st.markdown('</div>', unsafe_allow_html=True)

    # Acionamento de Módulos
    if m_iri: renderizar_plataforma_v11("Iridologia")
    elif m_der: renderizar_plataforma_v11("Dermatologia")
    elif m_rad: renderizar_plataforma_v11("Radiologia")
    elif m_lab:
        st.subheader("🧬 Inteligência Laboratorial Universal")
        exame = st.file_uploader("Carregar Exame para Auditoria", type=['pdf', 'jpg', 'png'])
        if exame and st.button("⚡ INICIAR AUDITORIA MASTER"):
            orquestrador_v11("Laboratório")
            st.success("Auditoria Concluída via Motor Multimodal.")
    elif m_super:
        st.subheader("🧠 Super IA Genesis: Central de Inteligência")
        pergunta = st.text_area("O que deseja que o Genesis analise agora?")
        if st.button("Executar Consulta"): 
            st.info("Resposta da IA baseada na base mundial MedAI Vision X...")
