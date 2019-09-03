from flask_restplus import Namespace, Resource, fields,marshal_with
from flask_jwt_extended import  jwt_required, get_raw_jwt
from flask import Flask,jsonify,request,flash,redirect,send_file
import logging,json
from apis.db import *
from apis.models import user
admin = Namespace('admin',ordered=False, description='Add/remove users and other user account and audience management endpoints')


    
# def clientAdmin_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         verify_jwt_in_request()
#         claims = get_jwt_claims()
#         if claims['roles'] != 'admin':
#             return jsonify(msg='Admins only!'), 403
#         audkey = getClientSecret( claims['aud'])
#         jwt.decode(encoded, public_key, algorithms='RS256')
#         else:
#             return fn(*args, **kwargs)
#     return wrapper


newUserModel = user.newUserModel(admin); # admin.model('user',user.fulluser)

clientModel = admin.model('client',user.client)

audModel = admin.model('aud',user.aud)


logger = logging.getLogger('admin')
@admin.route('/users/')
@admin.route('/users/<string:username>/' , methods=['GET'])
class Users(Resource):
      @admin.expect(newUserModel,validate=True)
      @admin.doc(responses={
            200: 'Success',
        401: 'Authentication Error',
        403: 'Requested resource unavailable',
        409: 'Conflict, document already exists',
        422: 'Validation Error'
                  })
      @jwt_required
      def post(self):
          try:
            reqdata =  request.get_json()
            rawjwt = get_raw_jwt()      
            if 'admin' not in rawjwt['aud']:#when aud admin is authanticated (only super admin can add users into any tenant/aud)
                reqdata['clientid'] = rawjwt['aud'][0]
                reqdata['tenant'] = rawjwt['tenant']

            if 'admin' in rawjwt['aud'] and 'tenant' in rawjwt['roles']:# tenant admin can add users to any aud
                print(rawjwt['tenant'][0])
                reqdata['tenant'] = rawjwt['tenant']
                
            if 'admin' in rawjwt['roles'] or 'tenant' in rawjwt['roles']:  #only admins can add users  
                res = addUser(reqdata)
                    
                return  res, 200
            else:
                return  {"msg": "Forbidden"}, 403

            
          except Exception as e:
              logger.error(e)
              return  {"msg": "Internal server error"}, 500


          

          
      @admin.doc(responses={
            200: 'return list of users in user model',
        401: 'Authentication Error',
        403: 'Requested resource unavailable',
        409: 'Conflict, document already exists',
        422: 'Validation Error'
                  })
      @jwt_required
      def get(self,username=''):
          try:
           
            rawjwt = get_raw_jwt()
            logger.info('get users '+username)
            tenant=rawjwt['tenant']
            aud=rawjwt['aud'][0]
            if(rawjwt['tenant']=='admin'):
                tenant=''
                aud=''
            users=getUser(username,aud,tenant)
           


            return json.dumps(users, sort_keys=True, default=str),200
          except Exception as e:
              logger.error(e)
              return  {"msg": "Internal server error"}, 500
          
@admin.route('/clients/<string:name>/' , methods=['GET'])
@admin.route('/clients')
class Clients(Resource):
      @admin.expect(clientModel,validate=True)
      @admin.doc(responses={
            200: 'Success',
        401: 'Authentication Error',
        403: 'Requested resource unavailable',
        409: 'Conflict, document already exists',
        422: 'Validation Error'
                  })
      @jwt_required
      def post(self):
          try:
            reqdata =  request.get_json()
            rawjwt = get_raw_jwt()      
            if 'admin' in rawjwt['roles'] and 'admin' in rawjwt['aud'] and 'admin'==rawjwt['tenant']:
                
                res = addClient(reqdata)
                
                return  res, 200

            else:
                return  {"msg": "Forbidden"}, 403
          except Exception as e:
              logger.error(e)
              return  {"msg": "Internal server error"}, 500


          

          
      @admin.doc(responses={
            200: 'success. server will return clientModel, as described in below section',
        401: 'Authentication Error',
        403: 'Requested resource unavailable',
        409: 'Conflict, document already exists',
        422: 'Validation Error'
                  })
      @jwt_required
      def get(self,name=''):
            try:
                reqdata =  request.get_json()
                rawjwt = get_raw_jwt()      
                if 'admin' in rawjwt['roles'] and 'admin' in rawjwt['aud'] and 'admin'==rawjwt['tenant']:
                    
                    res = getClients(name)
                    
                    return  json.dumps({'clients':res}, sort_keys=True, default=str), 200

                else:
                    return  {"msg": "Forbidden"}, 403
            except Exception as e:
              logger.error(e)
              return  {"msg": "Internal server error"}, 500