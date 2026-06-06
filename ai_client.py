# -*- coding: utf-8 -*-

from config import get_client, NVIDIA_MODEL, NVIDIA_BASE_URL, SYSTEM_PROMPT
from db import carregar_mensagens
from risk import analisar_risco


def testar_ia():
    client = get_client()

    if client is None:
        return False, "IA não ativada: chave NVIDIA não encontrada no .env."

    try:
        resposta = client.chat.completions.create(
            model=NVIDIA_MODEL,
            messages=[
                {"role": "system", "content": "Responda em português do Brasil."},
                {"role": "user", "content": "Responda somente: Asclépio NVIDIA ativo."}
            ],
            temperature=0,
            max_tokens=30
        )

        texto = resposta.choices[0].message.content
        return True, texto

    except Exception as erro:
        return False, f"Erro no teste real da IA NVIDIA: {erro}"


def montar_prompt(conversa_id, mensagem_usuario, paciente=None):
    mensagens = carregar_mensagens(conversa_id, limite=24)

    historico = ""

    for papel, conteudo in mensagens:
        nome = "Usuário" if papel == "usuario" else "Asclépio"
        historico += f"{nome}: {conteudo}\n"

    texto_total = historico + "\n" + mensagem_usuario
    analise = analisar_risco(texto_total)

    dados_paciente = "Paciente não cadastrado."

    if paciente:
        _, nome, idade, sexo, cidade, observacoes, _ = paciente
        dados_paciente = f"""
Nome: {nome}
Idade: {idade}
Sexo: {sexo}
Cidade: {cidade}
Observações: {observacoes}
"""

    sinais_texto = ", ".join(analise["sinais"]) if analise["sinais"] else "nenhum sinal grave detectado automaticamente"

    prompt = f"""
Dados do paciente:
{dados_paciente}

Histórico recente:
{historico}

Nova mensagem:
{mensagem_usuario}

Análise local de segurança:
Risco estimado: {analise["risco"]}
Pontuação: {analise["pontos"]}
Sinais encontrados: {sinais_texto}

Responda como Asclépio.
Não faça diagnóstico.
Não prescreva remédio.
Faça pergunta de continuação se faltar informação.
Se houver sinal grave, oriente atendimento imediato.
"""
    return prompt


def chamar_ia(conversa_id, mensagem_usuario, paciente=None):
    client = get_client()

    if client is None:
        return "IA não ativada: chave da NVIDIA não encontrada. Verifique o arquivo .env."

    try:
        resposta = client.chat.completions.create(
            model=NVIDIA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": montar_prompt(conversa_id, mensagem_usuario, paciente)}
            ],
            temperature=0.3,
            max_tokens=900
        )

        return resposta.choices[0].message.content

    except Exception as erro:
        return f"Erro ao chamar a IA NVIDIA: {erro}"


def info_ia():
    return {
        "base_url": NVIDIA_BASE_URL,
        "modelo": NVIDIA_MODEL
    }
