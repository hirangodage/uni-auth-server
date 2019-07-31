

ar=[{'Status': 1, 'Name': 'hiran', 'Email': 'hiran@tl.lk', 'Mobile': '12', 'Role': 'admin',
 'aud': 'admin', 'AudKey': 'test@key', 'Expire': 50000000, 'uex1': 'tl', 'uex2': None, 'uex3': None,
  'aex1': None, 'aex2': None, 'aex3': None}]
mo = map(lambda x:x['Role'],list(ar))
print(list(mo))