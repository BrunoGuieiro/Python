from flask import Blueprint, jsonify, request, session

from banco import buscar_tarefa_por_id, contar_tarefas_por_status, listar_tarefas
from controllers.auth_controller import login_obrigatorio

api_bp = Blueprint("api", __name__, url_prefix="/api")


def tarefa_para_dict(tarefa):
    return {
        "id": tarefa["id"],
        "titulo": tarefa["titulo"],
        "descricao": tarefa["descricao"],
        "status": tarefa["status"],
    }


@api_bp.route("/tarefas", methods=["GET"])
@login_obrigatorio
def listar():
    status = request.args.get("status", "").strip()
    usuario_id = session["usuario_id"]
    tarefas = listar_tarefas(usuario_id, status) if status else listar_tarefas(usuario_id)
    return jsonify([tarefa_para_dict(t) for t in tarefas])


@api_bp.route("/tarefas/<int:tarefa_id>", methods=["GET"])
@login_obrigatorio
def detalhe(tarefa_id):
    tarefa = buscar_tarefa_por_id(tarefa_id)
    if not tarefa or tarefa["usuario_id"] != session["usuario_id"]:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    return jsonify(tarefa_para_dict(tarefa))


@api_bp.route("/estatisticas", methods=["GET"])
@login_obrigatorio
def estatisticas():
    return jsonify(contar_tarefas_por_status(session["usuario_id"]))
