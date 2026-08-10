import os
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

PASTA = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(PASTA, "tarefas.db")


def conectar():
    conn = sqlite3.connect(CAMINHO_BANCO)
    conn.row_factory = sqlite3.Row
    return conn


def iniciar_banco():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'Pendente',
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
        """
    )
    conn.commit()
    conn.close()


def criar_usuario(nome, email, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
        (nome, email, generate_password_hash(senha)),
    )
    conn.commit()
    usuario_id = cursor.lastrowid
    conn.close()
    return usuario_id


def buscar_usuario_por_email(email):
    conn = conectar()
    usuario = conn.execute(
        "SELECT * FROM usuarios WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return usuario


def conferir_senha(usuario, senha):
    return check_password_hash(usuario["senha"], senha)


def listar_tarefas(usuario_id, status=None):
    conn = conectar()
    if status:
        tarefas = conn.execute(
            "SELECT * FROM tarefas WHERE usuario_id = ? AND status = ? ORDER BY id DESC",
            (usuario_id, status),
        ).fetchall()
    else:
        tarefas = conn.execute(
            "SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY id DESC",
            (usuario_id,),
        ).fetchall()
    conn.close()
    return tarefas


def buscar_tarefa_por_id(tarefa_id):
    conn = conectar()
    tarefa = conn.execute(
        "SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)
    ).fetchone()
    conn.close()
    return tarefa


def criar_tarefa(titulo, descricao, status, usuario_id):
    conn = conectar()
    conn.execute(
        "INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)",
        (titulo, descricao, status, usuario_id),
    )
    conn.commit()
    conn.close()


def atualizar_tarefa(tarefa_id, titulo, descricao, status):
    conn = conectar()
    conn.execute(
        "UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ?",
        (titulo, descricao, status, tarefa_id),
    )
    conn.commit()
    conn.close()


def remover_tarefa(tarefa_id):
    conn = conectar()
    conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    conn.commit()
    conn.close()


def marcar_concluida(tarefa_id):
    conn = conectar()
    conn.execute(
        "UPDATE tarefas SET status = 'Concluída' WHERE id = ?", (tarefa_id,)
    )
    conn.commit()
    conn.close()


def contar_tarefas_por_status(usuario_id):
    conn = conectar()
    linhas = conn.execute(
        "SELECT status, COUNT(*) AS total FROM tarefas WHERE usuario_id = ? GROUP BY status",
        (usuario_id,),
    ).fetchall()
    conn.close()
    dados = {"Pendente": 0, "Em andamento": 0, "Concluída": 0}
    for linha in linhas:
        dados[linha["status"]] = linha["total"]
    return dados
