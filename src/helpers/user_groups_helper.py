import logging as logger
from src.dao.user_group_dao import UserGroupsDAO
from src.configs.endpoints_config import API_ENDPOINTS
from src.configs.api_payloads import USER, USERGROUP
from src.utilities.requests_utility import RequestsUtility
from src.utilities.token_utility import TokenUtility
import json
import random
from src.helpers.user_helper import UserHelper
from src.utilities.custom_logger import customLogger

class UserGroupsHelper(object):

    log = customLogger()

    def __init__(self):
        self.cred = TokenUtility()
        self.request_helper = RequestsUtility()
        self.new_headers = {"Content-Type": "application/json",
                            "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.user_helper = UserHelper()
        self.grp_id_dao = UserGroupsDAO()


    def list_of_groups(self, page=1, limit=100):

        self.log.info("API call for user's groups")

        # get list of users id from api call
        get_all_users = self.user_helper.call_list_of_users(page, limit)
        users = get_all_users['result']['records']
        users_id = []
        for user in users:
            for key in user:
                if key == 'id' and len(user[key]) == 7: users_id.append(user[key])

        # Use random user id to fetch his groups
        random_id = random.choice(users_id)

        data = json.loads(USERGROUP['post']['userGroup'])
        data['data'][0]['usr_id'] = random_id
        data['data'][0]['pager']['limit'] = limit
        data['data'][0]['pager']['page'] = page

        req = self.request_helper.post(endpoint=API_ENDPOINTS['userGroup']['post']['groupList'], payload=data,
                                       headers=self.new_headers)

        return req


    def prepare_valid_data(self):

        """
        Returns  data for changeUser group api
        """

        # get random user id
        user_helper = self.user_helper.call_list_of_users()['result']['records']
        users_id = []
        for user in user_helper:
            for key in user:
                if key == 'id' and len(user[key]) == 7: users_id.append(int(user[key]))


        # get groups for random user
        random_user_id = random.choice(users_id)
        get_user_groups = self.list_of_groups()['result']['records']
        user_groups_id = []
        for index in range(len(get_user_groups)):
            for key in get_user_groups[index]:
                if key == 'id':
                    user_groups_id.append(int(get_user_groups[index][key]))

        # pick randomly two id's for revokes request  payload
        revokes_data = random.sample(user_groups_id, k=2)

        # remove form list groups with tpe = system
        for element in revokes_data:
            if len(str(element)) == 1:
                revokes_data.remove(element)

        # get from data base all groups id
        get_grp_id_dao = self.grp_id_dao.get_all_user_grp_id()

        # pick randomly two id's for new assignments
        assignments_data = random.sample(get_grp_id_dao, k=2)

        # remove form list groups with tpe = system
        for element in assignments_data:
            if len(str(element)) == 1:
                assignments_data.remove(element)

        return random_user_id, assignments_data, revokes_data

    def change_user_group(self, payload=None):

        if payload is not None:
            self.log.info("API call to change user groups")

            random_user_id, assignments_data, revokes_data = range(3)

            # prepare payload for request
            data = json.loads(USERGROUP['post']['changeGroup'])
            data['data'][0] = payload[random_user_id]
            data['data'][1] = payload[assignments_data]
            data['data'][2] = payload[revokes_data]

            # call api request
            req = self.request_helper.post(endpoint=API_ENDPOINTS['userGroup']['post']['changeUserGroups'], payload=data,
                                       headers=self.new_headers)

            return req
        else:
            self.log.error("Incorrect payload for API call.")



