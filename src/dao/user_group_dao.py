from src.utilities.db_utilities import DbUtility


class UserGroupsDAO(object):

    def __init__(self):
        self.db_helper = DbUtility()

    def get_total_number_of_active_users(self):

        sql = "select count(*) from usr where is_removed=0"
        rs_sql = self.db_helper.execute_select(sql)

        return rs_sql

    def get_all_user_grp_id(self):

        sql = "SELECT DISTINCT grp_id from usr_grp"
        rs_sql = self.db_helper.execute_select(sql)
        id_list=[]
        for index in range(len(rs_sql)):
            for key in rs_sql[index]:
                id_list.append(rs_sql[index][key])

        return id_list

    def get_changed_usr_grp(self, user_id=None):

        sql= f"SELECT * FROM usr_grp_trace where usr_id = {user_id}"

        rs_sql = self.db_helper.execute_select(sql)

        return rs_sql







