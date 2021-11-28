import requests
import json
header={'content-type':'application/json','auth':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.vFS2F3sz2K7Y7zYPEFWJt7_OCpgxF4QQZ9bOGehguFg'}
data1 = json.dumps({    'username':'bewwichaya123',
                        'email':'wichaya.kita@gmail.comasd',
                        'password':'Hello'})

data2 = json.dumps({    'username':'bewwichaya123',
                        'password':'0895591901',
                        'email':'wichaya.kita@gmail.comasd',
                        'iddpYear':'17',
                        'firstName':'earth',
                        'lastName':'earthhhh',
                        'birthDay':'15/02/1997'})

data3=json.dumps({      'username':'bewwichaya',
                        'password':'01808907822'})

data4=json.dumps({      'auth':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.vFS2F3sz2K7Y7zYPEFWJt7_OCpgxF4QQZ9bOGehguFg'})


#r = requests.post("http://127.0.0.1:5000/colleague",data=data4,headers=header)

r = requests.get("http://127.0.0.1:5000/colleague",headers=header)

print(r)
print(r.status_code)
print(r.json())