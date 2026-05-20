import concurrent.futures
from groq import Groq
import streamlit as st

class NexusOrchestrator:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def _cabeça_ia(self, perfil, comando, contexto):
        """Execução individual de uma cabeça da Hidra."""
        prompt = f"""
        Você é {perfil}. Sua missão é atuar como um agente especialista no Nexus Omnicore.
        Tarefa: {comando}
        Contexto Técnico: {contexto}
        Responda com precisão, segurança e foco em performance.
        """
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.2
            )
            return f"### 🧠 {perfil}\n{response.choices[0].message.content}"
        except Exception as e:
            return f"### ⚠️ {perfil}\nErro no processamento: {str(e)}"

    def orquestrar(self, comando, contexto):
        """Dispara as 7 perspectivas simultâneas."""
        perfis = [
            "Arquiteto de Software Sênior",
            "Engenheiro de Red Team (Segurança)",
            "Engenheiro de Blue Team (Defesa)",
            "Especialista em Performance",
            "Engenheiro de Compliance (LGPD)",
            "Documentador Técnico",
            "Juiz Final (Consenso Estratégico)"
        ]
        
        resultados = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            futuros = [executor.submit(self._cabeça_ia, p, comando, contexto) for p in perfis]
            for future in concurrent.futures.as_completed(futuros):
                resultados.append(future.result())
        
        return "\n\n---\n\n".join(resultados)
