from src.helpers.contractor_helper import ContractorHelper
from src.dao.contractor_dao import ContractorDAO
import pytest
import unittest
from src.utilities.custom_logger import customLogger



class ContractorApiTest(unittest.TestCase):

    log = customLogger()

    @pytest.fixture(autouse=True)
    def my_setup(self):
        self.contractor_helper = ContractorHelper()
        self.contractor_dao = ContractorDAO()

    @pytest.mark.tcid1
    def test_t1_list_of_contractors(self):
        """
        Call for list of contractors
        """
        self.log.info("*#" * 20)
        self.log.info("test_t1_list_of_contractors")
        self.log.info("*#" * 20)

        # Set page and groups number you want to call
        expected_number_of_contractors = 5
        set_page = 1
        rs_contractor = self.contractor_helper.list_of_contractors(page=set_page,limit=expected_number_of_contractors)

        # verify expected number with result
        number_of_contractors = len(rs_contractor['result']['records'])
        assert number_of_contractors == expected_number_of_contractors, self.log.error('TEST FAILED: Expected number of persons is not equal to result')

    @pytest.mark.tcid2
    def test_t2_get_total_number_of_contractors(self):
        """
        Get total number number of contractors
        """
        self.log.info("*#" * 20)
        self.log.info("test_t2_get_total_number_of_contractors")
        self.log.info("*#" * 20)

        # make the call with parameter is_removed set to 0
        rs_contractor = self.contractor_helper.total_number_of_contractor()
        number = rs_contractor['result']

        # get the number of contractors from database
        rs_dao = self.contractor_dao.get_total_number_of_contractors()

        # assert that api result is equal to database
        assert number == rs_dao[0]['count(*)'], self.log.error("TEST FAILED: API respnse not the same as in databse")

    @pytest.mark.tcid3
    def test_t3_add_new_contractor(self):
        """
        Verify that new person is added correctly
        """
        self.log.info("*#" * 20)
        self.log.info("test_t3_add_new_contractor")
        self.log.info("*#" * 20)

        # get the helper object to make a api call
        rs_contractor = self.contractor_helper.add_new_contractor()

        # check if the result is success
        assert rs_contractor['result']['success'] == True, self.log.error("TEST FAILED: API call failed to add new contractor")

        # retrive information about new added contractor from api response to compare it with database
        contractor_id = rs_contractor['result']['id']

        # get dao object to check if added object is in database
        rs_dao = self.contractor_dao.get_contractor_info(contractor_id=contractor_id)

        assert rs_dao[0]['action_tpe'] == 'create', self.log.error(f"TEST FAILED: Incorrect action type. Should be: 'create' is: {rs_dao[0]['action_tpe']}")

    @pytest.mark.tcid4
    def test_t4_edit_contractor(self):
        """
        Verify that new person is deactivated
        """
        self.log.info("*#" * 20)
        self.log.info("test_t4_edit_contractor")
        self.log.info("*#" * 20)

        # make an api call to edit new added contractor
        rs_contractor = self.contractor_helper.edit_contractor()
        contractor_id = rs_contractor['result']['id']

        assert rs_contractor['result']['success'] == True, self.log.error('TEST FAILED: New contractor has not been added.')
        if rs_contractor['result']['success'] != True:
            self.log.info(rs_contractor['result']['info'])

        # get the confiramtion from database
        rs_dao = self.contractor_dao.get_contractor_info(contractor_id=contractor_id)
        contractor_status = rs_dao[0]['action_tpe']
        # verify if new edited contractor has proper status
        assert contractor_status == 'update', self.log.error(f"TEST FAILED: Incorrect action type. Should be: 'update' is: '{contractor_status}'")

    @pytest.mark.tcid5
    def test_t5_delete_contractor(self):
        """
        Verify API call for delete contractor
        """
        self.log.info("*#" * 20)
        self.log.info("test_t5_delete_contractor")
        self.log.info("*#" * 20)

        # get the helper object to make a api call
        rs_contractor = self.contractor_helper.remove_contractor()

        # check if the result is success
        assert rs_contractor['method'] == 'remove'
        assert rs_contractor['result']['success'] == True, self.log.error("TEST FAILED: API call failed to delete contractor")
        if rs_contractor['result']['success'] != True:
            self.log.info(rs_contractor['result']['info'])

    

