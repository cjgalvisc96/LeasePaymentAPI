# pruebaceiba


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

## Unit Tests

1. For run the test (see in app/tests/):

    ```sh
    >>(Env)[DirProject] python -m unittest
    ```
