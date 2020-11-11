from flask import Flask
from os import environ
from dotenv import load_dotenv
from os.path import join, dirname

application = Flask(__name__)

# Linux
# dotenv_path = join(dirname(__file__), '..', '.env')

# Windows
dotenv_path = '.env'

load_dotenv(dotenv_path)

# Secret key for form
application.config['SECRET_KEY'] = environ.get('SECRET_KEY')
application.config['BASIC_AUTH_USERNAME'] = environ.get('BASIC_AUTH_USERNAME')
application.config['BASIC_AUTH_PASSWORD'] = environ.get('BASIC_AUTH_PASSWORD')


from newspaper import routes

