from os import getenv
#import pymssql
import pyodbc


    
def checkUser(username, password, aud):

    drs = pyodbc.drivers()
    print(drs)

    connectionString = getenv(f'auth_db_connection',f'Driver=FreeTDS;Server=devboxsql;Database=UNI_AUTH;Uid=authdev;Pwd=test123;')
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    cursor.execute('exec [dbo].[core_validateUser] ?,?,?',username,password,aud)
    rows = cursor.fetchall()
    
    conn.close()
    return rows


#print(checkUser('hiran','test456','test'))