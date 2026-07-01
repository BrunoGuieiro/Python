from . import db
from .base import ModeloBase


class OfertaTroca(ModeloBase):
    __tablename__ = "ofertas_troca"

    # TODO ALUNO: FK colecionador_id → colecionadores.id
    colecionador_id = db.Column(
        db.Integer, db.ForeignKey("colecionadores.id"), nullable=False
    )
    observacao = db.Column(db.String(255), nullable=True)

    # TODO ALUNO: relationship colecionador, itens
    colecionador = db.relationship("Colecionador", back_populates="ofertas")
    itens = db.relationship("ItemOferta", back_populates="oferta")

    @classmethod
    def listar_com_colecionador(cls):
        return cls.query.order_by(cls.data_criacao.desc()).all()


class ItemOferta(ModeloBase):
    __tablename__ = "itens_oferta"

    # TODO ALUNO: FK oferta_id, FK figurinha_id
    oferta_id = db.Column(
        db.Integer, db.ForeignKey("ofertas_troca.id"), nullable=False
    )
    figurinha_id = db.Column(
        db.Integer, db.ForeignKey("figurinhas.id"), nullable=False
    )
    tipo = db.Column(db.String(20), nullable=False)  # "oferece" ou "deseja"
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    # TODO ALUNO: relationship oferta, figurinha
    oferta = db.relationship("OfertaTroca", back_populates="itens")
    figurinha = db.relationship("Figurinha")
