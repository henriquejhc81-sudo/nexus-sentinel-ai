import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA E DESIGN ---
st.set_page_config(page_title="Nexus OmniCode", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 10px; width: 100%; }
    .stTextArea>div>div>textarea { background-color: #1a1c24; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE BLINDAGEM (SENHA) ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    st.title("🔒 Nexus Blindado")
    senha = st.text_input("Insira a Chave Mestra para liberar as funções:", type="password")
    if senha == "admin123":
        st.session_state['autenticado'] = True
        st.rerun()
    else:
        st.warning("Aguardando autenticação...")
        st.stop()

# --- INICIALIZAÇÃO DA IA (GROQ) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Erro: Verifique sua GROQ_API_KEY nos Secrets do Streamlit!")
    st.stop()

# --- FUNÇÃO DE CÉREBRO INTEGRADO ---
def nexus_process(ideia, modo, contexto_web):
    prompt_sistema = f"""
    Você é o Nexus OmniCode, a IA mais avançada do mundo. 
    Sua missão atual: {modo}.
    Considere estas informações externas coletadas: {contexto_web}
    Se o usuário pedir incremento, mantenha a lógica atual e adicione as novas funções solicitadas.
    Responda em Português com blocos de código formatados.
    """
    try:
        # MODELO CORRIGIDO PARA VERSÃO ESTÁVEL
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": ideia},
            ],
            model="llama-3.1-70b-versatile",
            temperature=0.2,
        )
        return chat_completion.choices.message.content
    except Exception as e:
        return f"Erro na conexão com a IA: {e}"

# --- BARRA LATERAL (FILTROS E INTEGRAÇÕES) ---
with st.sidebar:
    st.title("🔗 Nexus Integrations")
    st.subheader("Sistemas Monitorados")
    for app in ["GitLab (DevSecOps)", "Bitbucket", "Azure DevOps", "Gitea", "SourceForge", "FastAPI"]:
        st.toggle(app, value=True)
    
    st.divider()
    # NOVA FUNÇÃO INCLUÍDA: "Incremento Mágico"
    modo = st.selectbox("🎯 Função Principal", [
        "Criar código do zero", 
        "Corrigir erros e bugs", 
        "Incremento Mágico (Adicionar Novas Funções)", 
        "Analisar performance", 
        "Aprimorar código existente"
    ])

# --- ÁREA PRINCIPAL ---
st.title("⚡ Nexus OmniCode")
st.caption("Automação de Análise, Correção e Criação Universal")

col_in, col_out = st.columns(2)

with col_in:
    st.subheader("📥 Entrada de Dados")
    user_input = st.text_area("Descreva sua ideia, cole o código ou peça o incremento:", height=300, placeholder="Ex: [Cole seu código aqui] e escreva: 'Adicione uma função de envio de e-mail'...")
    upload = st.file_uploader("Upload de arquivo para análise", type=['py', 'js', 'html', 'txt', 'sql'])

with col_out:
    st.subheader("🚀 Resultado da IA Personalizada")
    if st.button("EXECUTAR ANÁLISE GLOBAL"):
        if user_input:
            with st.spinner("Nexus acessando bases globais para a evolução do código..."):
                contexto = ""
                try:
                    with DDGS() as ddgs:
                        search_results = [r['body'] for r in ddgs.text(f"melhores práticas e funções para: {user_input}", max_results=2)]
                        contexto = "\n".join(search_results)
                except:
                    contexto = "Usando base interna."

                resultado_final = nexus_process(user_input, modo, contexto)
                st.markdown(resultado_final)
                
                st.download_button(
                    label="📥 Baixar Código Nexus",
                    data=resultado_final,
                    file_name="nexus_output.txt",
                    mime="text/plain"
                )
        else:
            st.error("O campo de entrada está vazio!")

# --- BIBLIOTECA DE COMANDOS ---
st.divider()
with st.expander("📚 Biblioteca de Comandos Copie e Cole"):
    st.code("Nexus, use o Incremento Mágico para adicionar um sistema de login neste código.")
    st.code("Nexus, analise este código e gere uma versão aprimorada sem erros.")
    st.code("Crie uma automação que leia arquivos e faça upload para o Azure.")
