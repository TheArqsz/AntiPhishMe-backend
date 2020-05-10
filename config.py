import os
import connexion
import logging 

# Swagger directory in which .yml files are stored
SWAGGER_DIR = os.getenv('SWAGGER_DIR', './swagger') 

#
# Set environment (eg. DEV, PROD) 
# Set DEBUG mode - debugger turned on and logging level set to DEBUG
#
DEBUG = bool(os.getenv('DEBUG', False))
ENVIRONMENT = os.getenv('ENVIRONMENT', 'DEV')

# Basic connexion app
connexion_app = connexion.App(__name__, specification_dir=SWAGGER_DIR)

# Base directory for whole project
BASE_DIR = connexion_app.root_path

# Logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(format='[%(name)s %(levelname)s %(asctime)s]  %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=LOGGING_LEVEL)

# Set app details such as host, port and domain
PORT = os.getenv('PORT', 5000)
HOST = os.getenv('HOST', 'localhost')
DOMAIN = os.getenv('DOMAIN', f"{HOST}:{PORT}")


# Database configuration
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

# Set proper swagger.yml file; swagger_base_file needs to be even to swagger.yml (with $DOMAIN)
if ENVIRONMENT == 'DEV':
    connexion_app.add_api('swagger.yml')
else:
    swagger_base_file = "swagger_base.yml"
    swagger_file =  f"swagger_{ENVIRONMENT.lower()}.yml"
    with open(f"{SWAGGER_DIR}/{swagger_base_file}", 'r') as f:
        text = f.read()
        text = text.replace('$DOMAIN', DOMAIN) 
    with open(f"{SWAGGER_DIR}/{swagger_file}", 'w') as w:
        w.write(text)
    connexion_app.add_api(swagger_file)
