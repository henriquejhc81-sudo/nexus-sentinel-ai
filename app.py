        # --- LINHA 82 (Aproximadamente) do app.py ---
        if st.button("⚡ PROCESSAR CONSULTA GENESIS", type="primary"):
            if pergunta:
                with st.spinner("IA Multimodal executando Rastreamento Sentinel..."):
                    orquestrador_inteligencia("Super IA")
                    
                    if arquivo_universal:
                        # Verifica se é vídeo para aplicar rastreamento
                        if arquivo_universal.type in ['video/mp4', 'video/mov', 'video/avi']:
                            # Salva temporariamente para processar
                            with open("temp_video.mp4", "wb") as f:
                                f.write(arquivo_universal.read())
                            
                            analise_mov = rastreamento_movimento_genesis("temp_video.mp4")
                            resultado_ia = motor_multimodal_genesis(arquivo_universal, pergunta)
                            
                            st.success("🎥 Análise de Vídeo Concluída")
                            st.write(f"**Resultado do Rastreamento:** {analise_mov['status']}")
                            st.write(f"**Intensidade Biométrica:** {analise_mov['intensidade_media']}%")
                        else:
                            resultado_ia = motor_multimodal_genesis(arquivo_universal, pergunta)
                    
                        st.info("Resposta da Super IA:")
                        st.write(resultado_ia)
                    else:
                        st.write("Análise conceitual processada. Aguardando mídia para diagnóstico profundo.")
