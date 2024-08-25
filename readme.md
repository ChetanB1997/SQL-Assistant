## Download the sample database and load into pgserver
    https://www.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip

## create .env file
    'OPENAI_API_KEY' ="API key"
    'DATABASE'="postgres",
    'USER'="postgres",
    'PASSWORD'='passsword'

## Create python environment using
    python -m venv <env_name>

## Activate the environment
    ./<env_name>/Scripts/activate

## install requirements
    pip install -r requirements.txt

## Run this command to start app on streamlit
    streamlit run sqlapp.py

