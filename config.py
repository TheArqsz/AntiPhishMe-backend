import os
import connexion
import logging 

connexion_app = connexion.App(__name__, specification_dir='./swagger')

DEBUG = bool(os.getenv('DEBUG', False))
BASE_DIR = connexion_app.root_path
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(format='[%(name)s %(levelname)s %(asctime)s]  %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=LOGGING_LEVEL)

PORT = os.getenv('PORT', 5000)
HOST = os.getenv('HOST', '127.0.0.1')

SQL_ALCH_DATABASE = None 
#
#   ===================================
#   DATABASE_DIALECT: postgresql+pg8000
#   DATABASE_USER: username
#   DATABASE_PASS: password
#   DATABASE_IP: ip(:port)
#   DATABASE_NAME: database
#   ===================================
#
if os.environ.get('DATABASE_DIALECT') and os.environ.get('DATABASE_USER') and os.environ.get('DATABASE_PASS') and os.environ.get('DATABASE_IP') and os.environ.get('DATABASE_NAME'):
    SQL_ALCH_DATABASE = f"{os.environ.get('DATABASE_DIALECT')}://{os.environ.get('DATABASE_USER')}:{os.environ.get('DATABASE_PASS')}@{os.environ.get('DATABASE_IP')}/{os.environ.get('DATABASE_NAME')}"
    logging.debug(f"[DATABASE] Using external database with dialect {os.environ.get('DATABASE_DIALECT')}")
else:
    logging.debug('[DATABASE] Either DATABASE_DIALECT, DATABASE_USER, DATABASE_PASS, DATABASE_URL or DATABASE_NAME is missing')
    logging.debug('[DATABASE] Using default sqlite database')
    pass
SQLALCHEMY_DATABASE_URI = SQL_ALCH_DATABASE or 'sqlite:///' + os.path.join(BASE_DIR, 'database/phishing.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

connexion_app.app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
connexion_app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

connexion_app.add_api('swagger.yml')
