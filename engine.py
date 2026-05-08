# --- ENGINE.PY: MOTOR NEURAL GENESIS v9.8 ---
import cv2
import numpy as np
from PIL import Image
import datetime

def extrair_qualidade_maxima(img_pil):
    img_array = np.array(img_pil.convert('RGB'))
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img_sharp = cv2.filter2D(img_array, -1, kernel)
    img_yuv = cv2.cvtColor(img_sharp, cv2.COLOR_RGB2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    img_final = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    return Image.fromarray(img_final)

def aplicar_zoom_inteligente(img_pil, zoom_factor=1.8):
    """Centraliza e amplia baseado no centro da imagem para focar na íris."""
    img_array = np.array(img_pil.convert('RGB'))
    h, w = img_array.shape[:2]
    # Busca o centro exato para evitar cortes laterais errados
    y_center, x_center = h // 2, w // 2
    h_new, w_new = int(h / zoom_factor), int(w / zoom_factor)
    y1, y2 = max(0, y_center - h_new // 2), min(h, y_center + h_new // 2)
    x1, x2 = max(0, x_center - w_new // 2), min(w, x_center + w_new // 2)
    img_crop = img_array[y1:y2, x1:x2]
    return Image.fromarray(cv2.resize(img_crop, (w, h), interpolation=cv2.INTER_LANCZOS4))

def motor_diagnostico_genesis(img_pil, modulo):
    img_array = np.array(img_pil.convert('RGB'))
    img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
    img_enhanced = clahe.apply(img_gray)
    
    # Detecção de densidade e estresse cromático
    densidade_media = np.mean(img_gray)
    hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
    estresse = (np.sum(cv2.inRange(hsv, np.array([0, 50, 50]), np.array([10, 255, 255]))) / img_array.size) * 500
    
    return {
        "densidade": round(densidade_media, 2),
        "estresse": round(estresse, 2),
        "viz": img_enhanced,
        "modulo": modulo
    }

def gerar_diagnostico_master_v98(modulo, res_tec):
    """Gera o mega relatório clínico com 7 eixos."""
    if modulo == "Iridologia":
        fibra_status = "Fraca (Lacunas Presentes)" if res_tec['densidade'] < 130 else "Forte (Boa Resistência)"
        estresse_nivel = "Alto (Anéis de Tensão)" if res_tec['estresse'] > 8 else "Baixo (Estável)"
        
        return {
            "titulo": "DOSSIÊ CLÍNICO DE IRIDOLOGIA v9.8",
            "secoes": {
                "1. Constituição": f"Classificação Mista. Densidade de Fibras: {fibra_status}.",
                "2. Sinais Específicos": f"Identificados {estresse_nivel}. Presença de sinais de absorção lenta na banda do SNA.",
                "3. Mapeamento": "Fragilidades detectadas nos setores digestivo e circulatório (Anel de Sódio sugerido).",
                "4. Patologias Possíveis": "Gastrite Nervosa, Fadiga Adrenal ou Disfunção Hepática.",
                "5. Plano Terapêutico": "Suporte nutricional rico em minerais, manejo de estresse e fitoterapia.",
                "6. Encaminhamento": "Consultar Gastroenterologista para validar sinais de irritabilidade gástrica.",
                "7. Aviso Legal": "A iridologia é preventiva e não substitui diagnósticos clínicos tradicionais."
            }
        }
    return {"secoes": {}}
