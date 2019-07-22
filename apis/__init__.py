from flask_restplus import Api
from flask import url_for
from apis.Health import health
from apis.auth import auth


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
        scheme = 'https' if '443' in self.base_url else 'http'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)



api = MyApi(version='1.0', title='Unicorn authantication API',
    description='token server',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(health)



api.add_namespace(auth)