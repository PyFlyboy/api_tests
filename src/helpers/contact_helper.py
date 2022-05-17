import logging as logger
from src.configs.endpoints_config import API_ENDPOINTS
from src.configs.api_payloads import CONTACT
from src.utilities.requests_utility import RequestsUtility
from src.utilities.token_utility import TokenUtility
import json
from src.utilities.generic_utilities import GenericUtilities
from src.helpers.contractor_helper import ContractorHelper


class ContactHelper(object):

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


    def cretate_contractor_object(self):
        """
        Create contractor obj for api calls
        """
        contractor = self.contractor_helper.add_new_contractor()

        return contractor


    def list_of_contacts(self, page=1, limit=20, contractor=None):
        logger.debug("Calling for list of contacts.")

        data = json.loads(CONTACT['post']['contactList'])
        data['data'][0]['pager']['page'] = page
        data['data'][0]['pager']['limit'] = limit

        if contractor == None:
            new_contractor = self.contractor_helper.add_new_contractor()
            id_contr = new_contractor['result']['id']
            data['data'][0]['filter'][1]['value'] = id_contr
        else:
            data['data'][0]['filter'][1]['value'] = contractor['result']['id']

        req = self.request_helper.post(endpoint=API_ENDPOINTS['contact']['post']['contactList'], payload=data,
                                       headers=self.new_headers)
        return req


    def total_contact(self, contractor = None):
        logger.debug("Calling for total number of contact.")

        data = json.loads(CONTACT['post']['contactTotal'])

        if contractor == None:
            new_contractor = self.contractor_helper.add_new_contractor()
            id_contr = new_contractor['result']['id']
            data['data'][0]['filter'][1]['value'] = id_contr
        else:
            data['data'][0]['filter'][1]['value'] = contractor['result']['id']

        req = self.request_helper.post(endpoint=API_ENDPOINTS['contact']['post']['contactTotal'], payload=data,
                                       headers=self.new_headers)


        return req


    def add_new_contact(self, contractor=None):
        logger.debug("Adding new contact")

        # Preparing new payload for api call
        data = json.loads(CONTACT['post']['addContact'])
        name = self.generic_helper.generate_random_name()['name']
        tel = str(self.generic_helper.random_id_with_N_digits(n=10))
        email = self.generic_helper.generate_random_email_and_password()['email']
        data['name'] = name
        data['tel'] = tel
        data['email'] = email

        # If contractor not provided create new one
        if contractor == None:
            new_contractor = self.contractor_helper.add_new_contractor()
            id_contr = new_contractor['result']['id']
            data['contractor'] = id_contr
        else:
            data['contractor'] = contractor

        # Make a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['contact']['post']['addContact'], payload=data,
                                       headers=self.multipart_headers)


        return req


    def edit_contact(self, contractor=None):
        logger.debug("Editing new contact")

        # Preparing new payload
        data = json.loads(CONTACT['post']['editContact'])

        new_name = self.generic_helper.generate_random_name()["name"]
        data['name'] = new_name

        if contractor == None:
            contractor_object = self.contractor_helper.add_new_contractor()['result']['id']
            contact_object = self.add_new_contact(contractor=contractor_object)
            contact_id = contact_object['result']['data']['id']
            data['unique_item_id'] = contact_id
        else:
            data['unique_item_id'] = contractor

        # Making a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['contact']['post']['editContact'], payload=data,
                                       headers=self.multipart_headers)

        return req


    def remove_contact(self, contractor=None):
        logger.debug("Removing new added contact")

        # Preparing new payload
        data = json.loads(CONTACT['post']['removeContact'])

        if contractor == None:
            contractor_object = self.contractor_helper.add_new_contractor()['result']['id']
            contact_object = self.add_new_contact(contractor=contractor_object)
            contact_id = contact_object['result']['data']['id']
            data['data'][0] = contact_id
        else:
            data['data'][0] = contractor

        # Make a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['contact']['post']['removeContact'], payload=data,
                                       headers=self.new_headers)

        return req

