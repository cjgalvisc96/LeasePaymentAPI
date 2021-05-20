from app.db import BaseModelMixin, db


class Payment(db.Model, BaseModelMixin):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    lessee_id = db.Column(
        db.Integer,
        unique=True
    )
    property_code = db.Column(
        db.String(20),
        unique=True
    )
    paid_value = db.Column(db.Integer)
    payment_date = db.Column(db.Date)

    def __init__(
        self,
        lessee_id,
        property_code,
        paid_value,
        payment_date
    ):
        self.lessee_id = lessee_id
        self.property_code = property_code
        self.paid_value = paid_value
        self.payment_date = payment_date

    def __repr__(self):
        return f'Payment({self.lessee_id}, {self.property_code})'

    def __str__(self):
        return f'{self.lessee_id}, {self.property_code}'
