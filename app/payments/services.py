from typing import Optional

from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from app.payments.api_v1.error_messages import payment_error_messages
from app.payments.api_v1.success_messages import rent_success_messages
from app.payments.constants import MAX_PAYMENT_AMOUNT
from app.payments.models import Payment
from app.payments.selectors import (
    filter_payment_by_lessee_id_and_property_code
)


def process_payment(
    *,
    payment: dict
) -> str:
    existing_payment = filter_payment_by_lessee_id_and_property_code(
        lessee_id=payment['lessee_id'],
        property_code=payment['property_code']
    )
    if not existing_payment:
        payment_to_save = Payment(
            lessee_id=payment['lessee_id'],
            property_code=payment['property_code'],
            paid_value=payment['paid_value'],
            payment_date=payment['payment_date'],
        )
        try:
            payment_to_save.save()
        except Exception as error:
            error = manage_db_errors(
                payment=payment,
                db_error=error
            )
            raise ValidationError(error)

        if rent_is_paid(paid_value=payment['paid_value']):
            return rent_success_messages['total_rent_payment']

        missing_payment_value = get_missing_payment_value(
            actual_payment_value=payment['paid_value']
        )
        return rent_success_messages['partial_rent_payment'].\
            format(missing_payment_value)

    old_payment_value = existing_payment.paid_value
    new_paid_value = old_payment_value + payment['paid_value']
    if rent_is_paid(paid_value=new_paid_value):
        existing_payment.paid_value = MAX_PAYMENT_AMOUNT
        existing_payment.payment_date = payment['payment_date']
        existing_payment.save()
        return rent_success_messages['total_rent_payment']

    existing_payment.paid_value = new_paid_value
    existing_payment.payment_date = payment['payment_date']
    existing_payment.save()
    missing_payment_value = get_missing_payment_value(
        old_payment_value=old_payment_value,
        actual_payment_value=payment['paid_value']
    )
    return rent_success_messages['partial_rent_payment'].\
        format(missing_payment_value)


def get_missing_payment_value(
    *,
    old_payment_value: Optional[int] = 0,
    actual_payment_value: int
) -> int:
    return abs((old_payment_value + actual_payment_value) - MAX_PAYMENT_AMOUNT)


def rent_is_paid(
    *,
    paid_value: int
) -> bool:
    return paid_value >= MAX_PAYMENT_AMOUNT


def manage_db_errors(
    *,
    payment: dict,
    db_error: Exception
) -> str:
    if isinstance(db_error, IntegrityError):
        return payment_error_messages['integrity_db_error'].\
            format(
                payment['lessee_id'],
                payment['property_code']
            )
    return payment_error_messages['unknown_error']
