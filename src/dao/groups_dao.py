from src.utilities.db_utilities import DbUtility


class GroupsDAO(object):

    def __init__(self):
        self.db_helper = DbUtility()

    def get_total_number_of_active_groups(self):

        sql = "select count(*) from grp where is_removed=0"
        rs_sql = self.db_helper.execute_select(sql)

        return rs_sql

    def get_total_number_of_inactive_groups(self):

        sql = "select count(*) from grp where is_removed=1"
        rs_sql = self.db_helper.execute_select(sql)

        return rs_sql

