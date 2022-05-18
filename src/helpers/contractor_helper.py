import logging as logger
from src.configs.endpoints_config import API_ENDPOINTS
from src.configs.api_payloads import CONTRACTOR
from src.utilities.requests_utility import RequestsUtility
from src.utilities.token_utility import TokenUtility
import json
from src.utilities.generic_utilities import GenericUtilities


class ContractorHelper(object):

    def __init__(self):
        self.cred = TokenUtility()
        self.request_helper = RequestsUtility()
        self.new_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.multipart_headers = {"Content-Type": "multipart/form-data; boundry=--------------------------662510648987951698252197"
                                                  , "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.generic_helper = GenericUtilities()


    def list_of_contractors(self, page=1, limit=15):

        logger.debug("Calling for list of contractors.")
        data = json.loads(CONTRACTOR['post']['contractorList'])
        data['data'][0]['pager']['page'] = page
        data['data'][0]['pager']['limit'] = limit

        req = self.request_helper.post(endpoint=API_ENDPOINTS['contractor']['post']['contractorList'], payload=data, headers=self.new_headers)

        return req


    def total_number_of_contractor(self):

        logger.debug("Calling for total number of contractor.")
        data = json.loads(CONTRACTOR['post']['contractorTotal'])
        req = self.request_helper.post(endpoint=API_ENDPOINTS['contractor']['post']['contractorTotal'], payload=data, headers=self.new_headers)

        return req


    def add_new_contractor(self):

        logger.debug("Adding new contactor")

        # Preparing new payload for api call
        name = self.generic_helper.generate_random_name()["name"]
        name_short = self.generic_helper.generate_radom_string(n=3)["random_string"]
        nip = str(self.generic_helper.random_id_with_N_digits(n=10))

        data = json.loads(CONTRACTOR['post']['addContractor'])
        data['name'] = name
        data['name_short'] = name_short
        data['nip'] = nip

        # Making a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['contractor']['post']['addContractor'], payload=data,
                                                           headers=self.multipart_headers)

        return req

    def edit_contractor(self, item_id=None):

        logger.debug("Editing new contactor")

        contractor_object = self.add_new_contractor()
        contractor_id = contractor_object['result']['id']

        if item_id == None:
            item_id = contractor_id
        else:
            item_id = item_id

        # Preparing new payload
        new_name = self.generic_helper.generate_random_name()["name"]

        data = json.loads(CONTRACTOR['post']['editContractor'])
        data['name'] = new_name
        data['unique_item_id'] = contractor_id

        # Making a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['contractor']['post']['editContractor'], payload=data,
                                       headers=self.multipart_headers)

        return req


    def remove_contractor(self, item_id=None):

        logger.debug("Removing new added contractor")

        # Create new contractor object
        contractor_obj = self.add_new_contractor()
        contractor_id = contractor_obj['result']['id']

        if item_id == None:
            item_id = contractor_id
        else:
            item_id = item_id

        # Preparing new payload
        data = json.loads(CONTRACTOR['post']['removeContractor'])
        data['data'][0] = contractor_id

        req = self.request_helper.post(endpoint=API_ENDPOINTS['contractor']['post']['removeContractor'], payload=data,
                                                 headers=self.new_headers)

        return req








