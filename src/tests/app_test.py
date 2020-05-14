import json
import connexion
import pytest
import logging as log 

from config import connexion_app, BASE_PATH, SWAGGER_DIR, arguments

flask_app = connexion.FlaskApp(__name__, )
flask_app.add_api('../swagger/swagger.yml', base_path=BASE_PATH, arguments=arguments)


@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c

@pytest.fixture(scope='module')
def helper(json_info):
    for info in json_info:
        first_row = info.decode("utf-8")
        try:
            return str(json.loads(first_row))
        except:
            return str(first_row)

def test_server_health(client):
    response = client.get(BASE_PATH + '/server/health')
    json = helper(response.response)
    assert response._status_code == 200
    assert 'db_status' in json
    assert 'server_status' in json
