from flask import request, Blueprint
from flask_restful import Api, Resource
from app.payments.models import Payment
from app.payments.services import process_payment
from app.payments.api_v1.schemas import PaymentSchema
from app.payments.api_v1.constants import (
    STATUS_GOOD_RESPONSE,
    STATUS_BAD_REQUEST,
    API_URL
)

payment_v1_0_bp = Blueprint('payments_v1_0_bp', __name__)
api = Api(payment_v1_0_bp)


class PaymentListResource(Resource):
    def get(self):
        payment_qry = Payment.get_all()
        payment_schema = PaymentSchema(
            exclude=('id',),
            many=True
        )
        payments = payment_schema.dump(payment_qry)
        return payments, STATUS_GOOD_RESPONSE

    def post(self):
        data = request.get_json()
        payment_schema = PaymentSchema()
        try:
            payment = payment_schema.load(data)
            response = process_payment(payment=payment)
        except Exception as error:
            return {"resultado": error.messages}, STATUS_BAD_REQUEST
        return {"resultado": response}, STATUS_GOOD_RESPONSE


api.add_resource(
    PaymentListResource,
    API_URL,
    endpoint='payments_list_resource'
)
