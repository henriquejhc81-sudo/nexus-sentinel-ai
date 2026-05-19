import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA E DESIGN CYBER-SENTINEL ---
st.set_page_config(page_title="Nexus Sentinel v5.3", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stButton>button { 
        background: linear-gradient(135deg, #00c853 0%, #b2ff59 100%); 
        color: #000; font-weight: 800; border-radius: 8px; border: none; transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 200, 83, 0.3);
    }
    .status-box { 
        padding: 15px; border-radius: 10px; background: #161b22; 
        border: 1px solid #00c853; box-shadow: inset 0 0 10px rgba(0, 200, 83, 0.1);
        margin-bottom: 20px; font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE IA COM BLINDAGEM ANTI-ERRO 429 ---
def nexus_agent_call(prompt, modo, contexto):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        return "Erro: Chave API ausente nos Secrets!"
        
    max_retries = 5 # Aumentado para maior persistência
    for attempt in range(max_retries):
        try:
            prompt_sistema = f"""
            Você é o Nexus Sentinel 5.3. Missão: {modo}.
            DIRETRIZ OBRIGATÓRIA: Em QUALQUER projeto, inclua um '🛡️ MÓDULO DE SEGURANÇA' com Logs de Invasão e proteção contra intrusos.
            
            MODO ARQUITETO:
            1. '🛠️ SETUP'
            2. '📁 ESTRUTURA'
            3. '🚀 CÓDIGO COMPLETO'
            
            Responda em Português.
            """
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1,
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                # ESTRATÉGIA ANTI-BLOQUEIO: Espera progressiva
                wait_time = (attempt + 1) * 8 
                st.warning(f"🛡️ Nexus detectou Limite de Cota (429). Ativando Auto-Healing... Aguarde {wait_time}s")
                time.sleep(wait_time)
            else:
                return f"Erro Crítico no Sentinel: {e}"
    return "O Nexus não conseguiu furar o bloqueio da API após 5 tentativas. Tente reduzir o tamanho do pedido."

# --- BARRA LATERAL (ESTRUTURA MANTIDA) ---
with st.sidebar:
    st.title("🛡️ Nexus Sentinel")
    st.caption("v5.3 | Anti-Lock Mode")
    
    st.divider()
    with st.expander("🚀 Superpoderes Ativos", expanded=True):
        st.toggle("Segurança Nativa em Tudo", value=True)
        st.toggle("Auto-Healing Anti-429", value=True)
        st.toggle("Modo Arquiteto", value=True)
        st.toggle("Live Preview", value=True)

    st.divider()
    st.subheader("🔗 DevSecOps")
    for app in ["GitLab", "GitHub", "Azure DevOps", "Slack/Notion"]:
        st.toggle(app, value=True)
    
    modo = st.selectbox("🎯 Modo do Agente", [
        "Projeto do Zero (Modo Arquiteto)",
        "Incremento Mágico + Testes",
        "Análise de Vulnerabilidades",
        "Design-to-Code"
    ])

# --- ÁREA PRINCIPAL ---
st.title("⚡ Nexus OmniCode Sentinel")
st.markdown("<div class='status-box'><b>STATUS:</b> PROTEGIDO | <b>ANTI-429:</b> ATIVO | <b>SEGURANÇA:</b> INTEGRAL</div>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Missão")
    user_input = st.text_area("Descreva seu projeto (Segurança incluída automaticamente):", height=300)
    upload = st.file_uploader("Contexto (Opcional)", accept_multiple_files=True)

with col_out:
    st.subheader("🚀 Entrega Sentinel")
    if st.button("ATIVAR NEXUS SENTINEL"):
        if user_input:
            with st.spinner("Sentinel rompendo bloqueios de cota e processando..."):
                try:
                    with DDGS() as ddgs:
                        busca = [r['body'] for r in ddgs.text(f"security architecture for {user_input}", max_results=2)]
                        contexto = "\n".join(busca)
                except:
                    contexto = "Base interna de elite."
                
                resultado = nexus_agent_call(user_input, modo, contexto)
                st.session_state['last_result'] = resultado
        else:
            st.error("Diga ao Nexus o que construir.")

    if 'last_result' in st.session_state:
        resultado = st.session_state['last_result']
        tab1, tab2 = st.tabs(["💻 Plano e Código", "🖼️ Live Preview"])
        with tab1:
            st.markdown(resultado)
        with tab2:
            if "<html>" in resultado.lower() or "<!doctype html>" in resultado.lower():
                st.components.v1.html(resultado, height=500, scrolling=True)
            else:
                st.info("Aguardando código HTML...")

        st.divider()
        formato_ext = st.selectbox("Formato:", [".py", ".html", ".js", ".txt"], key="f_selector")
        st.download_button(label=f"BAIXAR PROJETO ({formato_ext})", data=resultado, file_name=f"nexus_sentinel_v53{formato_ext}")

st.divider()
st.subheader("💬 Nexus Sentinel Chat")
chat_input = st.text_input("Dúvida? Pergunte aqui:")
if chat_input and 'last_result' in st.session_state:
    with st.chat_message("assistant"):
        st.markdown(nexus_agent_call(f"Sobre o projeto: {st.session_state['last_result']}. Pergunta: {chat_input}", "Chat Suporte", ""))
