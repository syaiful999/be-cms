import os
import json
from requests import get, put, post
from flask import request
from flask_restful import Resource
from app.utils.databaseconf import runQuery
from app.utils.databaseconf import runMutationQuery
from app.utils.databaseconf import databaseConnector
from app.utils.authenticator import checkAuthenticator
from app.utils.querystringgenerator import queryStringGenerator
import psycopg2
from psycopg2 import connect, sql
import bcrypt
import jwt


class Auth(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from v_cms_user u where is_active = true '
            countQuery = 'select count(user_id) from v_cms_user c where is_active = true'

            data = runQuery(query)
            total = runQuery(countQuery)
            return {
                "data": data,
                "total": total[0]["count"]
            }
        except AssertionError as e:
            return e, 500

    def post(self):
        try:
            query = 'select * from v_cms_user u where is_active = true '
            countQuery = 'select count(user_id) from v_cms_user c where is_active = true'

            if not request.json['name'] is None:
                query += ' AND username = \'' + request.json['name'] + '\''
                countQuery += ' AND username = \'' + \
                    request.json['name'] + '\''

            data = runQuery(query)
            total = runQuery(countQuery)

            message = "Login failed"
            status = 401
            token = None
            if (total[0]["count"] > 0):
                if bcrypt.checkpw(request.json['password'].encode('utf8'),
                                  data[0]["password"].encode('utf-8')):
                    message = "Login success!"
                    status = 200
                    encodedData = {
                        "username": data[0]["fullname"],
                        "password": data[0]["password"],
                        "user_photo_1": data[0]["profile_photo"],
                        "user_account": data[0]["id"],
                        "role_id": data[0]["role_id"]
                    }
                    secretKey = os.getenv('TOKEN_SECRET_KEY')
                    token = jwt.encode(encodedData, secretKey,
                                       algorithm='HS256').decode('UTF-8')
            else:
                print("It Does not Match :(")

            return {
                "message": message,
                "status": status,
                "token": token
            }
        except AssertionError as e:
            return 500

    def put(self):
        sql = """UPDATE cms_user SET role_id = %s, user_type_id = %s, username = %s, fullname = %s, email = %s, profile_photo = %s, post_count = %s, created_by = %s, created_date = %s, modified_by = %s, modified_date = %s, is_active = %s WHERE id = %s RETURNING id;"""
        try:
            returnId = runMutationQuery(sql, (request.json['role_id'], request.json['user_type_id'], request.json['username'],
                                              request.json['fullname'], request.json['email'], request.json['profile_photo'],
                                              request.json['post_count'], request.json['created_by'], request.json['created_date'],
                                              request.json['modified_by'], request.json['modified_date'], request.json['is_active'], request.args.get('id')))
            data = runQuery(
                'SELECT * FROM v_cms_user where user_id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return e, 500
