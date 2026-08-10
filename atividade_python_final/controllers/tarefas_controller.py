from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from banco import (
    atualizar_tarefa,
    buscar_tarefa_por_id,
    contar_tarefas_por_status,
    criar_tarefa,
    listar_tarefas,
    marcar_concluida,
    remover_tarefa,
)
from controllers.auth_controller import login_obrigatorio
from services.conselho import buscar_frase

tarefas_bp = Blueprint("tarefas", __name__)

STATUS_VALIDOS = ["Pendente", "Em andamento", "Concluída"]

CORES_STATUS = {
    "Pendente": "status-pendente",
    "Em andamento": "status-andamento",
    "Concluída": "status-concluida",
}

BADGES_STATUS = {
    "Pendente": "badge-pendente",
    "Em andamento": "badge-andamento",
    "Concluída": "badge-concluida",
}


@tarefas_bp.route("/dashboard")
@login_obrigatorio
def dashboard():
    usuario_id = session["usuario_id"]
    tarefas = listar_tarefas(usuario_id)
    contagem = contar_tarefas_por_status(usuario_id)
    frase = buscar_frase()
    return render_template(
        "dashboard.html",
        tarefas=tarefas,
        contagem=contagem,
        frase=frase,
        status_validos=STATUS_VALIDOS,
        cores_status=CORES_STATUS,
        badges_status=BADGES_STATUS,
    )


@tarefas_bp.route("/nova_tarefa", methods=["GET", "POST"])
@login_obrigatorio
def nova_tarefa():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "Pendente")
        if status not in STATUS_VALIDOS:
            status = "Pendente"
        if not titulo:
            flash("O título da tarefa é obrigatório.", "danger")
            return render_template("formulario_tarefa.html", tarefa=None, status_validos=STATUS_VALIDOS)
        criar_tarefa(titulo, descricao, status, session["usuario_id"])
        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for("tarefas.dashboard"))
    return render_template("formulario_tarefa.html", tarefa=None, status_validos=STATUS_VALIDOS)


@tarefas_bp.route("/editar/<int:tarefa_id>", methods=["GET", "POST"])
@login_obrigatorio
def editar(tarefa_id):
    tarefa = buscar_tarefa_por_id(tarefa_id)
    if not tarefa or tarefa["usuario_id"] != session["usuario_id"]:
        flash("Tarefa não encontrada.", "danger")
        return redirect(url_for("tarefas.dashboard"))
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", tarefa["status"])
        if status not in STATUS_VALIDOS:
            status = tarefa["status"]
        if not titulo:
            flash("O título da tarefa é obrigatório.", "danger")
            return render_template("formulario_tarefa.html", tarefa=tarefa, status_validos=STATUS_VALIDOS)
        atualizar_tarefa(tarefa_id, titulo, descricao, status)
        flash("Tarefa atualizada com sucesso!", "success")
        return redirect(url_for("tarefas.dashboard"))
    return render_template("formulario_tarefa.html", tarefa=tarefa, status_validos=STATUS_VALIDOS)


@tarefas_bp.route("/excluir/<int:tarefa_id>", methods=["POST"])
@login_obrigatorio
def excluir(tarefa_id):
    tarefa = buscar_tarefa_por_id(tarefa_id)
    if tarefa and tarefa["usuario_id"] == session["usuario_id"]:
        remover_tarefa(tarefa_id)
        flash("Tarefa excluída.", "success")
    else:
        flash("Tarefa não encontrada.", "danger")
    return redirect(url_for("tarefas.dashboard"))


@tarefas_bp.route("/concluir/<int:tarefa_id>", methods=["POST"])
@login_obrigatorio
def concluir(tarefa_id):
    tarefa = buscar_tarefa_por_id(tarefa_id)
    if tarefa and tarefa["usuario_id"] == session["usuario_id"]:
        marcar_concluida(tarefa_id)
        flash("Tarefa concluída!", "success")
    return redirect(url_for("tarefas.dashboard"))
