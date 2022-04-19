from src.utilities.db_utilities import DbUtility
from src.utilities.custom_logger import customLogger

class ContractorDAO(object):

    def __init__(self):
        self.db_helper = DbUtility()
        self.logger = customLogger()

    def get_total_number_of_contractors(self):

        sql = "select count(*) from ict_contractor_inig"
        rs_sql = self.db_helper.execute_select(sql)

        return rs_sql

    def get_total_number_of_inactive_contractors(self):

        sql = "select count(*) from ict_contractor where is_active=1"
        rs_sql = self.db_helper.execute_select(sql)

        return rs_sql

    def get_removed_contractors(self, item_id=None):

        sql = f"select * from ict_contractor where item_id = '{item_id}'"
        rs_sql = self.db_helper.execute_select(sql)

        return rs_sql

    def get_contractor_info(self, contractor_id):

        sql = f"select * from ict_contractor_history where item_id = '{contractor_id}'"
        rs_sql = self.db_helper.execute_select(sql)

        return  rs_sql

