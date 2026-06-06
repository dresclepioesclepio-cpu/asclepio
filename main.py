# -*- coding: utf-8 -*-

from config import DB_PATH
from db import (
    criar_banco,
    criar_conversa,
    criar_paciente,
    buscar_paciente,
    vincular_paciente_conversa,
    salvar_mensagem,
    atualizar_titulo,
    listar_conversas,
    carregar_todas_mensagens
)
from ai_client import chamar_ia, testar_ia, info_ia
from risk import analisar_risco, alerta_emergencia
from reports import gerar_relatorio, salvar_conversa_txt


def cabecalho():
    print()
    print("╭──────────────────────────────────────────────╮")
    print("│                 ASCLEPIO IA                  │")
    print("│        Orientação inicial em saúde           │")
    print("╰──────────────────────────────────────────────╯")
    print()
    print("Converse naturalmente. Eu vou organizar as informações")
    print("e orientar o próximo passo com segurança.")
    print()
    print("Comandos úteis:")
    print("  /paciente    cadastrar paciente")
    print("  /testar_ia   testar conexão com a IA")
    print("  /relatorio   gerar relatório")
    print("  /ajuda       ver todos os comandos")
    print("  /sair        encerrar")
    print()
    print("Aviso: não faço diagnóstico médico e não substituo um profissional.")
    print()

def ajuda():
    print()
    print("╭──────────────────── AJUDA ───────────────────╮")
    print("│ /testar_ia     Testa a API da NVIDIA          │")
    print("│ /paciente      Cadastra dados do paciente     │")
    print("│ /ver_paciente  Mostra o paciente atual        │")
    print("│ /status        Mostra status do sistema       │")
    print("│ /historico     Lista conversas salvas         │")
    print("│ /detalhes ID   Abre uma conversa pelo ID      │")
    print("│ /salvar        Salva a conversa em TXT        │")
    print("│ /relatorio     Gera relatório organizado      │")
    print("│ /limpar        Inicia nova conversa           │")
    print("│ /sair          Fecha o Asclépio               │")
    print("╰──────────────────────────────────────────────╯")
    print()


def cadastrar_paciente_interativo():
    print()
    print("=" * 60)
    print("CADASTRO BÁSICO DO PACIENTE")
    print("=" * 60)

    nome = input("Nome: ").strip()

    while nome == "":
        print("Nome é obrigatório.")
        nome = input("Nome: ").strip()

    idade = input("Idade: ").strip()
    sexo = input("Sexo: ").strip()
    cidade = input("Cidade: ").strip()
    observacoes = input("Observações importantes, alergias ou histórico: ").strip()

    paciente_id = criar_paciente(nome, idade, sexo, cidade, observacoes)

    print(f"Paciente cadastrado com ID {paciente_id}.")
    return paciente_id


def mostrar_paciente(paciente_id):
    paciente = buscar_paciente(paciente_id)

    print()
    print("=" * 60)
    print("PACIENTE ATUAL")
    print("=" * 60)

    if not paciente:
        print("Nenhum paciente vinculado a esta conversa.")
        return

    _, nome, idade, sexo, cidade, observacoes, data_cadastro = paciente

    print(f"ID: {paciente_id}")
    print(f"Nome: {nome}")
    print(f"Idade: {idade}")
    print(f"Sexo: {sexo}")
    print(f"Cidade: {cidade}")
    print(f"Observações: {observacoes}")
    print(f"Cadastro: {data_cadastro}")
    print("=" * 60)


def status(conversa_id, paciente_id):
    mensagens = carregar_todas_mensagens(conversa_id)
    texto = "\n".join([conteudo for _, conteudo, _ in mensagens])
    analise = analisar_risco(texto)
    ia = info_ia()

    print()
    print("=" * 60)
    print("STATUS DO ASCLEPIO V6")
    print("=" * 60)
    print(f"Conversa atual: {conversa_id}")
    print(f"Paciente vinculado: {paciente_id if paciente_id else 'Não'}")
    print(f"Banco: {DB_PATH}")
    print(f"Base URL NVIDIA: {ia['base_url']}")
    print(f"Modelo NVIDIA: {ia['modelo']}")
    print(f"Risco local: {analise['risco']}")
    print(f"Pontuação: {analise['pontos']}")
    print(f"Sinais: {', '.join(analise['sinais']) if analise['sinais'] else 'Nenhum'}")
    print("Use /testar_ia para confirmar se a API respondeu de verdade.")
    print("=" * 60)
    print()


