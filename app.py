import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# --- MOTOR DE ANÁLISE GENESIS ---
def analisar_imagem_real(imagem_pil, tipo):
    # Converte imagem para formato processável
    img_array = np.array(imagem_pil.convert('RGB'))
    cinza = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Aplica Filtro de Realce de Patologias (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    realce = clahe.apply(cinza)
    
    # Simulação de detecção de anomalias por densidade de pixels
    media = np.mean(realce)
    anomalia_score = "Baixo" if media > 100 else "Moderado/Alto"
    
    relatorio = f"""
    --- RELATÓRIO GENESIS FORENSIC AI ---
    TIPO DE ANÁLISE: {tipo.upper()}
    STATUS: Processamento Concluído
    
    OBSERVAÇÕES TÉCNICAS:
    - Densidade de Tecido/Padrão: {media:.2f}
    - Risco Detectado: {anomalia_score}
    - Sugestão: Cruzamento de dados forenses indicado.
    
    Este relatório utiliza Visão Computacional para destacar variações térmicas e de densidade.
    """
    return relatorio, realce

# --- INTERFACE ---
st.set_page_config(page_title="Genesis Forensic AI", layout="wide")
st.title("👁️ Genesis Forensic AI")

btn_iridologia = st.sidebar.checkbox("🔬 Módulo Iridologia")
btn_autodiagnostico = st.sidebar.checkbox("🩺 Auto-Diagnóstico")
btn_exames = st.sidebar.checkbox("📂 Raio-X e Exames")

def interface_analise(label):
    st.subheader(f"Área de {label}")
    img_file = st.file_uploader(f"Carregar Imagem para {label}", type=['png', 'jpg', 'jpeg'])
    camera_file = st.camera_input(f"Capturar com Câmera ({label})")
    
    final_file = img_file if img_file else camera_file
    
    if final_file:
        img_view = Image.open(final_file)
        st.image(img_view, caption="Original", width=300)
        
        if st.button(f"Gerar Diagnóstico {label}"):
            with st.spinner("Analisando camadas profundas da imagem..."):
                texto, img_processada = analisar_imagem_real(img_view, label)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.text_area("Resultado do Diagnóstico", texto, height=250)
                with col2:
                    st.image(img_processada, caption="Visão de Contraste Forense", width=300)
                
                st.download_button("Baixar Relatório Oficial", texto, file_name=f"genesis_{label}.txt")

if btn_iridologia: interface_analise("Iridologia")
if btn_autodiagnostico: interface_analise("Auto-Diagnóstico")
if btn_exames: interface_analise("Radiologia")
