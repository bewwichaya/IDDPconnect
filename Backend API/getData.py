import mysql.connector
import json
import datetime
import jwt
from register import databaseConnect
from flask import Flask, request, abort

def verifyUser(auth_key):
    secret = 'IDDPconnect'
    try:
        id = jwt.decode(auth_key,secret,algorithms=["HS256"])['id']
    except:
        id = None
    return id

def colleagueData(auth_key):
    id = verifyUser(auth_key)
    if id:
        connect = databaseConnect()
        cur = connect.cursor(dictionary=True)
        cur.execute(''' SELECT iddpyear FROM IDDPconnect.information
                WHERE id= %s'''%(id))
        iddpyear = cur.fetchone()['iddpyear']
        cur.execute(''' SELECT id,firstname,lastname,email,iddpyear,birthday FROM IDDPconnect.information
                WHERE iddpyear = '%s' '''%(iddpyear))
        data = cur.fetchall()
        return json.dumps({'data':data})
    else:
        abort(401, 'Authentication key is incorrect')

