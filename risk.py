# -*- coding: utf-8 -*-

import unicodedata


def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto


SINTOMAS = {
    "dor no peito": {
        "pontos": 4,
        "emergencia": False,
        "termos": [
            "dor no peito", "aperto no peito", "pressao no peito",
            "peito doendo", "dor toracica", "dor no torax"
        ]
    },
    "falta de ar": {
        "pontos": 4,
        "emergencia": False,
        "termos": [
            "falta de ar", "nao consigo respirar", "dificuldade para respirar",
            "respiracao curta", "sem ar", "muita falta de ar"
        ]
    },
    "desmaio": {
        "pontos": 5,
        "emergencia": True,
        "termos": [
            "desmaio", "desmaiei", "apagao", "apaguei",
            "perdi a consciencia", "cai desmaiado"
        ]
    },
    "confusão mental": {
        "pontos": 5,
        "emergencia": True,
        "termos": [
            "confusao mental", "muito confuso", "nao reconhece",
            "desorientado", "fora de si", "delirando"
        ]
    },
    "convulsão": {
        "pontos": 5,
        "emergencia": True,
        "termos": [
            "convulsao", "convulsionou", "crise convulsiva",
            "ataque epileptico", "teve crise"
        ]
    },
    "sangramento intenso": {
        "pontos": 5,
        "emergencia": True,
        "termos": [
            "sangramento intenso", "muito sangue", "nao para de sangrar",
            "sangrando muito", "hemorragia"
        ]
    },
    "sinal neurológico importante": {
        "pontos": 5,
        "emergencia": True,
        "termos": [
            "fala enrolada", "fraqueza de um lado", "rosto torto",
            "boca torta", "nao consegue falar", "perdeu forca de um lado"
        ]
    },
    "febre alta": {
        "pontos": 2,
        "emergencia": False,
        "termos": [
            "febre alta", "febre muito alta", "39 graus", "40 graus",
            "temperatura alta"
        ]
    },
    "vômitos persistentes": {
        "pontos": 2,
        "emergencia": False,
        "termos": [
            "vomitando muito", "vomitos persistentes", "vomito sem parar",
            "nao paro de vomitar", "vomitando varias vezes"
        ]
    },
    "piora rápida": {
        "pontos": 2,
        "emergencia": False,
        "termos": [
            "piorando rapido", "piora rapida", "piorou de repente",
            "esta piorando", "ficou muito pior"
        ]
    },
    "risco de autoagressão": {
        "pontos": 6,
        "emergencia": True,
        "termos": [
            "me matar", "quero morrer", "tirar minha vida",
            "suicidio", "autoagressao", "me machucar"
        ]
    }
}


def analisar_risco(texto):
    texto_normalizado = normalizar(texto)

    pontos = 0
    sinais = []
    emergencia = False

    for nome_sintoma, regra in SINTOMAS.items():
        encontrou = any(termo in texto_normalizado for termo in regra["termos"])

        if encontrou and nome_sintoma not in sinais:
            sinais.append(nome_sintoma)
            pontos += regra["pontos"]

            if regra["emergencia"]:
                emergencia = True

    if "dor no peito" in sinais and "falta de ar" in sinais:
        emergencia = True

    if emergencia:
        risco = "EMERGÊNCIA"
    elif pontos >= 7:
        risco = "ALTO"
    elif pontos >= 3:
        risco = "MÉDIO"
    else:
        risco = "BAIXO"

    return {
        "risco": risco,
        "pontos": pontos,
        "sinais": sinais
    }


def orientacao_por_risco(risco):
    if risco == "EMERGÊNCIA":
        return (
            "Procure atendimento imediatamente. No Brasil, em emergência, ligue 192 "
            "ou vá ao pronto atendimento mais próximo."
        )

    if risco == "ALTO":
        return (
            "Procure pronto atendimento o quanto antes. Se houver piora, falta de ar, "
            "desmaio, dor no peito ou confusão mental, trate como emergência."
        )

    if risco == "MÉDIO":
        return (
            "Procure uma unidade de saúde ou consulta médica em breve, especialmente "
            "se os sintomas persistirem ou piorarem."
        )

    return (
        "Observe a evolução dos sintomas, mantenha cuidados básicos e procure atendimento "
        "se piorar ou aparecer algum sinal de alerta."
    )


def alerta_emergencia(analise):
    if analise["risco"] != "EMERGÊNCIA":
        return None

    sinais_texto = ", ".join(analise["sinais"]) if analise["sinais"] else "sinais de alerta"

    if "risco de autoagressão" in analise["sinais"]:
        return f"""
ALERTA DE SEGURANÇA

Você relatou possível risco de autoagressão: {sinais_texto}.

Procure ajuda agora: chame alguém de confiança para ficar com você.
No Brasil, você pode ligar para o CVV 188. Se houver perigo imediato, ligue 192 ou procure emergência.
"""

    return f"""
ALERTA DE SEGURANÇA

Pelo que você descreveu, apareceu possível sinal de risco importante:
{sinais_texto}

Eu não consigo confirmar diagnóstico por aqui, mas a orientação mais segura é procurar atendimento imediatamente.

Se você estiver no Brasil e for emergência, ligue para o SAMU 192 ou vá ao pronto atendimento mais próximo.
"""
