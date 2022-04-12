from src.helpers.user_helper import UserHelper
from src.dao.users_dao import UserDAO
import pytest
import logging as logger


@pytest.fixture(scope='module')
def my_setup():
    info = {}
    info['user_helper'] = UserHelper()
    return info

def test_remove_the_user(my_setup):


    logger.info("Testing removing user api")

    # get the helper object
    user_helper = my_setup['user_helper']

    # Call API to block the user
    rs_user = user_helper.remove_user()

    # Assert if result is success
    assert rs_user['result']['success'] == True

    # Verify Api method
    assert rs_user['method'] == 'remove'

    # Verify result with database
    dao = UserDAO()
    rs_dao = dao.get_removed_user()

    assert rs_dao == 1, f"Response not same as in database"


