import streamlit as st
import datetime
import cv2
import numpy as np
from PIL import Image
import io

# Tenta carregar os motores e o gerador de PDF
try:
    from fpdf import FPDF
except:
    st.error("Instale 'fpdf2' para gerar relatórios.")

try:
    from engine import * 
except:
    pass # Caso o engine.py ainda não tenha as funções, o sistema não trava

# --- ARQUITETURA FOCO IRIDOLOGIA v16.3 ---
class GenesisIridologia:
    def __init__(self):
        self.config_ui()
        self.paciente = {}

    def config_ui(self):
        st.set_page_config(page_title="IRIDOLOGIA E IRISDIAGNOSE", layout="wide", page_icon="🔬")
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

    def motor_ia_trava_iris(self, imagem_pil):
        """ Localiza a íris em qualquer posição (v16.3 Blindada) """
        try:
            img_cv = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)
            h, w = img_cv.shape[:2]
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            detectado = None
            
            # FIX DEFINITIVO: Uso de range(3,11,2) para evitar erro de sintaxe no servidor
            for b in range(3, 11, 2):
                blurred = cv2.GaussianBlur(gray, (b, b), 0)
                circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1.2, 100, 
                                           param1=50, param2=35, minRadius=int(h/10), maxRadius=int(h/2))
                if circles is not None:
                    detectado = np.round(circles[0, :]).astype("int")
                    break

            if detectado is not None:
                cx, cy, cr = int(detectado[0]), int(detectado[1]), int(detectado)
                margem = int(cr * 3.0)
                y1, y2 = max(0, cy - margem), min(h, cy + margem)
                x1, x2 = max(0, cx - margem), min(w, cx + margem)
                crop = img_cv[y1:y2, x1:x2]
                return Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
        except:
            pass
        return imagem_pil

    def interface(self):
        st.markdown("<div class='main-title'>IRIDOLOGIA E IRISDIAGNOSE</div>", unsafe_allow_html=True)

        # 1. DASHBOARD
        with st.expander("👤 DASHBOARD DO PACIENTE", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            self.paciente['nome'] = c1.text_input("NOME COMPLETO", key="n_163")
            self.paciente['idade'] = c2.text_input("IDADE", key="i_163")
            self.paciente['peso'] = c3.text_input("PESO (KG)", key="p_163")
            self.paciente['altura'] = c4.text_input("ALTURA (M)", key="a_163")

        # 2. SIDEBAR
        with st.sidebar:
            st.markdown("<h2 style='color: #A51C30;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
            m_iri = st.toggle("🔬 Módulo Iridologia Master", value=False)
            st.divider()
            st.caption("GENESIS FORENSIC v16.3 | Foco Iridologia")

        # 3. ESTAÇÃO MASTER
        if m_iri:
            st.subheader("🔬 ESTAÇÃO IRIDOLOGIA MASTER")
            col_in, col_viz = st.columns([1, 1.2], gap="large")
            
            with col_in:
                f = st.radio("FONTE", ["📁 ARQUIVO/VÍDEO", "📸 CÂMERA"], horizontal=True)
                ent = st.file_uploader("Subir Íris", type=['jpg','png','jpeg','mp4','mov']) if f == "📁 ARQUIVO/VÍDEO" else st.camera_input("Capturar")

            if ent:
                with col_viz:
                    img_raw = Image.open(ent)
                    img_focada = self.motor_ia_trava_iris(img_raw)
                    
                    # Funções do engine.py preservadas
                    try:
                        img_hd = extrair_qualidade_maxima(img_focada)
                        if st.checkbox("🔍 Zoom Analítico", value=True): 
                            img_hd = aplicar_zoom_inteligente(img_hd)
                        if st.checkbox("🗺️ Jensen Overlay"): 
                            img_hd = aplicar_mapa_iridologico(img_hd)
                    except:
                        img_hd = img_focada

                    st.markdown('<div class="img-container">', unsafe_allow_html=True)
                    st.image(img_hd, caption="Processamento Sentinel v16.3", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    if st.button("⚡ GERAR RELATÓRIO HARVARD"):
                        self.gerar_pdf(img_hd)

                    if 'pdf_ready' in st.session_state:
                        st.download_button("📥 BAIXAR RELATÓRIO", st.session_state['pdf_ready'], f"IrisReport_{self.paciente['nome']}.pdf")

    def gerar_pdf(self, img):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(165, 28, 48); pdf.rect(0, 0, 210, 35, 'F')
        pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 15, "IRISDIAGNOSE CLINICAL REPORT", ln=True, align='C')
        pdf.set_text_color(0, 0, 0); pdf.ln(25); pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"PACIENTE: {self.paciente['nome'].upper()}", ln=True)
        img.save("temp.jpg")
        pdf.image("temp.jpg", x=55, y=100, w=100)
        st.session_state['pdf_ready'] = pdf.output(dest='S').encode('latin-1', 'replace')
        st.success("Dossiê Criado!")

if __name__ == "__main__":
    GenesisIridologia().interface()
