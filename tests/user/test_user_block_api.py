from src.helpers.user_helper import UserHelper
from src.configs.api_payloads import USER
from src.dao.users_dao import UserDAO
import pytest
import logging as logger
import json

@pytest.fixture(scope='module')
def my_setup():
    info = {}
    info['user_helper'] = UserHelper()
    return info

def test_block_the_user(my_setup):

    """
    Get list of users with default parameters
    """
    logger.info("Testing block user api")

    # get the helper object
    user_helper = my_setup['user_helper']

    # Call API to block the user
    rs_user = user_helper.block_user()
    # Get id from blocked user
    userId = int(rs_user['result']['data']['id'])
    # verify the result is success
    assert rs_user['result']['success'] == True
    logger.info(rs_user['result']['info'])

    # verify blocked user in the response with database
    dao = UserDAO()
    rs_dao = dao.get_blocked_user(userId=userId)

    assert rs_dao == True, f"Response not same as in database"

def test_unblock_the_user(my_setup):
    """

      """
    logger.info("Testing unblock user api")

    # get the helper object
    user_helper = my_setup['user_helper']

    # Call API to unblock the user
    rs_user = user_helper.unblock_user()
    userId = rs_user['result']['data']['id']
    # verify the result is success
    assert rs_user['result']['success'] == True, f"Result status is incorrect"

    # verify unblocked user in the response with database
    dao = UserDAO()
    rs_dao = dao.get_user_details(userId=userId)
    id_dao = str(rs_dao['id'])

    assert userId == id_dao, f"Response not same as in database"

