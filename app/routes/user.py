import json
import bcrypt
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




fieldView = '"user_id", "role_id", "user_type_id", "username", "fullname", "email", "profile_photo", "post_count", "created_by", "created_date", "modified_by", "modified_date"'


class User(Resource):
 
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from v_cms_user u where is_active = true '
            countQuery = 'select count(user_id) from v_cms_user c where is_active = true'

            if (not request.args.get('general_filter') is None):
                query += ' AND "username" LIKE \'%' + \
                    request.args.get('general_filter') + '%\''
                countQuery += ' AND "username" LIKE \'%' + \
                    request.args.get('general_filter') + '%\''

            if (not request.args.get('role_filter') is None):
                query += ' AND "role_name" LIKE \'%' + \
                    request.args.get('role_filter') + '%\''
                countQuery += ' AND "role_name" LIKE \'%' + \
                    request.args.get('role_filter') + '%\''

            if (not request.args.get('order') is None and not request.args.get('dir') is None):
                query += ' ORDER BY "%s" %s ' % (
                    request.args.get('order'), request.args.get('dir'))

            if (not request.args.get('take') is None and not request.args.get('skip') is None):
                query += ' limit %d offset %d ' % (
                    int(request.args.get('take')), int(request.args.get('skip')))

            data = runQuery(query)
            total = runQuery(countQuery)
            return {
                "data": data,
                "total": total[0]["count"]
            }
        except AssertionError as e:
            return e, 500

    def post(self):
        sql = """INSERT INTO cms_user(role_id, dob, phone_no, address, username, fullname, email, profile_photo, real_password, password, created_by, created_date, modified_by, modified_date, is_active) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s) RETURNING id;"""
        try:
            returnId = runMutationQuery(sql, (request.json['role_id'],request.json['dob'],request.json['phone_no'],request.json['address'],request.json['username'],
                                              request.json['fullname'], request.json['email'], request.json['profile_photo'],
                                              request.json['password'],bcrypt.hashpw(request.json['password'].encode('utf8'), bcrypt.gensalt(10)).decode("utf8"),
                                              request.json['created_by'], request.json['created_date'],
                                              request.json['modified_by'], request.json['modified_date'], request.json['is_active']))
            data = runQuery(
                'SELECT * FROM v_cms_user where user_id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500

    def put(self):
        sql = """UPDATE cms_user SET address = %s, role_id = %s, phone_no = %s, dob = %s, username = %s, fullname = %s, email = %s, profile_photo = %s, real_password = %s, password = %s, created_by = %s, created_date = %s, modified_by = %s, modified_date = %s, is_active = %s WHERE id = %s RETURNING id;"""
        try:
            returnId = runMutationQuery(sql, (request.json['address'], request.json['role_id'], request.json['phone_no'],request.json['dob'], request.json['username'],
                                              request.json['fullname'], request.json['email'], request.json['profile_photo'],request.json['password'],
                                              bcrypt.hashpw(request.json['password'].encode('utf8'), bcrypt.gensalt(10)).decode("utf8"), request.json['created_by'], request.json['created_date'],
                                              request.json['modified_by'], request.json['modified_date'], request.json['is_active'], request.args.get('id')))
            data = runQuery(
                'SELECT * FROM v_cms_user where user_id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500
