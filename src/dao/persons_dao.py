from src.utilities.db_utilities import DbUtility


class PersonsDAO(object):

    def __init__(self):
        self.db_helper = DbUtility()

    def get_total_number_of_active_persons(self):

        sql = "select count(*) from pr_person where is_removed=0"
        rs_sql = self.db_helper.execute_select(sql)

        return rs_sql

    def get_total_number_of_inactive_persons(self):

        sql = "select count(*) from usr where is_removed=1"
        rs_sql = self.db_helper.execute_select(sql)

        return rs_sql

    def get_person_info(self, person_id):

        sql = f"select * from pr_person where item_id = '{person_id}'"
        rs_sql = self.db_helper.execute_select(sql)

        return  rs_sql

    def get_person_from_dao(self):

        sql = f"select * from pr_person"
        rs_sql = self.db_helper.execute_select_fetchone(sql)

        return rs_sql


