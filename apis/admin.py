from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import  jwt_required, get_raw_jwt
from flask import Flask,jsonify,request,flash,redirect,send_file
import logging
from apis.db import *
admin = Namespace('admin', description='Add/remove users and other user account and audience management endpoints')

newUserModel = admin.model('user',{
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password'),
    'clientid': fields.String(required=True, description='client id or aud'),
    'roles': fields.String(required=True, description='comma separated role list'),
    'email': fields.String(required=False, description='email address'),
    'mobile': fields.String(required=False, description='mobile number'),
    'ex1': fields.String(required=False, description='extended filed'),
    'ex2': fields.String(required=False, description='extended filed'),
    'ex3': fields.String(required=False, description='extended filed')
})


logger = logging.getLogger('admin')
@admin.route('/users')
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
            if 'admin' in rawjwt['roles'] and reqdata['clientid'] in rawjwt['uex1']:
                
                res = addUser(reqdata)
                
                return  res, 200

            else:
                return  {"msg": "Forbidden"}, 403
          except Exception as e:
              logger.error(e)
              return  {"msg": "Internal server error"}, 500


          

          

      @jwt_required
      def get(self):
            logger.info('health check get')
            return "working",200
