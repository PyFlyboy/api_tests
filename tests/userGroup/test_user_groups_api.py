from src.helpers.user_groups_helper import UserGroupsHelper
from src.configs.api_payloads import USER, USERGROUP
from src.dao.user_group_dao import UserGroupsDAO
import pytest
from src.utilities.custom_logger import customLogger
import unittest

class UserGroupApiTest(unittest.TestCase):

    log = customLogger()

    @pytest.fixture(autouse=True)
    def my_setup(self):
       self.user_groups_helper = UserGroupsHelper()
       self.user_groups_dao = UserGroupsDAO()

    def test_t1_list_of_user_groups(self):
        """
       Test list of user groups
        """
        self.log.info("*#" * 20)
        self.log.info("test_t1_list_of_user_groups")
        self.log.info("*#" * 20)


        # Set page number and how many users you want to call
        expected_page = 1
        expected_limit = 100 # Dlaczego 100 ? ??

        rs_user_group = self.user_groups_helper.list_of_groups()
        records = rs_user_group['result']['records']
        if records is not None:
            return True
        return False

        # verify the the action is correct
        assert rs_user_group['action'] == 'UserGroup', self.log.error('API response is not success')
        assert records == True, self.log.error("API response is an empty list")

    def test_t2_change_user_group(self):
        """
        Test the new group assaigments for user
        """
        self.log.info("*#" * 20)
        self.log.info("test_t2_change_user_group")
        self.log.info("*#" * 20)

        # get the helper object for payload
        payload = self.user_groups_helper.prepare_valid_data()
        rs_change_user_group = self.user_groups_helper.change_user_group(payload)

        # verify api response is success
        assert rs_change_user_group['result']['success'] == True, self.log.error("API response is not success")

        # verify response  with data base
        user_id = payload[0]
        assignments_data = payload[1]
        revokes_data = payload[2]

        rs_dao = self.user_groups_dao.get_changed_usr_grp(user_id)
        removed_grp_id = []
        added_grp_id = []
        for element in rs_dao:
            if element['change_tpe'] == 'remove':
                removed_grp_id.append(element['grp_id'])
            else:
                added_grp_id.append(element['grp_id'])

        # make assertion api response with database
        assert removed_grp_id == revokes_data, self.log.error("Removed grp_id is not the same as in api call")
        assert added_grp_id == assignments_data, self.log.error("Added grp_id is not the same as in api call")







