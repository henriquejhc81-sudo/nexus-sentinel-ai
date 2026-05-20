import streamlit as st
import sqlite3
import concurrent.futures
from groq import Groq
# Importa a classe do seu módulo
from nexus_orchestrator import NexusOrchestrator

# --- CONFIGURAÇÃO E DESIGN ---
st.set_page_config(page_title="Nexus Omnicore v8.5 | Global Ops", page_icon="🐉", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stButton>button { background: linear-gradient(135deg, #00c853 0%, #00e5ff 100%); color: #000; font-weight: 800; border-radius: 8px; border: none; height: 3.5em; width: 100%; }
    .status-box { padding: 15px; border-radius: 10px; background: #161b22; border: 1px solid #00c853; font-family: 'Courier New', monospace; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE SEGURANÇA E INSTÂNCIAS ---
if 'GROQ_API_KEY' not in st.secrets:
    st.error("Erro Crítico: GROQ_API_KEY não encontrada nos secrets.")
    st.stop()

# Inicializamos o objeto 'hidra' aqui, no escopo global, para evitar o erro de NameError
try:
    hidra = NexusOrchestrator(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Erro ao inicializar o Orquestrador da Hidra: {e}")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Operações")
    modo = st.selectbox("🎯 Neural Target", ["Recon & Strike", "Consenso da Hidra", "Arquitetura & Dev"])
    st.divider()
    st.info("Nexus v8.5 Online | Hidra Ready")

# --- UI PRINCIPAL ---
st.title("🐉 Nexus Omnicore v8.5")
st.markdown("<div class='status-box'><b>STATUS:</b> SISTEMA HÍBRIDO ATIVO | <b>MODO:</b> MULTI-AGENTE</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 MISSÃO (STRIKE)", "🧠 CONSENSO DA HIDRA", "📊 TELEMETRIA"])

with tab1:
    st.subheader("Protocolo Strike")
    user_input = st.text_area("Descreva a missão:", height=150)
    if st.button("💀 EXECUTAR STRIKE"):
        st.write("Processando missão tática...")

with tab2:
    st.subheader("Orquestrador Multi-Agente (Hidra de Lerna)")
    comando_global = st.text_input("Defina o objetivo estratégico para as 7 IAs:")
    
    if st.button("⚡ INICIAR CONSENSO GLOBAL"):
        if comando_global:
            with st.spinner("Despertando as 7 cabeças..."):
                try:
                    # Agora 'hidra' está definido globalmente e não causará erro
                    resultado_bruto = hidra.orquestrar(comando_global, "Contexto: Segurança e Engenharia v8.5")
                    
                    st.success("Consenso Global alcançado!")
                    
                    # Exibição organizada
                    blocos = resultado_bruto.split("---")
                    for bloco in blocos:
                        if bloco.strip():
                            st.markdown(bloco)
                            
                except Exception as e:
                    st.error(f"Falha neural no consenso: {e}")
        else:
            st.warning("Defina a missão para a Hidra.")

with tab3:
    st.subheader("Logs de Telemetria")
    st.write("Monitoramento de rede e hardware em tempo real.")

# --- FOOTER ---
st.divider()
st.caption("Nexus Omnicore v8.5 | Sistema Indestrutível")
