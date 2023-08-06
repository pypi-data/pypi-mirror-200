# Author : Snehamoy Laskar (pro programmer)
import requests as req


class MenousDB:

    def __init__(self, url, key, database):
        self.url = url
        self.key = key
        self.database = database

    def readDB(self):

        if self.database == None:
            raise Exception('No database')

        Headers = {
            'key': self.key,
            'database': self.database
        }
        ans = req.get(self.url + 'read-db', headers=Headers)
        try:
            return ans.json()
        except:
            return ans.text

    def createDb(self):

        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database
            }

            ans = req.post(self.url + 'create-db', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def deleteDatabase(self):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database
            }

            ans = req.delete(self.url + 'del-database', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def checkDbExists(self):

        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database
            }

            ans = req.get(self.url + 'check-db-exists', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def createTable(self, table:str, attributes:list):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            Json = {
                'attributes': attributes
            }

            ans = req.post(self.url + 'create-table', headers=Headers, json=Json)
            return ans.text

        except Exception as ex:
            raise ex

    def __str__(self) -> str:
        return self.database

    def checkTableExists(self, table):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            ans = req.get(self.url + 'check-table-exists', headers=Headers)
            return ans.text

        except Exception as ex:
            raise ex

    def insertIntoTable(self, table, values):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            Json = {
                'values': values,
            }

            ans = req.post(self.url + 'insert-into-table', headers=Headers, json=Json)
            return ans.text

        except Exception as ex:
            raise ex

    def selectWhere(self, table, conditions):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table
            }

            Json = {
                'conditions': conditions
            }

            ans = req.get(self.url + 'select-where', headers=Headers, json=Json)
            try:
                return ans.json()
            except:
                return ans.text

        except Exception as ex:
            raise ex

    def selectColumns(self, table, columns):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'columns': columns
            }

            ans = req.get(self.url + 'select-columns', headers=Headers, json=Json)
            try:
                return ans.json()
            except:
                return ans.text

        except Exception as ex:
            raise ex

    def selectColumnsWhere(self, table, columns, conditions):
        if self.database == None:
            raise Exception('No database')
        try:

            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'columns': columns,
                'conditions': conditions,
            }

            ans = req.get(self.url + 'select-columns-where', headers=Headers, json=Json)
            try:
                return ans.json()
            except:
                return ans.text

        except Exception as ex:
            raise ex

    def delete_where(self, table, conditions):
        if self.database == None:
            raise Exception('No Database')
        try:
            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'conditions':conditions
            }

            ans = req.delete(self.url+"delete-where", headers = Headers, json = Json)
            try:
                return ans.json()
            except:
                return ans.text
        except Exception as ex:
            return ex

    def delete_table(self, table):
            if self.database == None:
                raise Exception('No Database')
            try:
                Headers = {
                    'key': self.key,
                    'database': self.database,
                    'table': table,
                }
                ans = req.delete(self.url + "delete-table", headers=Headers)
                try:
                    return ans.json()
                except:
                    return ans.text
            except Exception as ex:
                return ex


    def update_table(self, table, conditions, values):
        try:
            Headers = {
                'key': self.key,
                'database': self.database,
                'table': table,
            }
            Json = {
                'conditions':conditions,
                'values':values
            }
            ans = req.post(self.url+'update-table', headers=Headers, json = Json)
            try:
                return ans.json()
            except:
                return ans.text
        except Exception as ex:
            return ex
