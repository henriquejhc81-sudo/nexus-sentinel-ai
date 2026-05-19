import streamlit as st
import openai
import google.generativeai as genai
import anthropic

# Configuração da página visual
st.set_page_config(page_title="Analisador de IAs", layout="wide")
st.title("🤖 Central Multiversal de IAs & Analisador Personalizado")
st.write("Insira sua pergunta abaixo para enviar às principais IAs do mercado e receber uma análise corrigida.")

# Área lateral para colocar as chaves de API com segurança
st.sidebar.header("🔑 Configuração das Chaves de API")
openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
gemini_key = st.sidebar.text_input("Gemini API Key", type="password")
claude_key = st.sidebar.text_input("Claude API Key", type="password")

# Campo de texto para o usuário fazer a pergunta
pergunta_usuario = st.text_area("✍️ Digite aqui a sua pergunta ou o problema que quer resolver:", height=100)

# Botão para iniciar o processo
if st.button("🚀 Enviar e Analisar Respostas"):
    if not (openai_key and gemini_key and claude_key):
        st.error("Por favor, preencha todas as chaves de API na barra lateral antes de continuar.")
    elif not pergunta_usuario:
        st.warning("Por favor, digite uma pergunta.")
    else:
        # Criando três colunas na tela para mostrar o que cada IA respondeu
        col1, col2, col3 = st.columns(3)
        
        resposta_openai = ""
        resposta_gemini = ""
        resposta_claude = ""

        # --- 1. Chamando a OpenAI ---
        with col1:
            st.subheader("🟢 ChatGPT (OpenAI)")
            with st.spinner("Aguardando ChatGPT..."):
                try:
                    client_oa = openai.OpenAI(api_key=openai_key)
                    completion = client_oa.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": pergunta_usuario}]
                    )
                    resposta_openai = completion.choices[0].message.content
                    st.success("Respondido!")
                    st.write(resposta_openai)
                except Exception as e:
                    resposta_openai = f"Erro ao chamar OpenAI: {e}"
                    st.error(resposta_openai)

        # --- 2. Chamando o Google Gemini ---
        with col2:
            st.subheader("🔵 Gemini (Google)")
            with st.spinner("Aguardando Gemini..."):
                try:
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(pergunta_usuario)
                    resposta_gemini = response.text
                    st.success("Respondido!")
                    st.write(resposta_gemini)
                except Exception as e:
                    resposta_gemini = f"Erro ao chamar Gemini: {e}"
                    st.error(resposta_gemini)

        # --- 3. Chamando o Anthropic Claude ---
        with col3:
            st.subheader("🟠 Claude (Anthropic)")
            with st.spinner("Aguardando Claude..."):
                try:
                    client_ant = anthropic.Anthropic(api_key=claude_key)
                    message = client_ant.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=1000,
                        messages=[{"role": "user", "content": pergunta_usuario}]
                    )
                    resposta_claude = message.content[0].text
                    st.success("Respondido!")
                    st.write(resposta_claude)
                except Exception as e:
                    resposta_claude = f"Erro ao chamar Claude: {e}"
                    st.error(resposta_claude)

        # --- 4. IA Personalizada: Analisando e Corrigindo as Respostas ---
        st.divider()
        st.header("🧠 Sua IA Personalizada (Análise Consolidada)")
        
        with st.spinner("Analisando contradições, erros e gerando sua resposta perfeita..."):
            try:
                # Criamos um comando especial (Prompt) dizendo para a IA agir como seu tutor pessoal
                prompt_analise = f"""
                Você é a IA personalizada do usuário. O usuário fez a seguinte pergunta: "{pergunta_usuario}"
                
                Abaixo estão as respostas que três IAs diferentes deram:
                
                --- RESPOSTA CHATGPT ---
                {resposta_openai}
                
                --- RESPOSTA GEMINI ---
                {resposta_gemini}
                
                --- RESPOSTA CLAUDE ---
                {resposta_claude}
                
                Sua tarefa:
                1. Analise se alguma das IAs cometeu erros, alucinações ou se contradisseram.
                2. Junte os melhores pontos de cada resposta.
                3. Entregue uma resposta final corrigida, ideal, sem erros, formatada de maneira limpa para o usuário.
                """
                
                # Usamos a OpenAI como o cérebro que analisa as outras
                client_oa = openai.OpenAI(api_key=openai_key)
                analise_final = client_oa.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt_analise}]
                )
                
                st.info("Aqui está o veredito final da sua IA Personalizada:")
                st.write(analise_final.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Não foi possível gerar a análise final: {e}")
