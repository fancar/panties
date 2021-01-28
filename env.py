import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')


URL1 = os.getenv('URL1')
URL2 = os.getenv('URL2')
AUTH1 = os.getenv('AUTH1')
AUTH2 = os.getenv('AUTH2')

if AUTH1 is None: AUTH1 = ""
if AUTH2 is None: AUTH2 = ""

REQUEST_TIME = int(os.getenv('REQUEST_TIME'))
