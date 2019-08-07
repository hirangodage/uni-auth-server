from os import getenv
#import pymssql
import mysql.connector

def getAuthDB():
     

     connection = mysql.connector.connect(user=getenv('dbuser'),
     password=getenv('dbpassword'),host=getenv('dbhost'), database=getenv('dbname'))

     return connection



def getUser(name):
     conn = getAuthDB()
          
     cursor = conn.cursor(dictionary=True)
     try:
         
          cursor.callproc('uni_auth.core_getUsers',[name])
          
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
     
     return result[0]

def getClientSecret(clientid):
     conn = getAuthDB()
          
     cursor = conn.cursor(dictionary=True)
     try:
         
          cursor.callproc('uni_auth.core_getClientSecret',[clientid])
          
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
     
     return result[0]['AudKey']

def checkUser(username, password, aud,tenant):
     conn = getAuthDB()
          
     cursor = conn.cursor(dictionary=True)
     try:
         
          cursor.callproc('uni_auth.core_validateUser',[username, password, aud,tenant])
          
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

def addUser(userObject,in_cur=None):
          conn = None
          cursor = None
          if in_cur is None:
               conn = getAuthDB()
               cursor = conn.cursor(dictionary=True)
          else:
               #conn = in_conn     
               cursor = in_cur
          try:
               
               cursor.callproc('uni_auth.core_addUser',[userObject['username'],userObject['password'],userObject['email'],
               userObject['mobile'],userObject['clientid'],
               userObject['ex1'],userObject['ex2'],userObject['ex3'],userObject['tenant']])

               returnMsg=''
               returnStatus=1
               result = []
               result2 =[]
               for res in cursor.stored_results():
                    for row in res:

                         result.append(dict(zip(res.column_names,row)))
               if(result[0]['result']==1):
                    returnMsg+='user added'
                    returnStatus=1
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
               
               if in_cur is None:
                    conn.commit()

               return {'message':returnMsg,'status':returnStatus}
          except Exception as ex:
               if in_cur is None:
                    conn.rollback()
               raise ex
          finally:
               if in_cur is None:
                    cursor.close()
                    conn.close()
               
     
    
def addAud(clientObject):
     
          conn = getAuthDB()
               
          cursor = conn.cursor(dictionary=True)
          try:
               
               cursor.callproc('uni_auth.core_addClient',[clientObject['clientid'],clientObject['clientSecret'],
               clientObject['Expire']
              ,clientObject['ex1'],clientObject['ex2'],clientObject['ex3']])

               returnMsg=''
               returnStatus=1
               result = []
               result2 =[]
               for res in cursor.stored_results():
                    for row in res:

                         result.append(dict(zip(res.column_names,row)))
               
               

               if(result[0]['ID']==-1):
                    returnMsg+='client already exists'
                    returnStatus=-1
                    conn.rollback()
                    return {'message':returnMsg,'status':returnStatus}

               
               # #add/create defult user
               # userobj = clientObject['adminUser']
               # userobj['clientid'] = clientObject['clientid']
               # userobj['roles'] = 'admin'
               # res = addUser(userobj,conn)

               returnMsg+='new client added'
               

               conn.commit()

               return {'message':returnMsg,'status':returnStatus}
          except Exception as ex:
               conn.rollback()
               raise ex
          finally:
               conn.close()
               cursor.close()     


def addClient(clientObject):
     
          conn = getAuthDB()
               
          cursor = conn.cursor(dictionary=True)
          try:
               
               cursor.callproc('uni_auth.core_addtenant',[clientObject['name'],clientObject['des']
               
              ,clientObject['ex1'],clientObject['ex2'],clientObject['ex3']])

               returnMsg=''
               returnStatus=1
               result = []
               result2 =[]
               for res in cursor.stored_results():
                    for row in res:

                         result.append(dict(zip(res.column_names,row)))
               
               #add auds to the company
               for auditem in clientObject['aud'].split(','):
                    cursor.callproc('uni_auth.core_addaudtotenant',[auditem,clientObject['name']])

               
               if(result[0]['ID']==-1):
                    returnMsg+='client already exists. audiences updated.'
                    returnStatus=-1
                    conn.commit()
                    return {'message':returnMsg,'status':returnStatus}
               
               
               #add/create defult user
               userobj = clientObject['adminUser']
               userobj['clientid'] = 'admin'
               userobj['tenant'] = clientObject['name']
               userobj['roles'] = 'tenant'
               res = addUser(userobj,cursor)
               returnMsg+=res['message']

               returnMsg+=',new client added'
               

               conn.commit()

               return {'message':returnMsg,'status':returnStatus}
          except Exception as ex:
               conn.rollback()
               raise ex
          finally:
               conn.close()
               cursor.close()   




#print(checkUser('hiran','test456','test'))