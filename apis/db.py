from os import getenv
#import pymssql
import pyodbc
import mysql.connector

def getAuthDB():
     

     connection = mysql.connector.connect(user=getenv('dbuser'),
     password=getenv('dbpassword'),host=getenv('dbhost'), database=getenv('dbname'))

     return connection




def checkUser(username, password, aud):
     conn= None
     cursor=None
     try:
          conn = getAuthDB()
          
          cursor = conn.cursor(dictionary=True)
          cursor.callproc('uni_auth.core_validateUser',[username, password, aud])
          
          result = []
          for res in cursor.stored_results():
               for row in res:

                    result.append(dict(zip(res.column_names,row)))
          conn.commit()
     except Exception as ex:
          conn.rollback()
          raise ex
     finally:
          conn.close()
          cursor.close()
    
     return result

def addUser(userObject):
     conn= None
     cursor=None
     try:
          conn = getAuthDB()
          
          cursor = conn.cursor(dictionary=True)
          cursor.callproc('uni_auth.core_addUser',[userObject['username'],userObject['password'],userObject['email'],
          userObject['mobile'],userObject['clientid'],
          userObject['roles'],userObject['ex1'],userObject['ex2'],userObject['ex3']])

          returnMsg=''
          returnStatus=1
          result = []
          result2 =[]
          for res in cursor.stored_results():
               for row in res:

                    result.append(dict(zip(res.column_names,row)))
          
          if(result[0]['result']==-1):
               returnMsg+='user already exists'
               returnStatus=-1

          if(result[0]['result']==-2):
               returnMsg+='incorrect client id'
               returnStatus=-2
               return {'message':returnMsg,'status':returnStatus}

          
          #add/create roles to user
          for role in userObject['roles'].split(','):
               cursor.callproc('uni_auth.core_addRole',[result[0]['userid'],role,userObject['clientid']])

          returnMsg+=',permission granted for the user'
          

          conn.commit()

          return {'message':returnMsg,'status':returnStatus}
     except Exception as ex:
          conn.rollback()
          raise ex
     finally:
          conn.close()
          cursor.close()
    
     




#print(checkUser('hiran','test456','test'))