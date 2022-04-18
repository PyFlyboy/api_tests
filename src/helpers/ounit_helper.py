import logging as logger
from src.dao.users_dao import UserDAO
from src.configs.endpoints_config import API_ENDPOINTS
from src.configs.api_payloads import OUNIT
from src.utilities.requests_utility import RequestsUtility
from src.utilities.token_utility import TokenUtility
import json
from src.utilities.generic_utilities import GenericUtilities


class OunitHelper(object):

    def __init__(self):
        self.cred = TokenUtility()
        self.request_helper = RequestsUtility()
        self.new_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.multipart_headers = {"Content-Type": "multipart/form-data; boundry=--------------------------662510648987951698252197"
                                                  , "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.generic_helper = GenericUtilities()


    def ounits_tree(self):

        logger.debug("Calling for ounit tree.")
        data = json.loads(OUNIT['post']['unitRepository'])

        req = self.request_helper.post(endpoint=API_ENDPOINTS['ounit']['post']['ounitTree'], payload=data, headers=self.new_headers)

        return req


    def add_new_ounit(self):

        logger.debug("Adding new ounit.")
        name = self.generic_helper.generate_random_name()['name']
        code = self.generic_helper.generate_radom_string()['random_string']
        data = json.loads(OUNIT['post']['addOunit'])
        data['name'] = name
        data['code'] = code

        req = self.request_helper.post(endpoint=API_ENDPOINTS['ounit']['post']['addOunit'], payload=data,
                                                   headers=self.multipart_headers)

        return req


    def edit_ounit(self):

        logger.debug("Editing new added ounit")

        # Create new unit object for updating

        ounit_obj = self.add_new_ounit()
        ounit_id = ounit_obj['result']['data']['item_id']
        code = self.generic_helper.generate_radom_string()['random_string']
        # New data for update req
        new_name = self.generic_helper.generate_random_name()
        while True:
            if new_name == ounit_obj['result']['data']['name']:
                new_name = self.generic_helper.generate_random_name()
            else:
                break

        # Preparing new payload for update request
        data = json.loads(OUNIT['post']['editOunit'])
        data['name'] = new_name['name']
        data['unique_item_id'] = ounit_id
        data['code'] = code

        req = self.request_helper.post(endpoint=API_ENDPOINTS['ounit']['post']['editOunit'], payload=data,
                                                             headers=self.multipart_headers)

        return req


    def remove_ounit(self):

        logger.debug("Removing new added ounit")

        # Create new ounit object
        ounit_obj = self.add_new_ounit()
        ounit_id = ounit_obj['result']['data']['item_id']

        # Preparing new payload for remove request
        data = json.loads(OUNIT['post']['removeOunit'])

        data['data'][0] = ounit_id


        req = self.request_helper.post(endpoint=API_ENDPOINTS['ounit']['post']['removeOunit'], payload=data,
                                                 headers=self.new_headers)

        return req



    def reactivate_ounit(self):

        logger.debug("Reactivaiting removed ounit.")

        # Create new person object and delete it
        ounit_obj = self.remove_ounit()
        ounit_id = ounit_obj['result']['data']['item_id']


        # Preparing new payload for reactivate ounit request
        data = json.loads(OUNIT['post']['reactivateOunit'])
        data['data'][0] = ounit_id


        req = self.request_helper.post(endpoint=API_ENDPOINTS['ounit']['post']['reactivateOunit'], payload=data,
                                       headers=self.new_headers)

        return req


