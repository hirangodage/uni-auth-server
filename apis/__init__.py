from flask_restplus import Api
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
api = Api(version='1.0', title='Unicorn authantication API',
    description='token server',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(health)



api.add_namespace(auth)