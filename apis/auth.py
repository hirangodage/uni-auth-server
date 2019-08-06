from flask import Flask,jsonify, request
from apis.db import *
from os import getenv
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
auth = Namespace('oauth', description='List of end points that use to retrive access token for all audience')

tokenModel = auth.model('tokenRequest',{
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password'),
    'aud': fields.String(required=True, description='ClientID'),
    'tenant': fields.String(required=True, description='company name')
})


def get_access_token(identity,expin,aud,key,roles,uex1,uex2,uex3,aex1,aex2,aex3,tenant):
    payload_access = {
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(milliseconds=expin),
                        'iat': datetime.datetime.utcnow(),
                        'nbf': datetime.datetime.utcnow(),
                        'iss' : getenv('tokenissuer'),
                        'identity': identity,
                        'aud':[aud],
                        'tenant':tenant,
                        "type": "access",
                        'roles':roles
                         }
    if uex1:
        payload_access['uex1']  = uex1

    if uex2:
        payload_access['uex2']  = uex2

    if uex3:
        payload_access['uex3']  = uex3

    if aex1:
        payload_access['aex1']  = aex1

    if aex2:
        payload_access['aex2']  = aex2

    if aex3:
        payload_access['aex3']  = aex3

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
            tenant = reqdata.get('tenant')
            logger.info(f'token request for user {username} and aud is {aud}')

            userState = checkUser(username,password,aud,tenant)
            if not userState:
                logger.info(f'invlaid aud for user {username}')
                return {'message':'invalid audience'},404
            
            if userState[0]['Status'] == -1:
                logger.info(f'incorrect credentials {username}')
                return {'message':'incorrect username password'},404


            grps = groupby(sorted(userState,key=lambda x:(x['Name'],x['Email'],x['Mobile'],x['AudKey'],
            x['Expire'],x['uex1'],x['uex2'],x['uex3'],x['aex1'],x['aex2'],x['aex3'])), lambda x:(
                x['Name'],x['Email'],x['Mobile'],x['AudKey'],x['Expire'],x['uex1'],x['uex2'],
                x['uex3'],x['aex1'],x['aex2'],x['aex3']))

               
            roles=''
            audkey=''
            email=''
            mobile=''
            expire =0
            uex1=''
            uex2=''
            uex3=''
            aex1=''
            aex2=''
            aex3=''
            for k,v in grps:
                
                roles = list(map(lambda x:x['Role'],list(v)))
                email = k[1]
                mobile = k[2]
                audkey = k[3]
                expire = int(k[4])
                uex1 = k[5]
                uex2 = k[6]
                uex3 = k[7]
                aex1 = k[8]
                aex2 = k[9]
                aex3 = k[10]

            
            access_token = get_access_token(username,expire,aud,audkey,roles,uex1,uex2,uex3,aex1,aex2,aex3,tenant)
            refresh_token =create_refresh_token(username)
            logger.info(f'token granted for user {username}')   
            return {'token_type': 'Bearer', 'expires_in': expire,'access_token': access_token, 
            'refresh_token': refresh_token},200

        except Exception as e:
            logger.info('username:'+username+'token request failed. check error log for more details.')
            logger.error(e)
            return {'message':'internal server error'},500
            



