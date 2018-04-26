import os
# You need to have a database called smartexchange inside your local MongoDB
MONGOALCHEMY_DATABASE = 'smartexchange'
MONGOALCHEMY_CONNECTION_STRING = os.environ.get('DATABASE_URL', 'mongodb://localhost:27017/smartexchange')

SALT = b'$2b$12$WDSY0pVdH/OP7RuzGJouBe'