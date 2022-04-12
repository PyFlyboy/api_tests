from src.helpers.user_helper import UserHelper
from src.configs.api_payloads import USER, USERGROUP
from src.dao.users_dao import UserDAO
import pytest
from src.utilities.custom_logger import customLogger
import unittest

class UsrApiTest(unittest.TestCase):

    log = customLogger()

    @pytest.fixture(autouse=True)
    def my_setup(self):
       self.user_helper = UserHelper()
       self.user_dao = UserDAO()

    @pytest.mark.tcid1
    def test_t1_list_of_users(self):
        """
        Get list of users
        """
        self.log.info("*#" * 20)
        self.log.info("test_t1_list_of_users")
        self.log.info("*#" * 20)

        # Set page number and how many users you want to call
        expected_number_of_users = 3
        set_page = 6
        rs_user = self.user_helper.call_list_of_users(page=set_page, limit=expected_number_of_users)

        # verify the number of users object
        number_of_users = len(rs_user['result']['records'])
        assert number_of_users == expected_number_of_users, self.log.error("TEST FAILED: Number of users not the same as expected")

    @pytest.mark.tcid2
    def test_t2_block_the_user(self):
        """
        Block the user test
        """
        self.log.info("*#" * 20)
        self.log.info("test_t2_block_the_users")
        self.log.info("*#" * 20)


        # Call API to block the user
        rs_user = self.user_helper.block_user()

        # Get id from blocked user
        userId = int(rs_user['result']['data']['id'])

        # verify the result is success
        assert rs_user['result']['success'] == True, self.log.info("TEST FAILED: Result of the API call is not success.")
        if rs_user['result']['success'] != True:
            self.log.info(rs_user['result']['info'])

        # verify blocked user in the response with database
        rs_dao = self.user_dao.get_blocked_user(userId=userId)
        assert rs_dao == True, self.log.info("TEST FAILED: User is not blocked in database.")

    @pytest.mark.tcid13
    def test_t3_unblock_the_user(self):
        """
        Unblock the user test
        """
        self.log.info("*#" * 20)
        self.log.info("test_t3_unblock_the_user")
        self.log.info("*#" * 20)


        # Call API to unblock the user
        rs_user = self.user_helper.unblock_user()
        userId = rs_user['result']['data']['id']

        # verify the result is success
        assert rs_user['result']['success'] == True, self.log.info("TEST FAILED: Result of the API call is not success.")

        # verify unblocked user with database
        rs_dao = self.user_dao.get_user_details(userId=userId)
        id_dao = rs_dao['is_blocked']

        assert userId == id_dao, self.log.info("TEST FAILED: Result of the API call is not success.")

    @pytest.mark.tcid4
    def test_t4_remove_the_user(self):
        """
        Remove the user
        """
        self.log.info("*#" * 20)
        self.log.info("test_t4_remove_the_user")
        self.log.info("*#" * 20)

        # Call API to block the user
        rs_user = self.user_helper.remove_user()

        # Assert if result is success
        assert rs_user['result']['success'] == True, self.log.info("TEST FAILED: Result of the API call is not success.")
        # Verify Api method
        assert rs_user['method'] == 'remove', self.log.info("TEST FAILED: Incorrect method.")

        # Verify with database that the user is removed
        rs_dao = self.user_dao.get_removed_user()
        assert rs_dao == 1, self.log.info("TEST FAILED: Incorrect method.")

    @pytest.mark.tcid5
    def test_t5_active_users_number(self):

        """
        Get number of active users
        """
        self.log.info("*#" * 20)
        self.log.info("test_t5_active_users_number")
        self.log.info("*#" * 20)

        # make the call with parameter is_removed = 0
        rs_user = self.user_helper.call_total_number_of_active_users()
        number = rs_user['result']
        # verify number with database

        rs_dao = self.user_dao.get_total_number_of_active_users()
        assert number == rs_dao[0]['count(*)'], self.log.info("TEST FAILED: Result form API call not the same as in database.")

    @pytest.mark.tcid6
    def test_t6_inactive_users_number(self):
        """
        Get number of inactive users
        """
        self.log.info("*#" * 20)
        self.log.info("test_t6_inactive_users_number")
        self.log.info("*#" * 20)


        # make the call with parameter is_removed = 1
        rs_user = self.user_helper.call_total_number_of_inactive_users()
        number = rs_user['result']

        # verify number in the response with database
        rs_dao = self.user_dao.get_total_number_of_inactive_users()
        assert number == rs_dao[0]['count(*)'], self.log.info("TEST FAILED: Result form API call not the same as in database.")

    @pytest.mark.tcid7
    def test_t7_add_new_user(self):
        """
        Verify that new user is added
        """
        self.log.info("*#" * 20)
        self.log.info("test_t7_add_new_user.")
        self.log.info("*#" * 20)

        # get the helper object to make an api call
        rs_user = self.user_helper.add_new_user()

        # check if the result is success
        assert rs_user['result']['success'] == 'true', self.log.error("TEST FAILED: API call failed to add new user")

        # retrive information about new added user from api response to compare it with database
        user_id = rs_user['result']['data']['id']

        # get dao object to check if added user is in database
        rs_dao = self.user_dao.get_user_details(user_id=user_id)
        assert rs_dao[0]['id'] == user_id, self.log.error("TEST FAILED: New added user is not in database.")

    @pytest.mark.tcid8
    def test_t8_edit_user(self):
        """
        Edit new added user
        """
        self.log.info("*#" * 20)
        self.log.info("test_t8_edit_user")
        self.log.info("*#" * 20)

        # make an api call to edit new added user
        rs_user = self.user_helper.user_update()
        user_id = rs_user['result']['data']['id']

        assert rs_user['result']['success'] == 'true', self.log.error('TEST FAILED: Api call is not success.')
        if rs_user['result']['success'] != 'true':
            self.log.info(rs_user['result']['info'])

        # get the edited user object from database
        rs_dao = self.user_dao.get_user_details(user_id=user_id)
        user_dao_id = rs_sql[0]['id']
        # verify if new edited user is present in database
        assert user_id == user_dao_id, self.log.error("TEST FAILED: API respnse not the same as in databse")