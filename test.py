import os
from apis.db import *
from itertools import groupby
from functools import reduce

print(os.getenv('testkey', 'default_value'))




lists = checkUser('hiran','test456','test')

grps = groupby(sorted(lists,key=lambda x:(x.Name,x.Email,x.Mobile,x.AudKey)), lambda x:(x.Name,x.Email,x.Mobile,x.AudKey))

for k,v in grps:
    xxx = list(v)
    newk= list(k)
   
    print(reduce(lambda x,y:x.Role+','+y.Role,xxx))
    print(newk)

