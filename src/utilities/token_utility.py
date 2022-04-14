from src.configs.configurations import getConfig
import requests
from src.configs.hosts_config import HOSTS
import json
from src.configs.credensials import JWT, AUTH, MYSQL


class TokenUtility(object):



    def __init__(self):
        pass

    def jwt_token_payload(self):
        jwt_username = JWT['username']
        jwt_password = JWT['password']
        jwt_system = JWT['system']

        if not jwt_username or not jwt_password:
            raise Exception("The API credentials 'jwt_username' and 'jwt_password' are not defined.")
        else:
            return {'username': jwt_username, 'password': jwt_password, 'system': jwt_system}


    def get_bearer_token(self):

        token = self.jwt_token_payload()
        headers = {"Content-Type": "application/json", }
        base_url = HOSTS['app'] + AUTH['endpoint']
        import pdb; pdb.set_trace()
        get_data = requests.post(url=base_url, data=json.dumps(token), headers=headers, verify=False)
        result = get_data.json()
        jwt = str(result['token'])

        if not get_data.status_code == 200:
            raise Exception(f"Bad Status code." \
            f"Expected 200, Actual status code: {get_data.status_code},")
        else:
            return jwt


    def get_db_credentials(self):
        db_user = MYSQL['user']
        db_password = MYSQL['password']
        if not db_user or not db_password:
            raise Exception("The DB credentials 'DB_USER' and 'DB_PASSWORD' are not defined")
        else:
            return {'user': db_user, 'password': db_password}



