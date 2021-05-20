from flask import Blueprint, request
from flask_restful import Api, Resource

from app.payments.api_v1.constants import (
    API_URL,
    STATUS_BAD_REQUEST,
    STATUS_GOOD_RESPONSE
)
from app.payments.api_v1.schemas import PaymentSchema
from app.payments.models import Payment
from app.payments.services import process_payment

payment_v1_0_bp = Blueprint('payments_v1_0_bp', __name__)
api = Api(payment_v1_0_bp)


class PaymentListResource(Resource):

    @staticmethod
    def get():
        payment_qry = Payment.get_all()
        payment_schema = PaymentSchema(
            exclude=('id',),
            many=True
        )
        payments = payment_schema.dump(payment_qry)
        return payments, STATUS_GOOD_RESPONSE

    @staticmethod
    def post():
        data = request.get_json()
        payment_schema = PaymentSchema()
        try:
            payment = payment_schema.load(data)
            response = process_payment(payment=payment)
        except Exception as error:
            return {"result": error.messages}, STATUS_BAD_REQUEST

        return {"result": response}, STATUS_GOOD_RESPONSE


api.add_resource(
    PaymentListResource,
    API_URL,
    endpoint='payments_list_resource'
)
