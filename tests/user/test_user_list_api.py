from src.helpers.user_helper import UserHelper
from src.configs.api_payloads import USER
import pytest
import logging as logger
import json

@pytest.fixture(scope='module')
def my_setup():
    info = {}
    info['user_helper'] = UserHelper()
    return info

def test_get_list_of_users(my_setup):
    """
    Get list of users with default parameters
    """
    logger.info("Testing list of users")

    # get the helper object
    user_helper = my_setup['user_helper']

    # Set page number and how many users you want to call
    expected_number_of_users = 3
    set_page = 6
    rs_user = user_helper.call_list_of_users(limit=expected_number_of_users,page=set_page)

    # verify the number of users object
    number_of_users = len(rs_user['result']['records'])
    assert number_of_users == expected_number_of_users, f'Expected number of usres is not equal to result'





