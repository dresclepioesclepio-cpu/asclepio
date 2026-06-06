from fastapi import FastAPI
from pydantic import BaseModel

from db import criar_banco, criar_conversa, salvar_mensagem, atualizar_titulo, buscar_paciente
from ai_client import chamar_ia, testar_ia, info_ia
from risk import analisar_risco, alerta_emergencia

app = FastAPI(title="Asclepio IA")


class ChatRequest(BaseModel):
    mensagem: str
    conversa_id: int | None = None
    paciente_id: int | None = None


@app.on_event("startup")
def iniciar():
    criar_banco()


@app.get("/")
def home():
    return {
        "status": "online",
        "app": "Asclepio IA",
        "mensagem": "API funcionando no Render"
    }


@app.get("/status")
def status():
    ok, resposta = testar_ia()
    ia = info_ia()

    return {
        "api": "online",
        "ia_funcionando": ok,
        "resposta_teste": resposta,
        "modelo": ia["modelo"],
        "base_url": ia["base_url"]
    }


@app.post("/chat")
def chat(dados: ChatRequest):
    conversa_id = dados.conversa_id

    if conversa_id is None:
        conversa_id = criar_conversa(dados.paciente_id)
        atualizar_titulo(conversa_id, dados.mensagem)

    salvar_mensagem(conversa_id, "usuario", dados.mensagem)

    analise = analisar_risco(dados.mensagem)
    alerta = alerta_emergencia(analise)

    if alerta:
        salvar_mensagem(conversa_id, "asclepio", alerta)
        return {
            "conversa_id": conversa_id,
            "risco": analise,
            "resposta": alerta
        }

    paciente = buscar_paciente(dados.paciente_id)
    resposta = chamar_ia(conversa_id, dados.mensagem, paciente)

    salvar_mensagem(conversa_id, "asclepio", resposta)

    return {
        "conversa_id": conversa_id,
        "risco": analise,
        "resposta": resposta
    }
