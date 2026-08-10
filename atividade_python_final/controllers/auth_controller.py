from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from banco import buscar_usuario_por_email, conferir_senha, criar_usuario

auth_bp = Blueprint("auth", __name__)


def login_obrigatorio(funcao):
    @wraps(funcao)
    def envolvida(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login para acessar esta página.", "danger")
            return redirect(url_for("auth.login"))
        return funcao(*args, **kwargs)

    return envolvida


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        usuario = buscar_usuario_por_email(email)
        if not usuario or not conferir_senha(usuario, senha):
            flash("Email ou senha incorretos.", "danger")
            return render_template("login.html", email=email)
        session["usuario_id"] = usuario["id"]
        session["usuario_nome"] = usuario["nome"]
        flash(f"Bem-vindo(a), {usuario['nome']}!", "success")
        return redirect(url_for("tarefas.dashboard"))
    return render_template("login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        if not nome or not email or len(senha) < 4:
            flash("Preencha todos os campos e use uma senha com pelo menos 4 caracteres.", "danger")
            return render_template("registro.html", nome=nome, email=email)
        if buscar_usuario_por_email(email):
            flash("Este email já está cadastrado.", "danger")
            return render_template("registro.html", nome=nome, email=email)
        criar_usuario(nome, email, senha)
        flash("Cadastro realizado! Faça login para continuar.", "success")
        return redirect(url_for("auth.login"))
    return render_template("registro.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("auth.login"))
