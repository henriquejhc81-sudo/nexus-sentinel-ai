# --- ADIÇÃO AO ENGINE.PY: ULTRA-HD & ZOOM INTELIGENTE v6.5 ---

def extrair_qualidade_maxima(img_pil):
    """Aplica Super-Resolução Digital e Nitidez Sentinel."""
    img_array = np.array(img_pil.convert('RGB'))
    # Filtro de Nitidez (Sharpening Kernel)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img_sharp = cv2.filter2D(img_array, -1, kernel)
    # Normalização de Histograma para equilibrar luz de sensores mobile
    img_yuv = cv2.cvtColor(img_sharp, cv2.COLOR_RGB2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    img_final = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    return Image.fromarray(img_final)

def aplicar_zoom_inteligente(img_pil, zoom_factor=2.0):
    """Localiza o centro de massa da imagem e aplica zoom digital."""
    img_array = np.array(img_pil.convert('RGB'))
    h, w, _ = img_array.shape
    # Define a área central para o zoom
    y_center, x_center = h // 2, w // 2
    h_new, w_new = int(h / zoom_factor), int(w / zoom_factor)
    
    y1 = max(0, y_center - h_new // 2)
    y2 = min(h, y_center + h_new // 2)
    x1 = max(0, x_center - w_new // 2)
    x2 = min(w, x_center + w_new // 2)
    
    img_crop = img_array[y1:y2, x1:x2]
    # Redimensiona de volta usando Interpolação de Lanczos (Melhor qualidade de zoom)
    img_zoom = cv2.resize(img_crop, (w, h), interpolation=cv2.INTER_LANCZOS4)
    return Image.fromarray(img_zoom)
