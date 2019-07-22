from flask import Flask,jsonify, request
from apis.db import *
from itertools import groupby
from functools import reduce
import operator
from flask_restplus import Namespace, Resource, fields
import jwt  , datetime
import signal,logging,json
from flask_jwt_extended import (
     jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_claims, get_jwt_identity
)

logger = logging.getLogger('auth')
auth = Namespace('authantication', description='Authatication and authrization for all other modules')

tokenModel = auth.model('requestObject',{
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password'),
    'aud': fields.String(required=True, description='audience name')
})


def get_access_token(identity,expin,aud,key,roles):
    payload_access = {
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(milliseconds=expin),
                        'iat': datetime.datetime.utcnow(),
                        'nbf': datetime.datetime.utcnow(),
                        'identity': identity,
                        'aud':[aud],
                        "type": "access",
                        'roles':roles
                         }
                        
    access_token = jwt.encode(payload_access, key, algorithm='HS256')
    return access_token.decode()

@auth.route('/refresh')
class refresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        
        access_token = get_access_token(get_jwt_identity())
        return {'access_token': access_token},200
   # access_token = jwt.encode(payload_access, 'test-123', algorithm='HS256')


@auth.route('/token')
class tokenServer(Resource):
    @auth.expect(tokenModel, validate=True)
    @auth.doc(responses={
            200: 'Success',
        401: 'Authentication Error',
        403: 'Requested resource unavailable',
        409: 'Conflict, document already exists',
        422: 'Validation Error'
                  })
    def post(self):
        try:
            reqdata =  request.get_json()
            username =reqdata.get('username')
            password = reqdata.get('password')
            aud = reqdata.get('aud')
            logger.info(f'token request for user {username} and aud is {aud}')

            userState = checkUser(username,password,aud)
            if not userState:
                logger.info(f'invlaid aud for user {username}')
                return {'message':'invalid audience'},404
            
            if userState[0].Status == -1:
                logger.info(f'incorrect credentials {username}')
                return {'message':'incorrect username password'},404


            grps = groupby(sorted(userState,key=lambda x:(x.Name,x.Email,x.Mobile,x.AudKey,x.Expire)), lambda x:(x.Name,x.Email,x.Mobile,x.AudKey,x.Expire))
            roles=''
            audkey=''
            email=''
            mobile=''
            expire =0
            for k,v in grps:
                roles = reduce(lambda x,y:x.Role+','+y.Role,list(v))
                email = k[1]
                mobile = k[2]
                audkey = k[3]
                expire = int(k[4])

            
            access_token = get_access_token(username,expire,aud,audkey,roles)
            refresh_token =create_refresh_token(username)
            logger.info(f'token granted for user {username}')   
            return {'token_type': 'Bearer', 'expires_in': expire,'access_token': access_token, 
            'refresh_token': refresh_token},200

        except Exception as e:
            logger.info('username:'+username+'token request failed. check error log for more details.')
            logger.error(e)
            return {'message':'internal server error'},500
            



