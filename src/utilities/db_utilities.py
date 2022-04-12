import pymysql
import logging as logger
from src.utilities.token_utility import TokenUtility
from src.configs.db_config import DB_HOST

class DbUtility(object):

    def __init__(self):
        credens = TokenUtility()
        self.credens = credens.get_db_credentials()
        self.host = DB_HOST['lab']['app']['host']
        self.port = DB_HOST['lab']['app']['port']
        self.database = DB_HOST['lab']['app']['database']


    def create_connection(self):

        connection = pymysql.connect(host=self.host, user=self.credens['user'],
                                         password=self.credens['password'],database=self.database, port=self.port)
        if not connection.open:
            raise Exception(f"Failed to connect databse: {self.database}")
        #     cur = connection.cursor(pymysql.cursors.DictCursor)
        #     cur.execute("select count(id) from usr")
        #     res = cur.fetchall()
        #     print(res)
        # import pdb; pdb.set_trace()
        return connection


    def execute_select(self, sql):
        conn = self.create_connection()
        try:
            logger.debug(f"Executing: {sql}")
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            rs_dict = cur.fetchall()

            cur.close()
        except Exception as e:
            raise Exception(f"Failed running sql: {sql} \n  Error: {str(e)}")
        finally:
            conn.close()

        return rs_dict

    def execute_select_fetchone(self, sql):
        conn = self.create_connection()
        try:
            logger.debug(f"Executing: {sql}")
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            rs_dict = cur.fetchone()

            cur.close()
        except Exception as e:
            raise Exception(f"Failed running sql: {sql} \n  Error: {str(e)}")
        finally:
            conn.close()

        return rs_dict
    
