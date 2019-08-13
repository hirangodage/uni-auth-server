from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import  jwt_required, get_raw_jwt
from flask import Flask,jsonify,request,flash,redirect,send_file
import logging,json
from apis.db import *
admin = Namespace('admin', description='Add/remove users and other user account and audience management endpoints')


    
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


newUserModel = admin.model('user',{
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password'),
    'clientid': fields.String(required=True, description='client id or aud. this field is valid only for super admin'),
    'roles': fields.String(required=True, description='comma separated role list'),
    'tenant': fields.String(required=True, description='tenant name , valid only for super admin'),
    'email': fields.String(required=False, description='email address'),
    'mobile': fields.String(required=False, description='mobile number'),
    'ex1': fields.String(required=False, description='extended filed'),
    'ex2': fields.String(required=False, description='extended filed'),
    'ex3': fields.String(required=False, description='extended filed')
})

clientModel = admin.model('client',{
    'name': fields.String(required=True, description='tenant name'),
    'des': fields.String(required=True, description='description'),
    'aud':fields.String(required=True, description='comma separated list of audiances'),
    'adminUser':fields.Nested(newUserModel,required=True, description='default admin user'),
    'ex1': fields.String(required=False, description='extended filed'),
    'ex2': fields.String(required=False, description='extended filed'),
    'ex3': fields.String(required=False, description='extended filed')
})

audModel = admin.model('aud',{
    'clientid': fields.String(required=True, description='client name'),
    'clientSecret': fields.String(required=True, description='client password'),
    'Expire': fields.String(required=True, description='token expire in - ms'),
    
    'ex1': fields.String(required=False, description='extended filed'),
    'ex2': fields.String(required=False, description='extended filed'),
    'ex3': fields.String(required=False, description='extended filed')
})


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
                    
                    return  json.dumps(res, sort_keys=True, default=str), 200

                else:
                    return  {"msg": "Forbidden"}, 403
            except Exception as e:
              logger.error(e)
              return  {"msg": "Internal server error"}, 500