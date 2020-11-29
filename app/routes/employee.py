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


class Employee(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from master_system_user u where is_active = true and field_user_type_id = 1'
            countQuery = 'select count(id) from master_system_user c where is_active = true and field_user_type_id = 1'

            if (not request.args.get('name') is None):
                query += ' AND UPPER(name) LIKE \'%' + \
                    request.args.get('name').upper() + '%\''
                countQuery += ' AND UPPER(name) LIKE \'%' + \
                    request.args.get('name').upper() + '%\''

            data = runQuery(query)
            total = runQuery(countQuery)
            return {
                "data": data,
                "total": total[0]["count"]
            }
        except AssertionError as e:
            return e, 500
