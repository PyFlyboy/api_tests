from src.helpers.user_helper import UserHelper
from src.dao.users_dao import UserDAO
import pytest
import logging as logger
import json

@pytest.fixture(scope='module')
def my_setup():
    info = {}
    info['user_helper'] = UserHelper()
    return info



def test_get_active_users_number(my_setup):
    """
    Get number of active users
    """
    logger.info("Testing list of users")

    # get the helper object
    user_helper = my_setup['user_helper']

    # make the call with parameter is_removed = 0
    rs_user = user_helper.call_total_number_of_active_users()
    number = rs_user['result']
    # verify number in the response with database
    dao = UserDAO()
    rs_dao = dao.get_total_number_of_active_users()
    assert number == rs_dao[0]['count(*)'], f"API respnse not the same as in databse"

def test_get_inactive_users_number(my_setup):
    """
    Get number of inactive users
    """
    logger.info("Testing list of users")

    # get the helper object
    user_helper = my_setup['user_helper']

    # make the call with parameter is_removed = 1
    rs_user = user_helper.call_total_number_of_inactive_users()
    number = rs_user['result']

    # verify number in the response with database
    dao = UserDAO()
    rs_dao = dao.get_total_number_of_inactive_users()

    assert number == rs_dao[0]['count(*)'], f"API Response not same as in database"
