import unittest
from datetime import datetime

from faker import Faker

from app.payments.api_v1.constants import (
    API_URL,
    STATUS_BAD_REQUEST,
    STATUS_GOOD_RESPONSE
)
from app.payments.api_v1.error_messages import (
    date_error_messages,
    payment_error_messages
)
from app.payments.api_v1.success_messages import rent_success_messages
from app.payments.constants import MAX_PAYMENT_AMOUNT, MIN_PAYMENT_AMOUNT
from app.payments.models import Payment
from app.tests import BaseTestClass

fake = Faker()


class BlogClientTestCase(BaseTestClass):

    def test_get_payments(self):
        numbers_of_payments = 5
        with self.app.app_context():
            for _ in range(numbers_of_payments):
                payment = Payment(
                    lessee_id=fake.unique.random_number(digits=5),
                    property_code=fake.ssn(),
                    paid_value=fake.random_int(
                        min=MIN_PAYMENT_AMOUNT,
                        max=MAX_PAYMENT_AMOUNT
                    ),
                    payment_date=datetime.now()
                )
                payment.save()
        res = self.client.get(API_URL)
        self.assertEqual(numbers_of_payments, len(res.json))
        self.assertEqual(STATUS_GOOD_RESPONSE, res.status_code)

    def test_create_payment_with_invalid_date_format(self):
        json_ = dict(
            lessee_id=(
                str(fake.unique.random_number(digits=5))
            ),
            property_code=str(fake.ssn()),
            paid_value=str(fake.random_int(
                min=MIN_PAYMENT_AMOUNT,
                max=MAX_PAYMENT_AMOUNT
            )),
            payment_date='25/06-1990'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_BAD_REQUEST, res.status_code)
        self.assertEqual(
            response['result']['payment_date'][0],
            date_error_messages['invalid_format']
        )

    def test_create_payment_with_invalid_lessee_id(self):
        json_ = dict(
            lessee_id=str(fake.ssn()),
            property_code=str(fake.ssn()),
            paid_value=str(fake.random_int(
                min=MIN_PAYMENT_AMOUNT,
                max=MAX_PAYMENT_AMOUNT
            )),
            payment_date='25/06/1990'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_BAD_REQUEST, res.status_code)
        self.assertIsInstance(
            response['result']['lessee_id'], list
        )

    def test_create_payment_with_odd_payment_date(self):
        json_ = dict(
            lessee_id=(
                str(fake.unique.random_number(digits=5))
            ),
            property_code=str(fake.ssn()),
            paid_value=str(fake.random_int(
                min=MIN_PAYMENT_AMOUNT,
                max=MAX_PAYMENT_AMOUNT
            )),
            payment_date='25/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_BAD_REQUEST, res.status_code)
        self.assertEqual(
            response['result']['payment_date'][0],
            date_error_messages['only_odd_days']
        )

    def test_create_payment_with_invalid_paid_value(self):
        json_ = dict(
            lessee_id=(
                str(fake.unique.random_number(digits=5))
            ),
            property_code=str(fake.ssn()),
            paid_value=str(MAX_PAYMENT_AMOUNT + fake.random_int(min=10)),
            payment_date='26/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_BAD_REQUEST, res.status_code)
        self.assertIsInstance(response['result']['paid_value'], list)

    def test_create_payment_with_exists_property_code(self):
        property_code = str(fake.ssn())
        with self.app.app_context():
            payment = Payment(
                lessee_id=(
                    str(fake.unique.random_number(digits=5))
                ),
                property_code=property_code,
                paid_value=fake.random_int(
                    min=MIN_PAYMENT_AMOUNT,
                    max=MAX_PAYMENT_AMOUNT
                ),
                payment_date=datetime.now()
            )
            payment.save()
        lessee_id = str(fake.unique.random_number(digits=6))
        json_ = dict(
            lessee_id=lessee_id,
            property_code=property_code,
            paid_value=fake.random_int(min=10),
            payment_date='26/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_BAD_REQUEST, res.status_code)
        self.assertEqual(
            response['result'][0],
            payment_error_messages['integrity_db_error'].format(
                property_code,
                lessee_id
            )
        )

    def test_create_one_total_payment_initial(self):
        json_ = dict(
            lessee_id=(
                str(fake.unique.random_number(digits=5))
            ),
            property_code=str(fake.ssn()),
            paid_value=str(MAX_PAYMENT_AMOUNT),
            payment_date='26/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_GOOD_RESPONSE, res.status_code)
        self.assertEqual(
            response['result'],
            rent_success_messages['total_rent_payment']
        )

    def test_create_payment_with_partial_payment(self):
        partial_payment = fake.unique.random_int(min=5, max=100)
        json_ = dict(
            lessee_id=(
                str(fake.unique.random_number(digits=5))
            ),
            property_code=str(fake.ssn()),
            paid_value=str(partial_payment),
            payment_date='26/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_GOOD_RESPONSE, res.status_code)
        self.assertEqual(
            response['result'],
            rent_success_messages['partial_rent_payment'].format(
                MAX_PAYMENT_AMOUNT - partial_payment
            )
        )

    def test_create_double_payment(self):
        lessee_id = str(fake.unique.random_number(digits=5))
        property_code = str(fake.ssn())
        first_payment = 300000
        with self.app.app_context():
            payment = Payment(
                lessee_id=lessee_id,
                property_code=property_code,
                paid_value=str(first_payment),
                payment_date=datetime.now()
            )
            payment.save()

        json_ = dict(
            lessee_id=lessee_id,
            property_code=property_code,
            paid_value=str(MAX_PAYMENT_AMOUNT - first_payment),
            payment_date='26/09/2020'
        )
        res = self.client.post(API_URL, json=json_)
        response = res.json
        self.assertEqual(STATUS_GOOD_RESPONSE, res.status_code)
        self.assertEqual(STATUS_GOOD_RESPONSE, res.status_code)
        self.assertEqual(
            response['result'],
            rent_success_messages['total_rent_payment']
        )


if __name__ == '__main__':
    unittest.main()
