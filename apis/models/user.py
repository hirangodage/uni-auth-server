from flask_restplus import Namespace, Resource, fields

def newUserModel(ns):
    return ns.model('user',{
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password'),
    'clientid': fields.String(required=True, description='client id or aud. this field is valid only for super admin'),
    'roles': fields.String(required=True, description='comma separated role list'),
    'tenant': fields.String(required=True, description='tenant name , valid only for super admin'),
    'email': fields.String(required=True, description='email address'),
    'mobile': fields.String(required=False, description='mobile number'),
    'ex1': fields.String(required=False, description='extended filed'),
    'ex2': fields.String(required=False, description='extended filed'),
    'ex3': fields.String(required=False, description='extended filed')
})


adminUser={
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password'),
    'email': fields.String(required=True, description='email address'),
    'mobile': fields.String(required=False, description='mobile number'),
    'ex1': fields.String(required=False, description='extended filed'),
    'ex2': fields.String(required=False, description='extended filed'),
    'ex3': fields.String(required=False, description='extended filed')
}

client={
    'name': fields.String(required=True, description='tenant name'),
    'des': fields.String(required=True, description='description'),
    'aud':fields.String(required=True, description='comma separated list of audiances'),
    'adminUser':fields.Nested({
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password'),
    'email': fields.String(required=True, description='email address'),
    'mobile': fields.String(required=False, description='mobile number'),
    'ex1': fields.String(required=False, description='extended filed'),
    'ex2': fields.String(required=False, description='extended filed'),
    'ex3': fields.String(required=False, description='extended filed'),
}),
    'ex1': fields.String(required=False, description='extended filed'),
    'ex2': fields.String(required=False, description='extended filed'),
    'ex3': fields.String(required=False, description='extended filed')
}

aud={
    'clientid': fields.String(required=True, description='client name'),
    'clientSecret': fields.String(required=True, description='client password'),
    'Expire': fields.String(required=True, description='token expire in - ms'),
    
    'ex1': fields.String(required=False, description='extended filed'),
    'ex2': fields.String(required=False, description='extended filed'),
    'ex3': fields.String(required=False, description='extended filed')
}