from flask_restplus import Api
from flask import url_for
from apis.Health import health
from apis.auth import auth
from apis.admin import admin


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'authorization',
        'description': 'Enter your bearer token in the format **Bearer &lt;token>**'
    }
}

class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'http' if '8083' in self.base_url else 'https'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)



api = MyApi(version='1.0', title='Unicorn authantication API',
    description='The Authentication API enables you to manage all aspects of user identity when you use any Unicorn product and services. It offers endpoints so your users can log in, sign up, log out, access APIs, and more.',
    authorizations=authorizations,
    security='apikey',
    doc='/'
)

api.add_namespace(health)



api.add_namespace(auth)

api.add_namespace(admin)