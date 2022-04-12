import logging as logger
from src.dao.users_dao import UserDAO
from src.configs.endpoints_config import API_ENDPOINTS
from src.configs.api_payloads import USER
from src.utilities.requests_utility import RequestsUtility
from src.utilities.token_utility import TokenUtility
from src.utilities.generic_utilities import GenericUtilities
from src.helpers.person_helper import PersonHelper
import json
import random


class UserHelper(object):

    def __init__(self):
        self.cred = TokenUtility()
        self.request_helper = RequestsUtility()
        self.new_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.multipart_headers = {"Content-Type": "multipart/form-data; boundry=--------------------------662510648987951698252197"
                                                  , "Authorization": f"Bearer {self.cred.get_bearer_token()}"}
        self.generic_helper = GenericUtilities()
        self.person_helper = PersonHelper()

    def call_list_of_users(self, page=3, limit=5):

        logger.debug("Calling for list of users.")
        data = json.loads(USER['post']['usersList'])
        data['data'][0]['pager']['page'] = page
        data['data'][0]['pager']['limit'] = limit

        req = self.request_helper.post(endpoint=API_ENDPOINTS['user']['post']['usersList'], payload=data, headers=self.new_headers)

        return req


    def call_total_number_of_active_users(self):

        logger.debug("Calling for total number of user.")
        data = json.loads(USER['post']['usersTotal'])
        req = self.request_helper.post(endpoint=API_ENDPOINTS['user']['post']['usersTotal'], payload=data, headers=self.new_headers)
        return req

    def call_total_number_of_inactive_users(self):

        logger.debug("Calling for total number of user.")
        data = json.loads(USER['post']['usersTotal'])
        data['data'][0]['filter'][0]['value']= 1
        req = self.request_helper.post(endpoint=API_ENDPOINTS['user']['post']['usersTotal'], payload=data, headers=self.new_headers)
        return req

    def add_new_user(self):

        logger.debug("Adding new user")

        # Prepare payload for api call:
        email_password = self.generic_helper.generate_random_email_and_password()
        person_obj = self.person_helper.add_new_person()
        person_id = person_obj['result']['data']['id']
        login = str(person_obj['result']['data']['first_name']) + '.' + str(person_obj['result']['data']['surname'])
        display_as = str(person_obj['result']['data']['first_name'])
        data = json.loads(USER['post']['addUser'])
        data['extTID'] = self.generic_helper.random_id_with_N_digits()
        data['person_id'] = person_id
        data['login'] = login
        data['email'] = email_password['email']
        data['display_as'] = display_as
        data['pass'] = email_password['password']
        data['pass2'] = email_password['password']

        # Make a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['user']['post']['addUser'], payload=data,
                                       headers=self.multipart_headers)

        return req

    def user_update(self):

        logger.debug("Updating user data.")

        # Create new user object for updating

        new_user = self.add_new_user()
        person_id = new_user['result']['data']['person_id']
        user_id = new_user['result']['data']['id']
        display_as = new_user['result']['data']['display_as']
        email = new_user['result']['data']['email']
        login = new_user['result']['data']['login']

        # New data for update req
        new_login = login + str(self.generic_helper.random_id_with_N_digits(2))

        # Preparing new payload for update request
        data = json.loads(USER['post']['updateUser'])
        data['extTID'] = self.generic_helper.random_id_with_N_digits()
        data['person_id'] = person_id
        data['id'] = user_id
        data['login'] = login
        data['email'] = email
        data['display_as'] =display_as
        data['login'] = new_login

        # Make a request call
        req = self.request_helper.post(endpoint=API_ENDPOINTS['user']['post']['updateUser'], payload=data,
                                       headers=self.multipart_headers)


        return req


    def block_user(self):

        logger.debug("Blocking user")

        # get list of users id from api call
        getUsersList = self.call_list_of_users(page=2,limit=5)
        usersList = getUsersList['result']['records']
        users_id = []
        for user in usersList:
            for key in user:
                if key == 'id' and len(user[key])==7: users_id.append(user[key])
        random_id = random.choice(users_id)
        data = json.loads(USER['post']['blockUser'])
        data['data'][0]['id'] = random_id

        req = self.request_helper.post(endpoint=API_ENDPOINTS['user']['post']['blockUser'], payload=data,
                                       headers=self.new_headers)
        return req


    def unblock_user(self):

        logger.debug("Blocking user")
        # get first blocked user from database
        userId_dao = UserDAO().get_first_blocked_user_from_dao()
        data = json.loads(USER['post']['unblockUser'])
        data['data'][0]['id'] = userId_dao
        req = self.request_helper.post(endpoint=API_ENDPOINTS['user']['post']['unblockUser'], payload=data,
                                      headers=self.new_headers)
        return req


    def remove_user(self):

        # hardcoded ID = 1000339 must be replaced
        logger.debug("Removing user")
        userId = 1000339
        data = json.loads(USER['post']['removeUser'])
        data['data'][0]['id'] = userId
        req = self.request_helper.post(endpoint=API_ENDPOINTS['user']['post']['removeUser'], payload=data,
                                       headers=self.new_headers)

        return req



