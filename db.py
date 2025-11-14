import mysql.connector

# cnx = mysql.connector.connect(user='scott', password='password',
#                               host='127.0.0.1',
#                               database='employees')
# cnx.close()


class MysqlConnector():
    def __init__(self,user,password,host,database):
        self.user=user
        self.password=password
        self.host=host
        self.database=database
    
    def connection(self):
        return mysql.connector.connect(user=self.user, password=self.password,
                              host=self.host,
                              database=self.database)