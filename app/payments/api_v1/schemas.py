from datetime import datetime
from typing import Union

from marshmallow import fields
from marshmallow.exceptions import ValidationError
from marshmallow.validate import Range

from app.ext import ma
from app.payments.api_v1.error_messages import date_error_messages
from app.payments.constants import MAX_PAYMENT_AMOUNT, MIN_PAYMENT_AMOUNT


class PaymentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    lessee_id = fields.Integer(required=True)
    property_code = fields.String(required=True)
    paid_value = fields.Integer(
        required=True,
        validate=Range(
            min=MIN_PAYMENT_AMOUNT,
            max=MAX_PAYMENT_AMOUNT
        )
    )
    payment_date = fields.Date(
        required=True,
        format="%d/%m/%Y",
        validate=lambda x: check_odd_days(date=x),
        error_messages={
            "format": date_error_messages['invalid_format'],
            "invalid": date_error_messages['invalid_format']
        }
    )


def check_odd_number(
    *,
    number: int
) -> bool:
    if number % 2 == 0:
        return False
    return True


def check_odd_days(
    *,
    date: datetime
) -> Union[None, ValidationError]:
    if check_odd_number(number=date.day):
        raise ValidationError(date_error_messages['only_odd_days'])
    return
