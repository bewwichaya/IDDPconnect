from flask import Flask, request, abort
from flask_restful import Api,Resource

from register import databaseConnect

app = Flask(__name__)
api =Api(app)

       

class registerCheck(Resource):
    def post(self):
        from register import registerCheck
        message = registerCheck(request.json)
        return {'message':message}

class registerCreate(Resource):
    def post(self):
        from register import registerCreate
        message = registerCreate(request.json)
        return {'message':message}

class login(Resource):
    def post(self):
        from register import login
        data = login(request.json)
        return data

class colleague(Resource):
    def get(self):
        from getData import colleagueData
        auth = request.headers['auth']
        data = colleagueData(auth)
        return data


api.add_resource(registerCheck,"/registercheck")
api.add_resource(registerCreate,"/registercreate")
api.add_resource(login,"/login")
api.add_resource(colleague,"/colleague")


if __name__ =="__main__":
    app.run(debug=True)
