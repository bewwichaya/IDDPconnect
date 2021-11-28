import mysql.connector
import json
import bcrypt
import datetime
import jwt
from flask import Flask, request, abort


def databaseConnect():
    endpoint = 'iddpconnect.cu5xkm7t9rel.ap-southeast-1.rds.amazonaws.com'
    username = 'admin'
    password = '0818089078'
    database_name = 'IDDPconnect'
    return mysql.connector.connect(host=endpoint, user=username, password=password)

def registerCheck(params):
    text = 'passsssss'
    username = params['username']
    email = params['email']
    connect = databaseConnect()
    cur = connect.cursor()
    cur.execute('''
        SELECT * FROM IDDPconnect.account
        WHERE username='%s' or email='%s'
        '''%(username,email))

    data=cur.fetchall()
    data=list(data)
    if data == []:
        text = 'ok'
    else:
        cur.execute('''
        SELECT * FROM IDDPconnect.account
       WHERE username='%s'
        '''%(username))
        data=list(cur.fetchall())
        if data==[]:
            message='email is already register'
            abort(401, message)
        else:
            message='username is already register'
            abort(401, message)
    connect.close()
    return text

def registerCreate(params):
    username=params['username']
    password=params['password']
    email=params['email']
    iddpYear=params['iddpYear']
    firstname=params['firstName']
    lastname=params['lastName']
    birthday=params['birthDay']

    time=datetime.datetime.now()+datetime.timedelta(hours=7)
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode(), salt).decode()
    salt=salt.decode()
    connect = databaseConnect()
    cur = connect.cursor()
    cur.execute( '''
                    INSERT INTO IDDPconnect.account(username,email,salt,hash,time_create)
                    VALUES('%s','%s','%s','%s','%s')
                    '''%(username,email,salt,hash[29:],time))
    cur.execute( '''
                    SELECT id,username FROM IDDPconnect.account
                    WHERE username='%s' AND email='%s'
                    '''%(username,email))
    id=cur.fetchone()
    id=(list(id)[0])
    cur.execute( '''
                    INSERT INTO IDDPconnect.information(login_id,firstname,lastname,email,iddpyear,birthday)
                    VALUES('%s','%s','%s','%s','%s','%s')
                    '''%(id,firstname,lastname,email,iddpYear,birthday))
    connect.commit()
    connect.close()
    text = 'ok'
    return text

def login(params):
    secret='IDDPconnect'
    username = params['username']
    password = params['password']

    connect = databaseConnect()
    cur = connect.cursor(dictionary=True)
    cur.execute('''
                SELECT * FROM IDDPconnect.account
                WHERE username='%s'
    '''%(username))
    data=cur.fetchone()
    if data==None:
        abort(401, 'Username incorrect')
    else:
        hashed=data['salt']+data['hash']
        hashed=hashed.encode()
        if bcrypt.checkpw(password.encode(),hashed):
            id=data['id']
            cur.execute('''
                SELECT * FROM IDDPconnect.information
                WHERE login_id=%s
                ORDER BY id DESC
                LIMIT 1 '''%(id))
            data=cur.fetchone()
            del data['id']
            del data['login_id']
            encoded_jwt = jwt.encode({"id": id}, secret, algorithm="HS256")
        else:
            abort(401, 'Password incorrect')
    cur.close()
    text={'auth':encoded_jwt,'data':data}
    return json.dumps(text)