def historico():
    conversas = listar_conversas()

    print()
    print("=" * 72)
    print("HISTÓRICO")
    print("=" * 72)

    if not conversas:
        print("Nenhuma conversa salva.")
        return

    for item in conversas:
        conversa_id, data_inicio, titulo, total, paciente = item
        paciente_texto = paciente if paciente else "sem paciente"
        print(f"{conversa_id} | {data_inicio} | {total} mensagens | {paciente_texto} | {titulo}")

    print("=" * 72)


def detalhes(comando):
    partes = comando.split()

    if len(partes) < 2 or not partes[1].isdigit():
        print("Use assim: /detalhes 1")
        return

    conversa_id = int(partes[1])
    mensagens = carregar_todas_mensagens(conversa_id)

    if not mensagens:
        print("Conversa não encontrada ou sem mensagens.")
        return

    print()
    print("=" * 72)
    print(f"DETALHES DA CONVERSA {conversa_id}")
    print("=" * 72)

    for papel, conteudo, data_hora in mensagens:
        nome = "Usuário" if papel == "usuario" else "Asclépio"
        print(f"[{data_hora}] {nome}: {conteudo}")
        print("-" * 72)


def iniciar():
    criar_banco()

    paciente_id = None
    conversa_id = criar_conversa(paciente_id)
    primeira_mensagem = True

    cabecalho()

    while True:
        mensagem = input("Paciente > ").strip()

        if mensagem == "":
            continue

        comando = mensagem.lower()

        if comando == "/sair":
            print("Asclépio: Encerrando. Cuide-se.")
            break

        if comando == "/ajuda":
            ajuda()
            continue

        if comando == "/testar_ia":
            ok, resposta = testar_ia()
            print()
            print("=" * 60)
            print("TESTE REAL DA IA NVIDIA")
            print("=" * 60)
            print(f"Funcionou: {'Sim' if ok else 'Não'}")
            print(f"Resposta: {resposta}")
            print("=" * 60)
            print()
            continue

        if comando == "/paciente":
            paciente_id = cadastrar_paciente_interativo()
            vincular_paciente_conversa(conversa_id, paciente_id)
            continue

        if comando == "/ver_paciente":
            mostrar_paciente(paciente_id)
            continue

        if comando == "/status":
            status(conversa_id, paciente_id)
            continue

        if comando == "/historico":
            historico()
            continue

        if comando.startswith("/detalhes"):
            detalhes(mensagem)
            continue

        if comando == "/salvar":
            salvar_conversa_txt(conversa_id)
            continue

        if comando == "/relatorio":
            paciente = buscar_paciente(paciente_id)
            gerar_relatorio(conversa_id, paciente)
            continue

        if comando == "/limpar":
            conversa_id = criar_conversa(paciente_id)
            primeira_mensagem = True
            print("Asclépio: Nova conversa iniciada.")
            continue

        salvar_mensagem(conversa_id, "usuario", mensagem)

        if primeira_mensagem:
            atualizar_titulo(conversa_id, mensagem)
            primeira_mensagem = False

        analise_mensagem = analisar_risco(mensagem)
        alerta = alerta_emergencia(analise_mensagem)

        if alerta:
            print()
            print("Asclépio:")
            print(alerta)
            print()
            salvar_mensagem(conversa_id, "asclepio", alerta)

        paciente = buscar_paciente(paciente_id)
        resposta = chamar_ia(conversa_id, mensagem, paciente)

        salvar_mensagem(conversa_id, "asclepio", resposta)

        print()
        print("Asclépio:")
        print(resposta)
        print()


if __name__ == "__main__":
    iniciar()
