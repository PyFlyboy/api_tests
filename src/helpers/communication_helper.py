import logging as logger
from src.configs.endpoints_config import API_ENDPOINTS
from src.configs.api_payloads import COMMUNICATION
from src.utilities.requests_utility import RequestsUtility
from src.utilities.token_utility import TokenUtility
import json
from src.utilities.generic_utilities import GenericUtilities
from src.helpers.contractor_helper import ContractorHelper
from src.dao.persons_dao import PersonsDAO


class CommHelper(object):

    def __init__(self):
        self.cred = TokenUtility()
        self.request_helper = RequestsUtility()
        self.new_headers = {"Content-Type": "application/json",
                            "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.multipart_headers = {
            "Content-Type": "multipart/form-data; boundry=--------------------------662510648987951698252197"
            , "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.generic_helper = GenericUtilities()
        self.contractor_helper = ContractorHelper()
        self.person_dao = PersonsDAO()

    def cretate_contractor_object(self):
        """
        Create contractor obj for api calls
        """
        contractor = self.contractor_helper.add_new_contractor()

        return contractor


    def contractor_communication_list(self, page=1, limit=20, contractor=None):
        logger.debug("Calling for contractor communication list.")

        data = json.loads(COMMUNICATION['post']['commList'])
        data['data'][0]['pager']['page'] = page
        data['data'][0]['pager']['limit'] = limit

        if contractor == None:
            new_contractor = self.contractor_helper.add_new_contractor()
            id_contr = new_contractor['result']['id']
            data['data'][0]['filter'][1]['value'] = id_contr
        else:
            data['data'][0]['filter'][1]['value'] = contractor

        req = self.request_helper.post(endpoint=API_ENDPOINTS['communication']['post']['commList'], payload=data,
                                       headers=self.new_headers)
        return req


    def contractor_communication_total(self, contractor = None):
        logger.debug("Calling for contractor commmunication.")

        data = json.loads(COMMUNICATION['post']['commTotal'])

        if contractor == None:
            new_contractor = self.contractor_helper.add_new_contractor()
            id_contr = new_contractor['result']['id']
            data['data'][0]['filter'][1]['value'] = id_contr
        else:
            data['data'][0]['filter'][1]['value'] = contractor

        req = self.request_helper.post(endpoint=API_ENDPOINTS['communication']['post']['commTotal'], payload=data,
                                       headers=self.new_headers)
        return req


    def add_new_communication(self, contractor=None):
        logger.debug("Adding new communication for contractor")

        # Preparing new payload for api call
        data = json.loads(COMMUNICATION['post']['addComm'])
        person = self.person_dao.get_person_from_dao()['item_id']
        contact_person = self.generic_helper.generate_random_name_and_surname()['full_name']
        date = self.generic_helper.generate_random_date()['date']

        data['person'] = person
        data['contact'] = contact_person
        data['date'] = date

        # If contractor not provided create new one
        if contractor == None:
            new_contractor = self.contractor_helper.add_new_contractor()
            id_contr = new_contractor['result']['id']

            data['contractor'] = id_contr
        else:
            data['contractor'] = contractor

       # Make a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['communication']['post']['addComm'], payload=data,
                                       headers=self.multipart_headers)
        return req


    def edit_communication(self, contractor=None):
        logger.debug("Editing contractor communication")

        # Preparing new payload
        data = json.loads(COMMUNICATION['post']['editComm'])

        new_contact = self.generic_helper.generate_random_name_and_surname()['full_name']
        data['contact'] = new_contact

        if contractor == None:
            contractor_object = self.contractor_helper.add_new_contractor()['result']['id']
            comm_object = self.add_new_communication(contractor=contractor_object)
            comm_id = comm_object['result']['data']['id']

            data['unique_item_id'] = comm_id
        else:
            data['unique_item_id'] = contractor

        # Making a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['communication']['post']['editComm'], payload=data,
                                       headers=self.multipart_headers)

        return req


    def remove_communication(self, contractor=None):
        logger.debug("Removing new added communication details")

        # Preparing new payload
        data = json.loads(COMMUNICATION['post']['removeComm'])

        if contractor == None:
            contractor_object = self.contractor_helper.add_new_contractor()['result']['id']
            comm_object = self.add_new_communication(contractor=contractor_object)
            comm_id = comm_object['result']['data']['id']
            data['data'][0] = comm_id
        else:
            data['data'][0] = contractor['result']['id']

        # Make a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['communication']['post']['removeComm'], payload=data,
                                       headers=self.new_headers)
        return req


