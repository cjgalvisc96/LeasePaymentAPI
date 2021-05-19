from app.db import db, BaseModelMixin


class Payment(db.Model, BaseModelMixin):
    __tablename__ = "pagos"

    id = db.Column(db.Integer, primary_key=True)
    documentoIdentificacionArrendatario = db.Column(db.Integer, unique=True)
    codigoInmueble = db.Column(db.String(20), unique=True)
    valorPagado = db.Column(db.Integer)
    fechaPago = db.Column(db.Date)

    def __init__(
        self,
        documentoIdentificacionArrendatario,
        codigoInmueble,
        valorPagado,
        fechaPago
    ):
        self.documentoIdentificacionArrendatario = \
            documentoIdentificacionArrendatario
        self.codigoInmueble = codigoInmueble
        self.valorPagado = valorPagado
        self.fechaPago = fechaPago

    def __repr__(self):
        return (
            f'Payment({self.documentoIdentificacionArrendatario}, '
            f'{self.codigoInmueble})'
        )

    def __str__(self):
        return (
            f'{self.documentoIdentificacionArrendatario}, '
            f'{self.codigoInmueble}'
        )
