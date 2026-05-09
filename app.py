import streamlit as st
import datetime
import cv2
import numpy as np
from PIL import Image
import io

# Tenta carregar as bibliotecas do seu requirements de forma segura
try:
    from fpdf import FPDF
except ImportError:
    st.error("Erro: fpdf2 não instalado. Verifique o requirements.txt")

try:
    from engine import * 
except ImportError:
    st.warning("Atenção: Funções de engine.py não localizadas. Operando em modo de segurança.")

# --- ARQUITETURA GLOBAL GENESIS v16.2 ---
class GenesisForensic:
    def __init__(self):
        self.configurar_interface()
        self.paciente = {}

    def configurar_interface(self):
        st.set_page_config(page_title="IRIDOLOGIA & IRISDIAGNOSE PRO", layout="wide", page_icon="🔬")
        st.markdown("""
            <style>
            .stApp { background: radial-gradient(circle at top right, #050a18, #000000); }
            .main-title {
                color: #A51C30; font-family: 'Inter', sans-serif; font-size: 38px; font-weight: 800;
                border-left: 5px solid #1e3a8a; padding-left: 15px; margin-bottom: 30px;
            }
            .img-container { border: 2px solid #1e3a8a; border-radius: 12px; background: #000; padding: 10px; text-align: center; }
            </style>
        """, unsafe_allow_html=True)

    def motor_ia_trava_iris(self, imagem_pil):
        """ Localiza a íris em qualquer posição com Scan Multivariado (v16.2) """
        try:
            img_cv = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)
            h, w = img_cv.shape[:2]
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            detectado = None
            
            # LISTA DE VARREDURA CORRIGIDA (Blindada contra SyntaxError)
            for b in:
                blurred = cv2.GaussianBlur(gray, (b, b), 0)
                circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1.2, 100, 
                                           param1=50, param2=35, minRadius=int(h/10), maxRadius=int(h/2))
                if circles is not None:
                    detectado = np.round(circles[0, :]).astype("int")
                    break

            if detectado is not None:
                cx, cy, cr = detectado, detectado, detectado[2]
                margem = int(cr * 3.0)
                y1, y2 = max(0, cy - margem), min(h, cy + margem)
                x1, x2 = max(0, cx - margem), min(w, cx + margem)
                crop = img_cv[y1:y2, x1:x2]
                return Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
        except Exception as e:
            st.sidebar.error(f"Erro no Rastreio: {e}")
        return imagem_pil

    def interface_principal(self):
        st.markdown("<div class='main-title'>IRIDOLOGIA E IRISDIAGNOSE</div>", unsafe_allow_html=True)

        # 1. DASHBOARD DO PACIENTE
        with st.expander("👤 DASHBOARD DO PACIENTE", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            self.paciente['nome'] = c1.text_input("NOME COMPLETO", key="n162")
            self.paciente['idade'] = c2.text_input("IDADE", key="i162")
            self.paciente['peso'] = c3.text_input("PESO (KG)", key="p162")
            self.paciente['altura'] = c4.text_input("ALTURA (M)", key="a162")

        # 2. COMMAND CENTER (ORQUESTRADOR DE MÓDULOS)
        with st.sidebar:
            st.markdown("<h2 style='color: #A51C30;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
            m_iri = st.toggle("🔬 Módulo Iridologia Master", value=False)
            m_super = st.toggle("🧠 Orquestração Neural IA", value=False)
            m_der = st.toggle("📸 SkinAI v2 Pro", value=False)
            m_rad = st.toggle("📂 Radiologia Digital", value=False)
            st.divider()
            st.caption("GENESIS FORENSIC v16.2 | Multi-Module Ready")

        # 3. LÓGICA DO MÓDULO IRIDOLOGIA
        if m_iri:
            st.subheader("🔬 ESTAÇÃO IRIDOLOGIA MASTER")
            col_in, col_viz = st.columns([1, 1.2], gap="large")
            
            with col_in:
                f = st.radio("FONTE DE DADOS", ["📁 ARQUIVO/VÍDEO", "📸 CÂMERA"], horizontal=True)
                ent = st.file_uploader("Importar Mídia HD", type=['jpg','png','jpeg','mp4','mov']) if f == "📁 ARQUIVO/VÍDEO" else st.camera_input("Scanner")

            if ent:
                with col_viz:
                    img_raw = Image.open(ent)
                    # IA DE RASTREIO E CENTRALIZAÇÃO
                    img_focada = self.motor_ia_trava_iris(img_raw)
                    img_hd = extrair_qualidade_maxima(img_focada)
                    
                    t1, t2 = st.columns(2)
                    if t1.checkbox("🔍 Zoom Analítico (Sentinel)", value=True): 
                        img_hd = aplicar_zoom_inteligente(img_hd)
                    if t2.checkbox("🗺️ Jensen/Batelo Overlay"): 
                        img_hd = aplicar_mapa_iridologico(img_hd)
                    
                    st.markdown('<div class="img-container">', unsafe_allow_html=True)
                    st.image(img_hd, caption="Processamento Sentinel v16.2", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    if st.button("⚡ GENERATE HARVARD EXECUTIVE REPORT"):
                        self.gerar_relatorio_pdf(img_hd)

                    if 'pdf_buffer' in st.session_state:
                        st.download_button("📥 BAIXAR RELATÓRIO PDF", st.session_state['pdf_buffer'], f"HBS_Report_{self.paciente['nome']}.pdf")

        # Fallback para outros módulos (SkinAI, etc)
        elif m_der:
            st.info("Módulo SkinAI v2 Pro aguardando integração de engine.")

    def gerar_relatorio_pdf(self, img):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(165, 28, 48); pdf.rect(0, 0, 210, 35, 'F')
        pdf.set_text_color(255, 255, 255); pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 15, "IRISDIAGNOSE CLINICAL REPORT", ln=True, align='C')
        
        pdf.set_text_color(0, 0, 0); pdf.ln(25); pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"PACIENTE: {self.paciente['nome'].upper() or 'NÃO IDENTIFICADO'}", ln=True)
        
        img.save("temp_report.jpg")
        pdf.image("temp_report.jpg", x=55, y=100, w=100)
        
        st.session_state['pdf_buffer'] = pdf.output(dest='S').encode('latin-1', 'replace')
        st.success("Dossiê Harvard Estruturado!")

if __name__ == "__main__":
    GenesisForensic().interface_principal()
