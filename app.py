"""
=============================================================================
🛡️ NEXUS OMNICORE v9.0 - HYDRA ORCHESTRATOR ENGINE (THE ECLIPSE)
=============================================================================
Cérebro Multi-Agente Híbrido Coerente de 7 Perspectivas Globais.
Integração e Sincronismo entre Llama 3.3, Gemini Pro, GPT-4 e Claude.
=============================================================================
"""

import concurrent.futures
import time
from groq import Groq
import google.generativeai as genai

class NexusOrchestrator:
    def __init__(self, groq_key, gemini_key):
        self.groq_key = groq_key
        self.gemini_key = gemini_key

    def _chamar_especialista(self, perfil, system_prompt, user_prompt, contexto):
        """Dispara chamadas individuais com roteamento resiliente (Self-Healing)."""
        prompt_completo = (
            f"Você é o {perfil} integrante do Consenso da Hidra.\n"
            f"DIRETRIZ DA MISSÃO: {user_prompt}\n"
            f"CONTEXTO OPERACIONAL:\n{contexto}"
        )
        
        # Tentativa 1: Groq Llama 3.3 (Velocidade e Precisão)
        if self.groq_key:
            try:
                client = Groq(api_key=self.groq_key)
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt_completo}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.15
                )
                return completion.choices[0].message.content
            except Exception as e:
                # Fallback Automático: Gemini Pro se o Groq falhar ou der 429
                if "429" in str(e) or "limit" in str(e).lower():
                    time.sleep(1) # Delay tático de prevenção
                pass

        # Tentativa 2: Gemini Pro 1.5 (Profundidade Cognitiva)
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                response = model.generate_content(f"{system_prompt}\n\n{prompt_completo}")
                return response.text
            except Exception:
                pass

        return f"[{perfil}]: Falha na sincronização do canal neural da Hidra."

    def orquestrar(self, comando, contexto):
        """Ativa simultaneamente as 7 perspectivas inteligentes da Hidra de Lerna."""
        agentes = {
            "Agent CTO (Arquiteto)": (
                "Aja como CTO Global e Arquiteto de Software Elite. "
                "Sua missão é desenhar a arquitetura, estrutura de arquivos, modelagem de dados e design patterns."
            ),
            "Agent Frontend (v0/Tailwind)": (
                "Aja como Engenheiro Frontend Elite (especialista em v0, Tailwind, React e interfaces soberbas). "
                "Gere códigos visuais incríveis, interativos, responsivos e no esquadro perfeito."
            ),
            "Agent Backend (FastAPI)": (
                "Aja como Engenheiro Backend Sênior (Python, FastAPI, Node.js). "
                "Escreva códigos de APIs seguros, rápidos, com rotas limpas e tratamento de exceções robusto."
            ),
            "Agent Database (SQL/NoSQL)": (
                "Aja como DBA Sênior (PostgreSQL, Supabase, SQLite). "
                "Crie esquemas eficientes, migrações otimizadas e queries de alta performance."
            ),
            "Agent Security (Red Team)": (
                "Aja como Analista Forense e Engenheiro Red Team. "
                "Ataque a arquitetura, procure vazamentos de memória, falhas OWASP, vulnerabilidades e riscos."
            ),
            "Agent QA (AutoFix Debugger)": (
                "Aja como Engenheiro de QA e Auto-Debugger Autônomo. "
                "Valide a coerência do código, escreva testes unitários em Playwright/Pytest e aponte correções."
            ),
            "Agent DevOps (Deploy)": (
                "Aja como Engenheiro DevOps (Docker, Kubernetes, Vercel, Railway). "
                "Gere scripts de CI/CD, configurações de containers e estratégias de deploy automático."
            )
        }

        resultados = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            futuros = {
                executor.submit(self._chamar_especialista, perfil, sys, comando, contexto): perfil 
                for perfil, sys in agentes.items()
            }
            for futuro in concurrent.futures.as_completed(futuros):
                perfil = futuros[futuro]
                try:
                    resultado_agente = futuro.result()
                    resultados.append(f"### 🧠 {perfil}\n{resultado_agente}")
                except Exception as e:
                    resultados.append(f"### ⚠️ {perfil}\nFalha de comunicação neural: {str(e)}")

        return "\n\n---\n\n".join(resultados)
