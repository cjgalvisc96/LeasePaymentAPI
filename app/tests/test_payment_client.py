import unittest
from faker import Faker
from app.payments.models import Payment
from app.tests import BaseTestClass
from datetime import datetime
from app.payments.constants import (
    MAX_PAYMENT_AMOUT,
    MIN_PAYMENT_AMOUT
)
from app.payments.api_v1.constants import (
    API_URL,
    STATUS_BAD_REQUEST,
    STATUS_GOOD_RESPONSE
)
from app.payments.api_v1.error_messages import (
    payment_error_messages,
    date_error_messages
)
from app.payments.api_v1.success_messages import (
    rent_success_messages
)
fake = Faker()


class BlogClientTestCase(BaseTestClass):

    def test_get_payments(self):
        numbers_of_payments = 5
        with self.app.app_context():
            for _ in range(numbers_of_payments):
                payment = Payment(
                    documentoIdentificacionArrendatario=(
                        fake.unique.random_number(digits=5)
                    ),
                    codigoInmueble=fake.ssn(),
                    valorPagado=fake.random_int(
                        min=MIN_PAYMENT_AMOUT,
                        max=MAX_PAYMENT_AMOUT
                    ),
                    fechaPago=datetime.now()
                )
                payment.save()
        res = self.client.get(API_URL)
        self.assertEqual(numbers_of_payments, len(res.json))
        self.assertEqual(STATUS_GOOD_RESPONSE, res.status_code)

    def test_create_payment_with_invalid_date_format(self):
        json_ = dict(
            documentoIdentificacionArrendatario=(
                str(fake.unique.random_number(digits=5))
            ),
            codigoInmueble=str(fake.ssn()),
            valorPagado=str(fake.random_int(
                min=MIN_PAYMENT_AMOUT,
                max=MAX_PAYMENT_AMOUT
            )),
            fechaPago='25/06-1990'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_BAD_REQUEST, res.status_code)
        self.assertEqual(
            response['resultado']['fechaPago'][0],
            date_error_messages['invalid_format']
        )

    def test_create_payment_with_invalid_lessee_id(self):
        json_ = dict(
            documentoIdentificacionArrendatario=str(fake.ssn()),
            codigoInmueble=str(fake.ssn()),
            valorPagado=str(fake.random_int(
                min=MIN_PAYMENT_AMOUT,
                max=MAX_PAYMENT_AMOUT
            )),
            fechaPago='25/06/1990'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_BAD_REQUEST, res.status_code)
        self.assertIsInstance(
            response['resultado']['documentoIdentificacionArrendatario'], list
        )

    def test_create_payment_with_odd_payment_date(self):
        json_ = dict(
            documentoIdentificacionArrendatario=(
                str(fake.unique.random_number(digits=5))
            ),
            codigoInmueble=str(fake.ssn()),
            valorPagado=str(fake.random_int(
                min=MIN_PAYMENT_AMOUT,
                max=MAX_PAYMENT_AMOUT
            )),
            fechaPago='25/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_BAD_REQUEST, res.status_code)
        self.assertEqual(
            response['resultado']['fechaPago'][0],
            date_error_messages['only_odd_days']
        )

    def test_create_payment_with_invalid_valorPagado(self):
        json_ = dict(
            documentoIdentificacionArrendatario=(
                str(fake.unique.random_number(digits=5))
            ),
            codigoInmueble=str(fake.ssn()),
            valorPagado=str(MAX_PAYMENT_AMOUT + fake.random_int(min=10)),
            fechaPago='26/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_BAD_REQUEST, res.status_code)
        self.assertIsInstance(response['resultado']['valorPagado'], list)

    def test_create_payment_with_exists_codigoInmueble(self):
        property_code = str(fake.ssn())
        with self.app.app_context():
            payment = Payment(
                documentoIdentificacionArrendatario=(
                    str(fake.unique.random_number(digits=5))
                ),
                codigoInmueble=property_code,
                valorPagado=fake.random_int(
                    min=MIN_PAYMENT_AMOUT,
                    max=MAX_PAYMENT_AMOUT
                ),
                fechaPago=datetime.now()
            )
            payment.save()
        lessee_id = str(fake.unique.random_number(digits=6))
        json_ = dict(
            documentoIdentificacionArrendatario=lessee_id,
            codigoInmueble=property_code,
            valorPagado=fake.random_int(min=10),
            fechaPago='26/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_BAD_REQUEST, res.status_code)
        self.assertEqual(
            response['resultado'][0],
            payment_error_messages['integrity_db_error'].format(
                property_code,
                lessee_id
            )
        )

    def test_create_one_total_payment_initial(self):
        json_ = dict(
            documentoIdentificacionArrendatario=(
                str(fake.unique.random_number(digits=5))
            ),
            codigoInmueble=str(fake.ssn()),
            valorPagado=str(MAX_PAYMENT_AMOUT),
            fechaPago='26/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_GOOD_RESPONSE, res.status_code)
        self.assertEqual(
            response['resultado'],
            rent_success_messages['total_rent_payment']
        )

    def test_create_payment_with_parcial_payment(self):
        parcial_payment = fake.unique.random_int(min=5, max=100)
        json_ = dict(
            documentoIdentificacionArrendatario=(
                str(fake.unique.random_number(digits=5))
            ),
            codigoInmueble=str(fake.ssn()),
            valorPagado=str(parcial_payment),
            fechaPago='26/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_GOOD_RESPONSE, res.status_code)
        self.assertEqual(
            response['resultado'],
            rent_success_messages['parcial_rent_payment'].format(
                MAX_PAYMENT_AMOUT - parcial_payment
            )
        )

    def test_create_double_payment(self):
        lessee_id = str(fake.unique.random_number(digits=5))
        property_code = str(fake.ssn())
        first_payment = 300000
        with self.app.app_context():
            payment = Payment(
                documentoIdentificacionArrendatario=lessee_id,
                codigoInmueble=property_code,
                valorPagado=str(first_payment),
                fechaPago=datetime.now()
            )
            payment.save()

        json_ = dict(
            documentoIdentificacionArrendatario=lessee_id,
            codigoInmueble=property_code,
            valorPagado=str(MAX_PAYMENT_AMOUT - first_payment),
            fechaPago='26/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_GOOD_RESPONSE, res.status_code)
        self.assertEqual(STATUS_GOOD_RESPONSE, res.status_code)
        self.assertEqual(
            response['resultado'],
            rent_success_messages['total_rent_payment']
        )


if __name__ == '__main__':
    unittest.main()
