from src.utilities.db_utilities import DbUtility


class UserDAO(object):

    def __init__(self):
        self.db_helper = DbUtility()

    def get_total_number_of_active_users(self):

        sql = "select count(*) from usr where is_removed=0"
        rs_sql = self.db_helper.execute_select(sql)

        return rs_sql

    def get_total_number_of_inactive_users(self):

        sql = "select count(*) from usr where is_removed=1"
        rs_sql = self.db_helper.execute_select(sql)

        return rs_sql

    def get_blocked_user(self, userId):

        # Returns False if user is not blocked
        sql = f"SELECT EXISTS(SELECT * FROM usr WHERE id = {userId} AND is_blocked = 1)"
        rs_sql = self.db_helper.execute_select(sql)

        get_value = rs_sql[0]
        value = [*get_value.values()]

        if value[0] == 1:
            return True
        return False

    def get_first_blocked_user_from_dao(self):

        # Return first blocked user
        sql = f"SELECT * FROM usr where is_blocked=1"
        rs_sql = self.db_helper.execute_select(sql)
        details = rs_sql[0]
        userId = details['id']

        return userId

    def get_user_details(self, user_id):

        sql = f"SELECT * FROM usr WHERE id = '{user_id}'"
        rs_sql = self.db_helper.execute_select(sql)

        user_details = rs_sql[0]

        return user_details

    def get_removed_user(self):

        # !!! Hardcoded - IT HAS TO BE CHANGED !!!

        sql = f"SELECT * FROM usr WHERE id = 1000339"
        rs_sql = self.db_helper.execute_select(sql)
        user_details = rs_sql[0]['is_removed']

        return user_details

