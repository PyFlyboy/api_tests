import logging as logger
from src.dao.users_dao import UserDAO
from src.configs.endpoints_config import API_ENDPOINTS
from src.configs.api_payloads import PERSONCONTRACT
from src.utilities.requests_utility import RequestsUtility
from src.utilities.token_utility import TokenUtility
import json
from src.utilities.generic_utilities import GenericUtilities


class PersonContractHelper(object):

    def __init__(self):
        self.cred = TokenUtility()
        self.request_helper = RequestsUtility()
        self.new_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.multipart_headers = {"Content-Type": "multipart/form-data; boundry=--------------------------662510648987951698252197"
                                                  , "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.generic_helper = GenericUtilities()


    def list_of_person_contracts(self, page=1, limit=15):

        logger.debug("Calling for list of persons.")
        data = json.loads(PERSONCONTRACT['post']['contractList'])
        data['data'][0]['pager']['page'] = page
        data['data'][0]['pager']['limit'] = limit

        req = self.request_helper.post(endpoint=API_ENDPOINTS['person']['post']['personsList'], payload=data, headers=self.new_headers)

        return req


    def add_new_person_contract(self):

        logger.debug("Adding new person")
        name = self.generic_helper.generate_random_name_and_surname()["name"]
        surname = self.generic_helper.generate_random_name_and_surname()["surname"]
        ext_id = self.generic_helper.random_id_with_N_digits()

        data = json.loads(PERSON['post']['addPerson'])
        data['first_name'] = name
        data['surname'] = surname
        data['extTID'] = ext_id
        req = self.request_helper.post(endpoint=API_ENDPOINTS['person']['post']['addPerson'], payload=data,
                                                   headers=self.multipart_headers)
        return req


    def edit_person_contract(self):

        logger.debug("Editing new added person")

        # Create new person object for updating

        person_obj = self.add_new_person()
        person_id = person_obj['result']['data']['id']
        ext_id = self.generic_helper.random_id_with_N_digits()

        # New data for update req
        name_surname_obj = self.generic_helper.generate_random_name_and_surname()
        new_name = name_surname_obj['name']

        # Preparing new payload for update request
        data = json.loads(PERSON['post']['editPerson'])
        data['extTID'] = ext_id
        data['unique_item_id'] = person_id
        data['first_name'] = new_name

        req = self.request_helper.post(endpoint=API_ENDPOINTS['person']['post']['editPerson'], payload=data,
                                                   headers=self.multipart_headers)
        return req

