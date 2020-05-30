from antiphishme.src.config import connexion_app, DEBUG, HOST, PORT

if __name__ == '__main__':
    connexion_app.run(host=HOST, port=PORT, debug=DEBUG)
