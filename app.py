import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA E DESIGN ---
st.set_page_config(page_title="Nexus OmniCode", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 10px; }
    .stTextArea>div>div>textarea { background-color: #1a1c24; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE BLINDAGEM (SENHA) ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    cols = st.columns()
    with cols:
        st.title("🔒 Nexus Blindado")
        senha = st.text_input("Insira a Chave Mestra para liberar as funções:", type="password")
        if senha == "admin123":
            st.session_state['autenticado'] = True
            st.rerun()
        else:
            st.warning("Aguardando autenticação...")
            st.stop()

# --- INICIALIZAÇÃO DA IA (GROQ) ---
# Certifique-se de que a GROQ_API_KEY esteja nos Secrets do Streamlit
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Erro: API Key não encontrada nos Secrets do Streamlit!")
    st.stop()

# --- FUNÇÃO DE CÉREBRO INTEGRADO ---
def nexus_process(ideia, modo, contexto_web):
    prompt_sistema = f"""
    Você é o Nexus OmniCode, a IA mais avançada do mundo em engenharia de software.
    Seu objetivo agora é: {modo}.
    Você deve analisar as respostas de outras fontes: {contexto_web}
    E entregar um código superior, corrigido, limpo e pronto para produção.
    Responda sempre em Português e use blocos de código formatados.
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": ideia},
        ],
        model="llama3-70b-8192", # Modelo de alta performance
        temperature=0.2,
    )
    return chat_completion.choices.message.content

# --- BARRA LATERAL (FILTROS E INTEGRAÇÕES) ---
with st.sidebar:
    st.title("🔗 Nexus Integrations")
    st.subheader("Sistemas Monitorados")
    for app in ["GitLab (DevSecOps)", "Bitbucket", "Azure DevOps", "Gitea", "SourceForge", "FastAPI"]:
        st.toggle(app, value=True)
    
    st.divider()
    modo = st.selectbox("🎯 Função Principal", [
        "Criar código do zero", 
        "Corrigir erros e bugs", 
        "Analisar performance", 
        "Gerar Documentação",
        "Aprimorar código existente"
    ])

# --- ÁREA PRINCIPAL ---
st.title("⚡ Nexus OmniCode")
st.caption("Automação de Análise, Correção e Criação Universal")

col_in, col_out = st.columns()

with col_in:
    st.subheader("📥 Entrada de Dados")
    user_input = st.text_area("Descreva sua ideia ou cole o código aqui:", height=300, placeholder="Ex: Crie um sistema de análise de sentimentos para o GitLab...")
    upload = st.file_uploader("Upload de arquivo para análise", type=['py', 'js', 'html', 'txt', 'sql'])

with col_out:
    st.subheader("🚀 Resultado da IA Personalizada")
    if st.button("EXECUTAR ANÁLISE GLOBAL"):
        if user_input:
            with st.spinner("Nexus consultando bases globais e sintetizando código..."):
                # Busca "Invisível" para alimentar o Nexus
                try:
                    with DDGS() as ddgs:
                        search_results = [r['body'] for r in ddgs.text(f"best practices and code for: {user_input}", max_results=3)]
                        contexto = "\n".join(search_results)
                except:
                    contexto = "Sem acesso à web no momento. Usando base interna."

                # Processamento com a Groq
                resultado_final = nexus_process(user_input, modo, contexto)
                st.markdown(resultado_final)
                
                # Gerar botão de download
                st.download_button(
                    label="📥 Baixar Código Aprimorado",
                    data=resultado_final,
                    file_name="nexus_optimized_code.txt",
                    mime="text/plain"
                )
        else:
            st.error("Digite algo para o Nexus analisar!")

# --- BIBLIOTECA DE COMANDOS ---
st.divider()
with st.expander("📚 Biblioteca de Comandos (Copie e Cole)"):
    st.code("Nexus, aja como uma IA personalizada e crie um script de automação para o Azure.")
    st.code("Analise este código, encontre erros e gere uma versão aprimorada com filtros de segurança.")
    st.code("Crie um arquivo FastAPI completo baseado na ideia acima.")
