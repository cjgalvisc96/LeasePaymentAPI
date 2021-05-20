# Lease Payment API

This is a little api to create partial or full lease payments. 

There are the restrictions over the lease payments:
   1. The format of the "payment_date" must be dd/mm/yyyy.
   2. The field "lessee_id" must be only numeric.
   3. The "property_code" field must be alphanumeric.
   4. The "payment_date "field must always be a valid date and
      existing in the calendar.
   5. The field "paid_value" must be between 1 and 1000000 (1
      million) that is, partial payments are received.
   6. The value of the total monthly rent for all
      tenants is 1,000,000 (1 million).
   7. If the payment is made in full, that is, 1000000 (1 million) the
      response of the operation should be "Thank you for paying
      all your rent”.
   8. If the payment is partial, that is, less than 1,000,000 (1
      million) the response of the operation should be "thank you
      for your subscription, however remember that you need
      pay $ {put the remaining value here} ".
   9. If the payment is made for the remaining value, the answer of
      the operation should be "thank you for paying all your rent".
   10. Payments are only received on odd days of each month.
      say if the value is sent in the field "díaPago"
      "09/02/2020" the answer should be "I'm sorry but payment cannot 
       be received by decree of administration"; In this case, the http code 400 must be returned (bad request)
   11. The unique identifier of each tenant is "lessee_id" and "property_code" 


## Installation

It is recommended that you create a virtual environment (use pyenv like suggestions)

1. Install requirements
    ```sh
    >>(Env)[DirProject] pip install -r requirements.txt
    ```
   
2. Allow .envrc(enviroment vars)
   ```sh
    >>(Env)[DirProject] direnv allow
    ```
   
3. Init db and Migrate migrations (only first time)
    ```sh
    >>(Env)[DirProject] flask db init
    >>(Env)[DirProject] flask db migrate -m "Initial_db"
    >>(Env)[DirProject] flask db upgrade
    ```

4. Run server
    ```sh
    >>(Env)[DirProject] flask run
    ```

### Usage


1. Get all lease payments
    ```sh
    [GET] http://127.0.0.1:8084/api/payments
    ```

    [RESPONSE]
    ```json
    [
       {
           "lessee_id": 1036946620,
           "paid_value": 1000000,
           "property_code": "8879",
           "payment_date": "26/09/2020"
       },
       {
           "lessee_id": 1036946621,
           "paid_value": 800000,
           "property_code": "8874",
           "payment_date": "28/09/2020"
       }
    ]
    ```

2. Create lease payment
    ```sh
    [POST] http://127.0.0.1:8084/api/payments
    ```

    [BODY]
    ```json
    {
       "lessee_id": "1036946621",
       "property_code": "8874",
       "paid_value": "800000",
       "payment_date": "28/09/2020"
     }
    ```
   
   [RESPONSE]
    ```json
    {
       "result": "Thank you for your subscription, however remember that you need to pay 200000"
    }
    ```

## Unit Tests

1. For run the test (see in app/tests/):

    ```sh
    >>(Env)[DirProject] python -m unittest
    ```
