from src.helpers.person_helper import PersonHelper
from src.dao.persons_dao import PersonsDAO
import pytest
import unittest
from src.utilities.custom_logger import customLogger



class PersonApiTest(unittest.TestCase):

    log = customLogger()

    @pytest.fixture(autouse=True)
    def my_setup(self):
        self.person_helper = PersonHelper()
        self.person_dao = PersonsDAO()

    def test_t1_list_of_persons(self):
        """
        Call for list of persons
        """
        self.log.info("*#" * 20)
        self.log.info("test_t1_list_of_persons")
        self.log.info("*#" * 20)

        # Set page and groups number you want to call
        expected_number_of_persons = 20
        set_page = 1
        rs_persons = self.person_helper.list_of_persons(page=set_page,limit=expected_number_of_persons)

        # verify the number
        # verify the number of users object
        number_of_persons = len(rs_persons['result']['records'])
        assert number_of_persons == expected_number_of_persons, self.log.error('TEST FAILED: Expected number of persons is not equal to result')

    def test_t2_get_total_number_of_active_persons(self):
        """
        Get total number number of active persons
        """
        self.log.info("*#" * 20)
        self.log.info("test_t2_get_total_number_of_active_persons")
        self.log.info("*#" * 20)

        # make the call with parameter is_removed set to 0
        rs_person = self.person_helper.total_number_of_active_persons()
        number = rs_person['result']

        # get the number from database
        rs_dao = self.person_dao.get_total_number_of_active_persons()

        # assert that api result is equal to database
        assert number == rs_dao[0]['count(*)'], self.log.error("TEST FAILED: API respnse not the same as in databse")

    def test_t3_get_total_number_of_inactive_persons(self):
        """
        Get total number of inactive person
        """
        self.log.info("*#" * 20)
        self.log.info("test_t3_get_total_number_of_inactive_persons")
        self.log.info("*#" * 20)

        # make the call with parameter is_removed set to 1
        rs_person = self.person_helper.total_number_of_inactive_persons()
        number = rs_person['result']

        # get the number from database
        rs_dao = self.person_dao.get_total_number_of_inactive_persons()

        # assert that api result is equal to database
        assert number == rs_dao[0]['count(*)'], self.log.error("TEST FAILED: API respnse not the same as in databse")

    def test_t4_add_new_person(self):
        """
        Verify that new person is added correctly
        """
        self.log.info("*#" * 20)
        self.log.info("test_t4_add_new_person")
        self.log.info("*#" * 20)

        # get the helper object to make a api call
        rs_person = self.person_helper.add_new_person()

        # check if the result is success
        assert rs_person['result']['success'] == 'true', self.log.error("TEST FAILED: API call failed to add new person")

        # retrive information about new added person from api response to compare it with database
        person_id = rs_person['result']['data']['id']

        # get dao object to check if added person is in database
        rs_dao = self.person_dao.get_person_info(person_id=person_id)
        assert rs_dao[0]['is_active'] == 1, self.log.error("TEST FAILED: New added person is not active.")

    def test_t5_deactivate_person(self):
        """
        Verify that new person is deactivated
        """
        self.log.info("*#" * 20)
        self.log.info("test_t5_deactivate_new_person")
        self.log.info("*#" * 20)

        # get the helper object to make a api call
        rs_person = self.person_helper.delete_person()

        # check if the result is success
        assert rs_person['result']['success'] == 'true', self.log.error("TEST FAILED: API call failed to add new person")
        self.log.info(rs_person['result']['info'])
        # retrive information about deactivated person from api response to compare it with database
        person_id = rs_person['result']['data']['unique_item_id']

        # get dao object to check if person is deactivated in database
        rs_dao = self.person_dao.get_person_info(person_id=person_id)
        assert rs_dao[0]['is_active'] == 0, self.log.error("TEST FAILED: Person is not deactivated.")


    def test_t6_reactivate_person(self):
        """
        Verify that deactivated person is reactivated
        """
        self.log.info("*#" * 20)
        self.log.info("test_t6_activate_person")
        self.log.info("*#" * 20)

        # get the helper object to make a api call
        rs_person = self.person_helper.reactivate_person()

        # check if the result is success
        assert rs_person['method'] == 'reactivate'
        assert rs_person['result']['success'] == 'true', self.log.error("TEST FAILED: API call failed to reactivate new person")
        self.log.info(rs_person['result']['info'])

        # retrive information about activated person from api response to compare it with database
        person_id = rs_person['result']['data']['unique_item_id']

        # get dao object to check if person is deactivated in database
        rs_dao = self.person_dao.get_person_info(person_id=person_id)
        assert rs_dao[0]['is_active'] == 1, self.log.error("TEST FAILED: Person is not reactivated.")

