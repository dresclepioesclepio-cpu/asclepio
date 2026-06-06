# -*- coding: utf-8 -*-

from datetime import datetime
import sqlite3
from config import DB_PATH


def conectar():
    return sqlite3.connect(DB_PATH)


def criar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade TEXT,
            sexo TEXT,
            cidade TEXT,
            observacoes TEXT,
            data_cadastro TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_inicio TEXT NOT NULL,
            titulo TEXT NOT NULL,
            paciente_id INTEGER,
            status TEXT NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversa_id INTEGER NOT NULL,
            data_hora TEXT NOT NULL,
            papel TEXT NOT NULL,
            conteudo TEXT NOT NULL,
            FOREIGN KEY (conversa_id) REFERENCES conversas(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relatorios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversa_id INTEGER NOT NULL,
            data_hora TEXT NOT NULL,
            risco TEXT NOT NULL,
            caminho TEXT NOT NULL,
            FOREIGN KEY (conversa_id) REFERENCES conversas(id)
        )
    """)

    conexao.commit()
    conexao.close()


def criar_paciente(nome, idade="", sexo="", cidade="", observacoes=""):
    conexao = conectar()
    cursor = conexao.cursor()

    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    cursor.execute("""
        INSERT INTO pacientes (nome, idade, sexo, cidade, observacoes, data_cadastro)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, idade, sexo, cidade, observacoes, data))

    paciente_id = cursor.lastrowid

    conexao.commit()
    conexao.close()

    return paciente_id


def buscar_paciente(paciente_id):
    if paciente_id is None:
        return None

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, idade, sexo, cidade, observacoes, data_cadastro
        FROM pacientes
        WHERE id = ?
    """, (paciente_id,))

    paciente = cursor.fetchone()
    conexao.close()

    return paciente


def criar_conversa(paciente_id=None):
    conexao = conectar()
    cursor = conexao.cursor()

    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    titulo = f"Conversa {data}"

    cursor.execute("""
        INSERT INTO conversas (data_inicio, titulo, paciente_id, status)
        VALUES (?, ?, ?, ?)
    """, (data, titulo, paciente_id, "ativa"))

    conversa_id = cursor.lastrowid

    conexao.commit()
    conexao.close()

    return conversa_id


def atualizar_titulo(conversa_id, titulo):
    titulo = titulo.strip()

    if len(titulo) > 70:
        titulo = titulo[:70] + "..."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE conversas SET titulo = ? WHERE id = ?",
        (titulo, conversa_id)
    )

    conexao.commit()
    conexao.close()


def vincular_paciente_conversa(conversa_id, paciente_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE conversas SET paciente_id = ? WHERE id = ?",
        (paciente_id, conversa_id)
    )

    conexao.commit()
    conexao.close()


def salvar_mensagem(conversa_id, papel, conteudo):
    conexao = conectar()
    cursor = conexao.cursor()

    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    cursor.execute("""
        INSERT INTO mensagens (conversa_id, data_hora, papel, conteudo)
        VALUES (?, ?, ?, ?)
    """, (conversa_id, data, papel, conteudo))

    conexao.commit()
    conexao.close()


def carregar_mensagens(conversa_id, limite=20):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT papel, conteudo
        FROM mensagens
        WHERE conversa_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (conversa_id, limite))

    mensagens = cursor.fetchall()
    mensagens.reverse()
    conexao.close()

    return mensagens


def carregar_todas_mensagens(conversa_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT papel, conteudo, data_hora
        FROM mensagens
        WHERE conversa_id = ?
        ORDER BY id ASC
    """, (conversa_id,))

    mensagens = cursor.fetchall()
    conexao.close()

    return mensagens


def listar_conversas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT c.id, c.data_inicio, c.titulo, COUNT(m.id), p.nome
        FROM conversas c
        LEFT JOIN mensagens m ON c.id = m.conversa_id
        LEFT JOIN pacientes p ON c.paciente_id = p.id
        GROUP BY c.id
        ORDER BY c.id DESC
        LIMIT 20
    """)

    conversas = cursor.fetchall()
    conexao.close()

    return conversas


def salvar_relatorio_banco(conversa_id, risco, caminho):
    conexao = conectar()
    cursor = conexao.cursor()

    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    cursor.execute("""
        INSERT INTO relatorios (conversa_id, data_hora, risco, caminho)
        VALUES (?, ?, ?, ?)
    """, (conversa_id, data, risco, str(caminho)))

    conexao.commit()
    conexao.close()
