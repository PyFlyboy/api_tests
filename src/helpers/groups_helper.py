import logging as logger
from src.configs.endpoints_config import API_ENDPOINTS
from src.configs.api_payloads import GROUPS
from src.utilities.requests_utility import RequestsUtility
from src.utilities.token_utility import TokenUtility
import json



class GroupsHelper(object):

    def __init__(self):
        self.cred = TokenUtility()
        self.request_helper = RequestsUtility()
        self.new_headers = {"Content-Type": "application/json",
                            "Authorization": f"Bearer {self.cred.get_bearer_token()}"}


    def list_of_groups(self, page=1, limit=20):
        logger.debug("Calling for list of groups.")
        data = json.loads(GROUPS['post']['groupsList'])
        data['data'][0]['pager']['page'] = page
        data['data'][0]['pager']['limit'] = limit

        req = self.request_helper.post(endpoint=API_ENDPOINTS['groups']['post']['groupsList'], payload=data,
                                       headers=self.new_headers)

        return req


    def number_of_active_groups(self):
        logger.debug("Calling for total number of active groups.")
        data = json.loads(GROUPS['post']['groupsTotal'])
        req = self.request_helper.post(endpoint=API_ENDPOINTS['groups']['post']['groupsTotal'], payload=data,
                                       headers=self.new_headers)
        return req

    def number_of_inactive_groups(self):
         logger.debug("Calling for total number of inactive groups.")
         data = json.loads(GROUPS['post']['groupsTotal'])
         data['data'][0]['filter'][0]['value'] = 1
         req = self.request_helper.post(endpoint=API_ENDPOINTS['groups']['post']['groupsTotal'], payload=data,
                                        headers=self.new_headers)
         return req

