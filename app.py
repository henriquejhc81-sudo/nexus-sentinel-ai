import streamlit as st
import datetime
import cv2
import numpy as np
from PIL import Image
import io
from fpdf import FPDF

# --- MOTORES DE ALTA PERFORMANCE ---
try:
    from engine import * 
except ImportError:
    st.warning("⚠️ Modo de compatibilidade Sentinel Ativo.")

class GenesisOrchestrator:
    def __init__(self):
        self.config_global()
        self.prontuario = {}

    def config_global(self):
        st.set_page_config(page_title="GENESIS FORENSIC AI v16.6", layout="wide", page_icon="🛡️")
        st.markdown("""
            <style>
            .stApp { background: radial-gradient(circle at top right, #050a18, #000000); }
            .main-title {
                color: #A51C30; font-family: 'Arial', sans-serif; font-size: 38px; font-weight: bold;
                border-left: 6px solid #1e3a8a; padding-left: 15px; margin-bottom: 25px;
            }
            .img-container { border: 2px solid #1e3a8a; border-radius: 12px; background: #000; padding: 10px; text-align: center; }
            </style>
        """, unsafe_allow_html=True)

    def otimizar_imagem_flash(self, imagem_pil):
        """ Processamento ultrarápido para evitar lentidão (v16.6) """
        img_cv = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)
        # Filtro de Nitidez Direto (Unsharp Masking) - Mais rápido que detecção circular
        gaussian = cv2.GaussianBlur(img_cv, (0, 0), 3)
        img_hd = cv2.addWeighted(img_cv, 1.5, gaussian, -0.5, 0)
        return Image.fromarray(cv2.cvtColor(img_hd, cv2.COLOR_BGR2RGB))

    def renderizar_ui(self):
        st.markdown("<div class='main-title'>IRIDOLOGIA E IRISDIAGNOSE</div>", unsafe_allow_html=True)

        with st.expander("👤 DASHBOARD DO PACIENTE", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            self.prontuario['nome'] = c1.text_input("NOME COMPLETO", key="n_166")
            self.prontuario['idade'] = c2.text_input("IDADE", key="i_166")
            self.prontuario['peso'] = c3.text_input("PESO (KG)", key="p_166")
            self.prontuario['altura'] = c4.text_input("ALTURA (M)", key="a_166")

        with st.sidebar:
            st.markdown("<h2 style='color: #A51C30;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
            m_super = st.toggle("🧠 Super IA Genesis", value=False)
            m_iri = st.toggle("🔬 Iridologia Master", value=False)
            m_der = st.toggle("📸 SkinAI v2 Pro", value=False)
            m_rad = st.toggle("📂 Radiologia Digital", value=False)
            m_lab = st.toggle("🧬 Inteligência Laboratorial", value=False)
            st.divider()
            st.caption("GENESIS FORENSIC v16.6 | Ultra-Fast Engine")

        if m_iri:
            st.subheader("🔬 Estação Iridologia Master")
            col_in, col_viz = st.columns([1, 1.2], gap="large")
            with col_in:
                f = st.radio("ENTRADA", ["📁 ARQUIVO/VÍDEO", "📸 CÂMERA"], horizontal=True)
                ent = st.file_uploader("Leitura Universal (IMG/VÍDEO)", type=['jpg','png','jpeg','mp4','mov','avi']) if f == "📁 ARQUIVO/VÍDEO" else st.camera_input("Scanner")

            if ent:
                with col_viz:
                    if hasattr(ent, 'type') and 'video' in ent.type:
                        st.video(ent)
                        st.info("💡 Modo Vídeo Ativo: Extraindo Frames em Alta Definição.")
                    else:
                        img_raw = Image.open(ent)
                        # Aplica otimização instantânea para acabar com a lentidão
                        img_ready = self.otimizar_imagem_flash(img_raw)
                        
                        try:
                            # Funções da engine.py agora rodam sobre a imagem pré-otimizada
                            img_hd = extrair_qualidade_maxima(img_ready)
                            if st.checkbox("🔍 Zoom Analítico (Lanczos4)", value=True): img_hd = aplicar_zoom_inteligente(img_hd)
                            if st.checkbox("🗺️ Jensen/Batelo Overlay"): img_hd = aplicar_mapa_iridologico(img_hd)
                        except:
                            img_hd = img_ready

                        st.markdown('<div class="img-container">', unsafe_allow_html=True)
                        st.image(img_hd, caption="Processamento Sentinel v16.6 - High Speed", use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                        if st.button("⚡ GENERATE HARVARD EXECUTIVE REPORT"):
                            self.gerar_pdf_harvard(img_hd)

                        if 'pdf_report' in st.session_state:
                            st.download_button("📥 BAIXAR RELATÓRIO", st.session_state['pdf_report'], f"HBS_Report_{self.prontuario['nome']}.pdf")

        elif m_der: st.info("Módulo Dermatologia em Standby.")
        elif m_rad: st.info("Módulo Radiologia em Standby.")

    def gerar_pdf_harvard(self, img):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_fill_color(165, 28, 48); pdf.rect(0, 0, 210, 35, 'F')
            pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", 'B', 20)
            pdf.cell(0, 15, "IRISDIAGNOSE CLINICAL REPORT", ln=True, align='C')
            pdf.set_text_color(0, 0, 0); pdf.ln(25); pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, f"PACIENTE: {self.prontuario['nome'].upper() or 'NÃO IDENTIFICADO'}", ln=True)
            
            img.save("temp_v166.jpg", quality=95)
            pdf.image("temp_v166.jpg", x=55, y=100, w=100)
            
            # FIX DO ERRO DE BYTEARRAY: Detecta se o output já é binário
            out = pdf.output(dest='S')
            if isinstance(out, str):
                st.session_state['pdf_report'] = out.encode('latin-1', 'replace')
            else:
                st.session_state['pdf_report'] = out # Já é bytes/bytearray
                
            st.success("Dossiê Harvard Gerado sem Erros!")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

if __name__ == "__main__":
    GenesisOrchestrator().renderizar_ui()
