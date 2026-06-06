# -*- coding: utf-8 -*-

from datetime import datetime
from config import RELATORIOS_DIR, CONVERSAS_DIR
from db import carregar_todas_mensagens, salvar_relatorio_banco
from risk import analisar_risco, orientacao_por_risco


def primeira_mensagem_usuario(mensagens):
    for papel, conteudo, _ in mensagens:
        if papel == "usuario":
            return conteudo
    return "Não informado."


def formatar_paciente(paciente):
    if not paciente:
        return """Paciente: não cadastrado
Idade: não informada
Sexo: não informado
Cidade: não informada
Observações: não informadas"""

    _, nome, idade, sexo, cidade, observacoes, data_cadastro = paciente

    return f"""Paciente: {nome}
Idade: {idade or "não informada"}
Sexo: {sexo or "não informado"}
Cidade: {cidade or "não informada"}
Observações: {observacoes or "não informadas"}
Cadastro: {data_cadastro}"""


def salvar_conversa_txt(conversa_id):
    mensagens = carregar_todas_mensagens(conversa_id)

    data = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = CONVERSAS_DIR / f"conversa_{conversa_id}_{data}.txt"

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"CONVERSA ASCLEPIO IA V6 - ID {conversa_id}\n")
        arquivo.write("=" * 70 + "\n\n")

        for papel, conteudo, data_hora in mensagens:
            nome = "Usuário" if papel == "usuario" else "Asclépio"
            arquivo.write(f"[{data_hora}] {nome}:\n{conteudo}\n\n")

    print(f"Conversa salva em: {caminho}")


def gerar_relatorio(conversa_id, paciente=None):
    mensagens = carregar_todas_mensagens(conversa_id)

    texto_total = "\n".join([conteudo for _, conteudo, _ in mensagens])
    analise = analisar_risco(texto_total)

    sinais_texto = ", ".join(analise["sinais"]) if analise["sinais"] else "Nenhum sinal grave detectado automaticamente."
    queixa_principal = primeira_mensagem_usuario(mensagens)
    orientacao = orientacao_por_risco(analise["risco"])

    conversa_formatada = ""

    for papel, conteudo, data_hora in mensagens:
        nome = "Usuário" if papel == "usuario" else "Asclépio"
        conversa_formatada += f"[{data_hora}] {nome}: {conteudo}\n\n"

    relatorio = f"""
============================================================
                 RELATÓRIO ASCLEPIO IA V6
============================================================

Data e hora do relatório: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
ID da conversa: {conversa_id}

1. DADOS DO PACIENTE
{formatar_paciente(paciente)}

2. QUEIXA PRINCIPAL RELATADA
{queixa_principal}

3. ANÁLISE LOCAL DE SEGURANÇA
Risco estimado: {analise["risco"]}
Pontuação local: {analise["pontos"]}
Sinais identificados: {sinais_texto}

4. ORIENTAÇÃO SEGURA
{orientacao}

5. RESUMO PARA LEVAR AO PROFISSIONAL DE SAÚDE
O usuário conversou com o agente Asclépio IA para organizar sintomas e sinais de alerta.
Este documento reúne as informações relatadas na conversa, a análise local de risco e a conversa registrada.

6. AVISO IMPORTANTE
Este relatório não é diagnóstico médico.
Ele não substitui avaliação de um profissional de saúde.
Em caso de emergência no Brasil, ligue 192 ou procure atendimento imediatamente.

7. CONVERSA REGISTRADA
{conversa_formatada}

============================================================
"""

    data = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = RELATORIOS_DIR / f"relatorio_v6_conversa_{conversa_id}_{data}.txt"

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(relatorio)

    salvar_relatorio_banco(conversa_id, analise["risco"], caminho)

    print(f"Relatório salvo em: {caminho}")
