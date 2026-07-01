from models import Filme, Sala, db


def popular_dados():
    if Filme.query.count() > 0:
        return

    filmes = [
        Filme(titulo="Ultimato", duracao_min=200, classificacao="12"),
        Filme(titulo="Titanic", duracao_min=100, classificacao="L"),
    ]
    salas = [
        Sala(numero=1, capacidade=120),
        Sala(numero=2, capacidade=80),
    ]
    db.session.add_all(filmes + salas)
    db.session.commit()
