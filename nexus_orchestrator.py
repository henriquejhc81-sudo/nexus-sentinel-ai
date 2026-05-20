import concurrent.futures
from groq import Groq
import os

class NexusOrchestrator:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        
    def _cabeça_ia(self, perfil, comando, contexto):
        prompt = f"Você é {perfil}. Analise a seguinte tarefa com foco máximo:\nTarefa: {comando}\nContexto: {contexto}"
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.2
            )
            return f"[{perfil}]: {response.choices[0].message.content}"
        except Exception as e:
            return f"[{perfil}]: Falha na reconexão (Auto-Healing Ativo)... {str(e)}"

    def orquestrar(self, comando, contexto):
        perfis = [
            "Arquiteto de Software Sênior",
            "Engenheiro de Red Team (Segurança)",
            "Engenheiro de Blue Team (Defesa)",
            "Especialista em Performance",
            "Engenheiro de Segurança (LGPD/Compliance)",
            "Documentador Técnico",
            "Juiz Final (Consenso)"
        ]
        
        resultados = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            # Dispara as 7 cabeças simultaneamente
            futures = [executor.submit(self._cabeça_ia, p, comando, contexto) for p in perfis]
            for future in concurrent.futures.as_completed(futures):
                resultados.append(future.result())
        
        return "\n\n".join(resultados)
