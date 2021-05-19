from app.payments.models import Payment


def filter_payment_by_leese_id_and_code_property(
    *,
    leese_id: int,
    code_property: str
) -> Payment:
    return Payment.simple_filter(
        documentoIdentificacionArrendatario=leese_id,
        codigoInmueble=code_property
    )
