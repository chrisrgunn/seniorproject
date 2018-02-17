import os
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://trinitydev:trinitypass123@localhost/TrinityDB')
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# MONGO_DBNAME = 'app'
# MONGO_URI = 'mongodb://localhost:27017/smartexchange'

MONGOALCHEMY_DATABASE = 'smartexchange'
MONGOALCHEMY_CONNECTION_STRING = 'mongodb://localhost:27017/smartexchange'

# WTF_CSRF_ENABLED = False # This option enables cross-site forgery prevention (makes more secure)
# SECRET_KEY = 'mhprojectsecretpass123' # used to create a cryptographic token used to validate forms, only needed when CSRF enabled,
# # UPLOAD_FOLDER = 'app/static/images'
# UPLOAD_FOLDER = 'static/images'
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# SALT = '36dcb01de5d046d88b9a3701edf11c31' # used for password encryption