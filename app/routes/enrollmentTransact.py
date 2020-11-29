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


class EnrollmentTransact(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from v_user_enrollment_transact n where 1=1 '
            countQuery = 'select count(id) from v_user_enrollment_transact n where 1=1 '
            queryTopik = 'select id from v_user_enrollment_transact n where 1=1 '

            if (not request.args.get('id_course') is None):
                query += ' AND "id_course" = \'' + \
                    request.args.get('id_course') + '\''
                countQuery += ' AND "id_course" = \'' + \
                    request.args.get('id_course') + '\''
                queryTopik += ' AND "id_course" = \'' + \
                    request.args.get('id_course') + '\''
                    
            if (not request.args.get('id_user') is None):
                query += ' AND "id_user" = \'' + \
                    request.args.get('id_user') + '\''
                countQuery += ' AND "id_user" = \'' + \
                    request.args.get('id_user') + '\''
                queryTopik += ' AND "id_user" = \'' + \
                    request.args.get('id_user') + '\''
            
            if (not request.args.get('id_topik') is None):
                queryTopik += ' AND "id_topik" = \'' + \
                    request.args.get('id_topik') + '\''
            # if (not request.args.get('status_filter') is None):
            #     query += ' AND "status_name" = \'' + \
            #         request.args.get('status_filter') + '\''
            #     countQuery += ' AND "status_name" = \'' + \
            #         request.args.get('status_filter') + '\''

            # if (not request.args.get('general_filter') is None):
            #     query += ' AND "id_topik" LIKE \'%' + \
            #         request.args.get('general_filter') + '%\''
            #     countQuery += ' AND "id_topik" LIKE \'%' + \
            #         request.args.get('general_filter') + '%\''

            if (not request.args.get('order') is None and not request.args.get('dir') is None):
                query += ' ORDER BY "%s" %s ' % (
                    request.args.get('order'), request.args.get('dir'))

            if (not request.args.get('take') is None and not request.args.get('skip') is None):
                query += ' limit %d offset %d ' % (
                    int(request.args.get('take')), int(request.args.get('skip')))

            data = runQuery(query)
            total = runQuery(countQuery)
            dataTopic = runQuery(queryTopik)
            return {
                "data": data,
                "total": total[0]["count"],
                "dataTopik": dataTopic
            }
        except AssertionError as e:
            return e, 500

    def post(self):
        sql = """INSERT INTO user_enrollment_transact(id_user, id_topik, id_course, time_spend, status) VALUES(%s, %s, %s, %s, %s ) RETURNING id;"""
        try:
            returnId = runMutationQuery(
                sql, (request.json['id_user'], request.json['id_topik'], request.json['id_course'], request.json['time_spend'], request.json['status']))
            print((request.json['id_user'], request.json['id_topik'], request.json['id_course'], request.json['time_spend'], request.json['status']))
            data = runQuery(
                'SELECT * FROM user_enrollment_transact where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500

    def put(self):
        sql = """UPDATE user_enrollment_transact SET time_spend= %s, status = %s WHERE id_topik = %s RETURNING id;"""
        try:
            returnId = runMutationQuery(
                sql, (request.json['time_spend'],request.json['status'], request.json['id_topik']))
            data = runQuery(
                'SELECT * FROM user_enrollment_transact where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500
