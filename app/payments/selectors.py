from app.payments.models import Payment


def filter_payment_by_lessee_id_and_property_code(
    *,
    lessee_id: int,
    property_code: str
) -> Payment:
    return Payment.simple_filter(
        lessee_id=lessee_id,
        property_code=property_code
    )
