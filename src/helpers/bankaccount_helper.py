import logging as logger
from src.configs.endpoints_config import API_ENDPOINTS
from src.configs.api_payloads import BANKACCOUNT
from src.utilities.requests_utility import RequestsUtility
from src.utilities.token_utility import TokenUtility
import json
from src.utilities.generic_utilities import GenericUtilities
from src.helpers.contractor_helper import ContractorHelper


class BankAccountHelper(object):

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


    def contractor_list_of_bankaccounts(self, page=1, limit=20, contractor=None):
        logger.debug("Calling for contractor bankaccounts.")

        data = json.loads(BANKACCOUNT['post']['bankList'])
        data['data'][0]['pager']['page'] = page
        data['data'][0]['pager']['limit'] = limit

        if contractor == None:
            new_contractor = self.contractor_helper.add_new_contractor()
            id_contr = new_contractor['result']['id']
            data['data'][0]['filter'][1]['value'] = id_contr
        else:
            data['data'][0]['filter'][1]['value'] = contractor['result']['id']


        req = self.request_helper.post(endpoint=API_ENDPOINTS['bankAccount']['post']['bankList'], payload=data,
                                       headers=self.new_headers)

        return req


    def contractor_bankaccount_number(self, contractor = None):
        logger.debug("Calling for contractor number of bankaccount.")

        data = json.loads(BANKACCOUNT['post']['bankTotal'])

        if contractor == None:
            new_contractor = self.contractor_helper.add_new_contractor()
            id_contr = new_contractor['result']['id']
            data['data'][0]['filter'][1]['value'] = id_contr
        else:
            data['data'][0]['filter'][1]['value'] = contractor['result']['id']

        req = self.request_helper.post(endpoint=API_ENDPOINTS['bankAccount']['post']['bankTotal'], payload=data,
                                       headers=self.new_headers)
        return req


    def add_new_bankaccount(self, contractor=None):
        logger.debug("Adding new contractor bankaccount")

        # Preparing new payload for api call
        data = json.loads(BANKACCOUNT['post']['addBank'])
        new_account = self.generic_helper.generate_random_bank_account()['account']
        data['accountnum'] = new_account

        # If contractor not provided create new one
        if contractor == None:
            new_contractor = self.contractor_helper.add_new_contractor()
            id_contr = new_contractor['result']['id']

            data['contractor'] = id_contr
        else:
            data['contractor'] = contractor

       # Make a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['bankAccount']['post']['addBank'], payload=data,
                                       headers=self.multipart_headers)

        return req


    def edit_contractor_bankaccount(self, contractor=None):
        logger.debug("Editing contractor bankaccount")

        # Preparing new payload
        data = json.loads(BANKACCOUNT['post']['editBank'])

        new_currency = self.generic_helper.generate_random_bank_account()['currency']
        data['currency'] = new_currency

        if contractor == None:
            contractor_object = self.contractor_helper.add_new_contractor()['result']['id']
            bank_object = self.add_new_bankaccount(contractor=contractor_object)
            bankaccount_id = bank_object['result']['data']['id']

            data['unique_item_id'] = bankaccount_id
        else:
            data['unique_item_id'] = contractor

        # Making a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['bankAccount']['post']['editBank'], payload=data,
                                       headers=self.multipart_headers)

        return req


    def remove_bankaccount(self, contractor=None):
        logger.debug("Removing new added address")

        # Preparing new payload
        data = json.loads(BANKACCOUNT['post']['removeAddress'])

        if contractor == None:
            contractor_object = self.contractor_helper.add_new_contractor()['result']['id']
            bank_object = self.add_new_bankaccount(contractor=contractor_object)
            bankaccount_id = bank_object['result']['data']['id']
            data['data'][0] = bankaccount_id
        else:
            data['data'][0] = contractor

        # Make a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['bankAccount']['post']['removeBank'], payload=data,
                                       headers=self.new_headers)
        return req




