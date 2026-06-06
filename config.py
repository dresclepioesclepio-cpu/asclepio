# -*- coding: utf-8 -*-

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import os

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
RELATORIOS_DIR = BASE_DIR / "relatorios"
CONVERSAS_DIR = BASE_DIR / "conversas"

for pasta in [CONFIG_DIR, DATA_DIR, RELATORIOS_DIR, CONVERSAS_DIR]:
    pasta.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "asclepio_v6.db"

load_dotenv(BASE_DIR / ".env")
load_dotenv(CONFIG_DIR / ".env")

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY") or os.getenv("OPENAI_API_KEY")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct")

SYSTEM_PROMPT = """
Você é o Asclépio, um agente conversacional de pré-triagem em saúde.

Objetivo:
- Conversar de forma natural, parecida com o ChatGPT.
- Ajudar o usuário a organizar sintomas.
- Fazer perguntas de continuação.
- Orientar próximos passos com segurança.

Estilo:
- Português do Brasil.
- Linguagem simples, humana e acolhedora.
- Respostas objetivas.
- Faça uma pergunta por vez quando faltar informação.

Regras obrigatórias:
- Não faça diagnóstico médico.
- Não prescreva remédios.
- Não substitua avaliação médica.
- Não diga que a pessoa está bem com certeza.
- Não invente sintomas.
- Se houver sinais graves, oriente atendimento imediato.
- No Brasil, em emergência, oriente ligar 192.
- Em risco de autoagressão, oriente buscar ajuda imediata, chamar alguém de confiança e ligar 188/CVV ou 192 se houver perigo imediato.
"""


def get_client():
    if not NVIDIA_API_KEY:
        return None

    return OpenAI(
        base_url=NVIDIA_BASE_URL,
        api_key=NVIDIA_API_KEY
    )
