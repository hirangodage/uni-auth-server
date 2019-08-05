from flask import Flask
from apis import api
from cheroot.wsgi import Server as WSGIServer,PathInfoDispatcher
from flask_jwt_extended import JWTManager, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
import logging
import os
from apis.db import *

LOGGINGFORMAT = '%(asctime)-15s %(levelname)-8s %(name)-8s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOGGINGFORMAT, datefmt='%d-%b-%y %H:%M:%S')

mapp=Flask(__name__)
mapp.secret_key = os.getenv('adminkey', 'test@key')


mapp.config['PROPAGATE_EXCEPTIONS'] = True

#mapp.config['JWT_SECRET_KEY']=mapp.secret_key
#mapp.config['JWT_DECODE_AUDIENCE']=os.getenv('adminaud', 'admin')
#mapp.config['JWT_ENCODE_AUDIENCE']='testapp'
api.init_app(mapp)


jwt = JWTManager(mapp)
#register error handlers (inbuilt)
jwt._set_error_handler_callbacks(api)

@jwt.decode_key_loader
def decode_key_loader_callback(claims,para2):
      if 'admin' in claims['aud']:
            mapp.config['JWT_DECODE_AUDIENCE']='admin'
            return os.getenv('adminkey', 'test@key')

      if 'admin' in claims['roles']:
            mapp.config['JWT_DECODE_AUDIENCE']=claims['aud'][0]
            return getClientSecret( claims['aud'][0])

      return ''
      

      




#host multiple instances
d=PathInfoDispatcher({'/':mapp})
server=WSGIServer(('0.0.0.0',8083),d)
#docker run -d -p 8088:8088 -t nginx
#start web server
try:
      server.start()
except KeyboardInterrupt:
      server.stop()