import streamlit as st
import datetime
import cv2
import numpy as np
from PIL import Image
import io
from fpdf import FPDF

# --- MOTORES DE ALTA PERFORMANCE (ENGINE.PY) ---
try:
    from engine import * 
except ImportError:
    pass

class GenesisOrchestrator:
    def __init__(self):
        self.config_global()
        self.prontuario = {}

    def config_global(self):
        st.set_page_config(page_title="GENESIS FORENSIC AI v16.7", layout="wide", page_icon="🛡️")
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

    def renderizar_ui(self):
        st.markdown("<div class='main-title'>IRIDOLOGIA E IRISDIAGNOSE</div>", unsafe_allow_html=True)

        with st.expander("👤 DASHBOARD DO PACIENTE", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            self.prontuario['nome'] = c1.text_input("NOME COMPLETO", key="n_167")
            self.prontuario['idade'] = c2.text_input("IDADE", key="i_167")
            self.prontuario['peso'] = c3.text_input("PESO (KG)", key="p_167")
            self.prontuario['altura'] = c4.text_input("ALTURA (M)", key="a_167")

        with st.sidebar:
            st.markdown("<h2 style='color: #A51C30;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
            m_iri = st.toggle("🔬 Iridologia Master", value=False)
            m_super = st.toggle("🧠 Super IA Genesis", value=False)
            m_der = st.toggle("📸 SkinAI v2 Pro", value=False)
            m_rad = st.toggle("📂 Radiologia Digital", value=False)
            m_lab = st.toggle("🧬 Inteligência Laboratorial", value=False)
            st.divider()
            st.caption("GENESIS FORENSIC v16.7 | Interative Overlay")

        if m_iri:
            st.subheader("🔬 Estação Iridologia Master")
            col_in, col_viz = st.columns([1, 1.2], gap="large")
            with col_in:
                f = st.radio("ENTRADA", ["📁 ARQUIVO/VÍDEO", "📸 CÂMERA"], horizontal=True)
                ent = st.file_uploader("Leitura Universal", type=['jpg','png','jpeg','mp4','mov','avi']) if f == "📁 ARQUIVO/VÍDEO" else st.camera_input("Scanner")

            if ent:
                with col_viz:
                    if hasattr(ent, 'type') and 'video' in ent.type:
                        st.video(ent)
                    else:
                        img_raw = Image.open(ent)
                        
                        # CONTROLES INTERATIVOS PARA O OVERLAY (Sua sugestão)
                        st.markdown("---")
                        map_on = st.checkbox("🗺️ Ativar Jensen/Batelo Overlay")
                        
                        # Sliders dinâmicos aparecem apenas se o overlay estiver ativo
                        if map_on:
                            st.write("🎯 Ajuste o Posicionamento do Mapa:")
                            off_x = st.slider("Ajuste Lateral (X)", -200, 200, 0)
                            off_y = st.slider("Ajuste Altura (Y)", -200, 200, 0)
                            escala = st.slider("Tamanho do Círculo", 0.5, 2.5, 1.0)
                            
                            # Função para aplicar overlay com as coordenadas manuais
                            img_hd = self.aplicar_overlay_interativo(img_raw, off_x, off_y, escala)
                        else:
                            try:
                                img_hd = extrair_qualidade_maxima(img_raw)
                                if st.checkbox("🔍 Zoom Analítico", value=True): 
                                    img_hd = aplicar_zoom_inteligente(img_hd)
                            except:
                                img_hd = img_raw

                        st.markdown('<div class="img-container">', unsafe_allow_html=True)
                        st.image(img_hd, caption="Processamento Interativo v16.7", use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                        if st.button("⚡ GENERATE HARVARD EXECUTIVE REPORT"):
                            self.gerar_pdf_harvard(img_hd)

                        if 'pdf_report' in st.session_state:
                            st.download_button("📥 BAIXAR RELATÓRIO", st.session_state['pdf_report'], f"HBS_Report_{self.prontuario['nome']}.pdf", mime="application/pdf")

    def aplicar_overlay_interativo(self, img_pil, off_x, off_y, escala):
        """ Aplica o mapa de Jensen com ajustes manuais de X, Y e Tamanho """
        img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        h, w = img_cv.shape[:2]
        centro_x, centro_y = (w // 2) + off_x, (h // 2) + off_y
        raio = int((min(h, w) // 3) * escala)
        
        # Desenha o Mapa de Jensen Interativo
        overlay = img_cv.copy()
        cv2.circle(overlay, (centro_x, centro_y), raio, (30, 58, 146), 3) # Azul Batello
        for i in range(0, 360, 30): # Linhas horárias
            angulo = np.deg2rad(i)
            x2 = int(centro_x + raio * np.cos(angulo))
            y2 = int(centro_y + raio * np.sin(angulo))
            cv2.line(overlay, (centro_x, centro_y), (x2, y2), (30, 58, 146), 1)
        
        cv2.addWeighted(overlay, 0.4, img_cv, 0.6, 0, img_cv)
        return Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

    def gerar_pdf_harvard(self, img):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_fill_color(165, 28, 48); pdf.rect(0, 0, 210, 35, 'F')
            pdf.set_font("Arial", 'B', 20); pdf.set_text_color(255, 255, 255)
            pdf.cell(0, 15, "IRISDIAGNOSE CLINICAL REPORT", ln=True, align='C')
            
            pdf.set_text_color(0, 0, 0); pdf.ln(25); pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, f"PACIENTE: {self.prontuario['nome'].upper() or 'NÃO IDENTIFICADO'}", ln=True)
            
            img.save("temp_v167.jpg", quality=95)
            pdf.image("temp_v167.jpg", x=55, y=100, w=100)
            
            # FIX DEFINITIVO DO DOWNLOAD: Garantindo conversão para bytes
            pdf_bytes = pdf.output(dest='S')
            if not isinstance(pdf_bytes, bytes):
                pdf_bytes = bytes(pdf_bytes)
            
            st.session_state['pdf_report'] = pdf_bytes
            st.success("Dossiê Harvard Gerado!")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

if __name__ == "__main__":
    GenesisOrchestrator().renderizar_ui()
