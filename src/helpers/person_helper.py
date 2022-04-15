import logging as logger
from src.dao.users_dao import UserDAO
from src.configs.endpoints_config import API_ENDPOINTS
from src.configs.api_payloads import USER,PERSON
from src.utilities.requests_utility import RequestsUtility
from src.utilities.token_utility import TokenUtility
import json
from src.utilities.generic_utilities import GenericUtilities


class PersonHelper(object):

    def __init__(self):
        self.cred = TokenUtility()
        self.request_helper = RequestsUtility()
        self.new_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.multipart_headers = {"Content-Type": "multipart/form-data; boundry=--------------------------662510648987951698252197"
                                                  , "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.generic_helper = GenericUtilities()


    def list_of_persons(self, page=1, limit=15):

        logger.debug("Calling for list of persons.")
        data = json.loads(PERSON['post']['personsList'])
        data['data'][0]['pager']['page'] = page
        data['data'][0]['pager']['limit'] = limit

        req = self.request_helper.post(endpoint=API_ENDPOINTS['person']['post']['personsList'], payload=data, headers=self.new_headers)

        return req


    def total_number_of_active_persons(self):

        logger.debug("Calling for total number of persons.")
        data = json.loads(PERSON['post']['personsTotal'])
        req = self.request_helper.post(endpoint=API_ENDPOINTS['person']['post']['personsTotal'], payload=data, headers=self.new_headers)
        return req

    def total_number_of_inactive_persons(self):

        logger.debug("Calling for total number of inactive persons.")
        data = json.loads(PERSON['post']['personsTotal'])
        data['data'][0]['filter'][0]['value']= 0
        req = self.request_helper.post(endpoint=API_ENDPOINTS['person']['post']['personsTotal'], payload=data, headers=self.new_headers)
        return req

    def add_new_person(self):

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


    def edit_person(self):

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


    def delete_person(self):

        logger.debug("Deleting new added person")

        # Create new person object
        person_obj = self.add_new_person()
        person_id = person_obj['result']['data']['id']

        # Preparing new payload for del request
        data = json.loads(PERSON['post']['deletePerson'])
        data['data'][0]['item_id'] = person_id

        req = self.request_helper.post(endpoint=API_ENDPOINTS['person']['post']['deletePerson'], payload=data,
                                                 headers=self.new_headers)
        return req



    def reactivate_person(self):

        logger.debug("Reactivating new deleted person")

        # Create new person object and delete it
        person_obj = self.delete_person()
        person_id = person_obj['result']['data']['unique_item_id']


        # Preparing new payload for new request
        data = json.loads(PERSON['post']['reactivatePerson'])
        data['data'][0]['item_id'] = person_id

        req = self.request_helper.post(endpoint=API_ENDPOINTS['person']['post']['reactivatePerson'], payload=data,
                                       headers=self.new_headers)

        return req

