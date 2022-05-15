import logging as logger
from src.configs.endpoints_config import API_ENDPOINTS
from src.configs.api_payloads import DICTVALUE
from src.dao.dictvalue_dao import DictvalueDAO
from src.utilities.requests_utility import RequestsUtility
from src.utilities.token_utility import TokenUtility
import json
import random


class DictvalueHelper(object):

    def __init__(self):
        self.cred = TokenUtility()
        self.request_helper = RequestsUtility()
        self.new_headers = {"Content-Type": "application/json",
                            "Authorization": f"Bearer {self.cred.get_bearer_token()}"}


    def dictvalue_list(self, page=1, limit=10):

       logger.debug("Calling for dictvalue list.")
       # get random dict_id from database
       dictvalue_list_dao = DictvalueDAO().get_dictvalue_lists()
       random_dict = random.choice(dictvalue_list_dao)
       dict_id = random_dict['dict_id']

       data = json.loads(DICTVALUE['post']['dictvalueList'])
       data['data'][0]['dict_id']= dict_id
       data['data'][0]['pager']['page'] = page
       data['data'][0]['pager']['limit'] = limit

       req = self.request_helper.post(endpoint=API_ENDPOINTS['dictvalue']['post']['dictvalueList'], payload=data,
                                       headers=self.new_headers)

       return req

