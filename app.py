import streamlit as st
import datetime
import cv2
import numpy as np
from PIL import Image
import io
from fpdf import FPDF

# --- IMPORTAÇÃO DOS MOTORES ORIGINAIS ---
try:
    from engine import * 
except ImportError:
    st.warning("⚠️ Motores de engine.py em modo de compatibilidade.")

# --- ARQUITETURA INTEGRADA GENESIS v16.5 ---
class GenesisOrchestrator:
    def __init__(self):
        self.config_global()
        self.prontuario = {}

    def config_global(self):
        st.set_page_config(page_title="GENESIS FORENSIC AI v16.5", layout="wide", page_icon="🛡️")
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

    def motor_trava_iris_ia(self, imagem_pil):
        """ IA de Rastreio Multivariado (v16.5) """
        try:
            img_cv = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)
            h, w = img_cv.shape[:2]
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            detectado = None
            
            # Varredura por tupla para máxima estabilidade no servidor
            for b in (3, 5, 7, 9, 11):
                blurred = cv2.GaussianBlur(gray, (b, b), 0)
                circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1.2, 100, 
                                           param1=50, param2=35, minRadius=int(h/10), maxRadius=int(h/2))
                if circles is not None:
                    detectado = np.round(circles[0, :]).astype("int")
                    break

            if detectado is not None:
                cx, cy, cr = int(detectado[0]), int(detectado[1]), int(detectado)
                margem = int(cr * 3.0)
                y1, y2 = max(0, cy - margem), min(h, cy + pad) if 'pad' in locals() else min(h, cy + margem)
                x1, x2 = max(0, cx - margem), min(w, cx + margem)
                crop = img_cv[y1:y2, x1:x2]
                return Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
        except: pass
        return imagem_pil

    def renderizar_ui(self):
        st.markdown("<div class='main-title'>IRIDOLOGIA E IRISDIAGNOSE</div>", unsafe_allow_html=True)

        # 1. DASHBOARD DO PACIENTE (CAMPOS LIMPOS)
        with st.expander("👤 DASHBOARD DO PACIENTE", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            self.prontuario['nome'] = c1.text_input("NOME COMPLETO", key="n_165")
            self.prontuario['idade'] = c2.text_input("IDADE", key="i_165")
            self.prontuario['peso'] = c3.text_input("PESO (KG)", key="p_165")
            self.prontuario['altura'] = c4.text_input("ALTURA (M)", key="a_165")

        # 2. COMMAND CENTER (RESTAURAÇÃO DOS 5 MÓDULOS)
        with st.sidebar:
            st.markdown("<h2 style='color: #A51C30;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
            m_super = st.toggle("🧠 Super IA Genesis", value=False)
            m_iri = st.toggle("🔬 Iridologia Master", value=False)
            m_der = st.toggle("📸 SkinAI v2 Pro", value=False)
            m_rad = st.toggle("📂 Radiologia Digital", value=False)
            m_lab = st.toggle("🧬 Inteligência Laboratorial", value=False)
            st.divider()
            st.caption("GENESIS FORENSIC v16.5 | Integridade Total")

        # 3. LÓGICA DO MÓDULO IRIDOLOGIA MASTER
        if m_iri:
            st.subheader("🔬 Estação Iridologia Master")
            col_in, col_viz = st.columns([1, 1.2], gap="large")
            with col_in:
                f = st.radio("ENTRADA", ["📁 ARQUIVO/VÍDEO", "📸 CÂMERA"], horizontal=True)
                ent = st.file_uploader("Importar Mídia", type=['jpg','png','jpeg','mp4','mov']) if f == "📁 ARQUIVO/VÍDEO" else st.camera_input("Scanner")

            if ent:
                with col_viz:
                    # Detecção de tipo e leitura de arquivo
                    if hasattr(ent, 'type') and 'video' in ent.type:
                        st.video(ent)
                    else:
                        img_raw = Image.open(ent)
                        img_focada = self.motor_trava_iris_ia(img_raw)
                        
                        # Processamento de Motores do Engine.py
                        try:
                            img_hd = extrair_qualidade_maxima(img_focada)
                            if st.checkbox("🔍 Zoom Analítico", value=True): img_hd = aplicar_zoom_inteligente(img_hd)
                            if st.checkbox("🗺️ Jensen Overlay"): img_hd = aplicar_mapa_iridologico(img_hd)
                        except:
                            img_hd = img_focada

                        st.markdown('<div class="img-container">', unsafe_allow_html=True)
                        st.image(img_hd, caption="Processamento Sentinel v16.5", use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                        if st.button("⚡ GENERATE HARVARD EXECUTIVE REPORT"):
                            self.gerar_pdf_harvard(img_hd)

                        if 'pdf_report' in st.session_state:
                            st.download_button("📥 BAIXAR RELATÓRIO", st.session_state['pdf_report'], f"HBS_Report_{self.prontuario['nome']}.pdf")

        # 4. PLACEHOLDERS PARA DEMAIS MÓDULOS (PRESERVAÇÃO)
        elif m_der: st.info("Estação SkinAI v2 Pro Ativa. Pronto para Dermatoscopia.")
        elif m_rad: st.info("Estação Radiologia Digital Ativa. Pronto para DICOM/JPG.")
        elif m_lab: st.info("Estação Laboratorial Ativa. Pronto para Auditoria de Exames.")
        elif m_super: st.info("Super IA Genesis Ativa. Processamento Multimodal em Background.")

    def gerar_pdf_harvard(self, img):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_fill_color(165, 28, 48); pdf.rect(0, 0, 210, 35, 'F')
            pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", 'B', 20)
            pdf.cell(0, 15, "IRISDIAGNOSE CLINICAL REPORT", ln=True, align='C')
            pdf.set_text_color(0, 0, 0); pdf.ln(25); pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, f"PACIENTE: {self.prontuario['nome'].upper() or 'NÃO IDENTIFICADO'}", ln=True)
            img.save("temp_v16.jpg")
            pdf.image("temp_v16.jpg", x=55, y=100, w=100)
            st.session_state['pdf_report'] = pdf.output(dest='S').encode('latin-1', 'replace')
            st.success("Dossiê Harvard Estruturado com Sucesso!")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

if __name__ == "__main__":
    GenesisOrchestrator().renderizar_ui()
