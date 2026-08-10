import os

from flask import Flask, redirect, session, url_for

from banco import iniciar_banco
from controllers import api_bp, auth_bp, tarefas_bp


def criar_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )
    app.config["SECRET_KEY"] = "chave-secreta-tarefas-dev"

    iniciar_banco()
    app.register_blueprint(auth_bp)
    app.register_blueprint(tarefas_bp)
    app.register_blueprint(api_bp)

    @app.route("/")
    def root():
        if "usuario_id" in session:
            return redirect(url_for("tarefas.dashboard"))
        return redirect(url_for("auth.login"))

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
