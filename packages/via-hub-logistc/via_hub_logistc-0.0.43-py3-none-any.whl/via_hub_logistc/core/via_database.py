import pymongo
import ibm_db

from pydoc import cli
from datetime import datetime

from robot.api.logger import info, debug, trace, console, error
from robot.api.deco import keyword
from robot.api import Error

class ViaMongo():

    def connect_to_database(self, strConnction):
        try:
            client = pymongo.MongoClient(f"mongodb://{strConnction}/")

            return client
        except Exception as e:
            raise Error(e)


    def disconnect_to_database(self, client):
        try:
            client.close()

            info("Connection has closed sucess")
        except Exception as e:
            raise Error(e)


    def find_all(self, client, baseName, collectionName):
        try:
            lstItems = []

            dataBase = client[baseName]

            collection = dataBase[collectionName]

            result = collection.find()

            for item in result:
                lstItems.append(item)

            info(lstItems)

            return lstItems
        except Exception as e:
            raise Error(e)


    def find_by_parameter(self, client, baseName, collectionName, filter):
        try:
            dataBase = client[baseName]

            collection = dataBase[collectionName]

            return collection.find(filter)

        except Exception as e:
            raise Error(e)

class ViaDb2():

    def connect_to_db2(self, host, db_name, user_id, password):
        try:
            connString = f"ATTACH=FALSE;DATABASE={db_name};HOSTNAME={host};PROTOCOL=TCPIP;UID={user_id};PWD={password}"
            return ibm_db.connect(connString, '', '')
        except Exception as e:
            raise Error(e)
    
    def get_all_table_name_db2(self, connection):
        db_connection = None
        lst_table_name = []

        try:
            db_connection = connection

            sql_stmt = ""

            result = ibm_db.exec_immediate(db_connection, sql_stmt)

            while(ibm_db.fetch_tuple(result)):

                name = ibm_db.fetch_tuple(result)

                if type(name) != bool:
                    lst_table_name.append(name[0])

            return lst_table_name
        except Exception as e:
            raise Error(e)


    def execute_query_db2(self, connection, query):
        db_connection = None

        lsr_result = []

        try:
            stmt = ibm_db.exec_immediate(connection, query)

            result = ibm_db.fetch_assoc(stmt)

            while(result):

                if type(result) != bool:
                    lsr_result.append(result)

                result = ibm_db.fetch_assoc(stmt)

            return lsr_result
        except Exception as e:
            raise Error(e)
