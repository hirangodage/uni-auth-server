from flask import Flask,jsonify, request
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
    'username': fields.String(required=True, description='username that given by the service provider'),
    'password': fields.String(required=True, description='password that given by the service provider')
})


def get_access_token(identity):
    payload_access = {
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(milliseconds=50000),
                        'iat': datetime.datetime.utcnow(),
                        'nbf': datetime.datetime.utcnow(),
                        'identity': identity,
                        'aud':['testapp','testapp2'],
                        "type": "access"
                         }
    access_token = jwt.encode(payload_access, 'test-123', algorithm='HS256')
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

           
            if username == password:

                access_token = get_access_token(username)
                refresh_token =create_refresh_token(username)


                return {'token_type': 'Bearer', 'expires_in': 50000,'access_token': access_token.decode(), 
                'refresh_token': refresh_token.decode()},200
            else:
                return {'message':'incorrect username password'},404
        except Exception as e:
            return {'message':e}
            



