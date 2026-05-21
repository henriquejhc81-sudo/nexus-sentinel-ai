"""
BLOCO 1: ENGINE NEURAL E ORQUESTRAÇÃO
Este módulo contém a lógica dos 7 especialistas e a gestão de dados.
"""
import streamlit as st
import sqlite3, concurrent.futures
from groq import Groq
import google.generativeai as genai

class NexusOrchestrator:
    def __init__(self, groq_key, gemini_key):
        self.groq_key = groq_key
        self.gemini_key = gemini_key

    def _chamar_especialista(self, perfil, system_prompt, user_prompt, contexto):
        try:
            client = Groq(api_key=self.groq_key)
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}, 
                          {"role": "user", "content": f"MISSÃO: {user_prompt}\nCONTEXTO: {contexto}"}],
                model="llama-3.3-70b-versatile", temperature=0.1
            )
            return completion.choices[0].message.content
        except Exception as e: return f"Erro no especialista {perfil}: {e}"

    def orquestrar(self, comando, contexto):
        agentes = {
            "CTO": "Aja como Arquiteto Sênior.",
            "Frontend": "Aja como Eng. Frontend.",
            "Backend": "Aja como Eng. Backend.",
            "Database": "Aja como DBA.",
            "Security": "Aja como Red Team.",
            "QA": "Aja como QA.",
            "DevOps": "Aja como DevOps."
        }
        resultados = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            futuros = {executor.submit(self._chamar_especialista, p, s, comando, contexto): p for p, s in agentes.items()}
            for f in concurrent.futures.as_completed(futuros):
                resultados.append(f"### 🧠 {futuros[f]}\n{f.result()}")
        return "\n\n---\n\n".join(resultados)
