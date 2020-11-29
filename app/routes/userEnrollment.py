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


class userEnrollment(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from v_elearning_enrollment n where is_active = true '
            countQuery = 'select count(id) from v_elearning_enrollment n where is_active = true '
            queryAll = 'select n.id_course from elearning_enrollment n where "is_active" = true '
            queryAllTopic = 'select count(status) from v_user_enrollment_transact n where 1=1 '
            queryAllTopicDone = 'select count(status) from v_user_enrollment_transact n where "status" = true '

            if (not request.args.get('id_user') is None):
                query += ' AND "id_user" = \'' + \
                    request.args.get('id_user') + '\''
                countQuery += ' AND "id_user" = \'' + \
                    request.args.get('id_user') + '\''
                queryAll += ' AND "id_user" = \'' + \
                    request.args.get('id_user') + '\''
                queryAllTopic += ' AND "id_user" = \'' + \
                    request.args.get('id_user') + '\''
                queryAllTopicDone += ' AND "id_user" = \'' + \
                    request.args.get('id_user') + '\''

            if (not request.args.get('order') is None and not request.args.get('dir') is None):
                query += ' ORDER BY "%s" %s ' % (
                    request.args.get('order'), request.args.get('dir'))

            if (not request.args.get('take') is None and not request.args.get('skip') is None):
                query += ' limit %d offset %d ' % (
                    int(request.args.get('take')), int(request.args.get('skip')))

            data = runQuery(query)
            total = runQuery(countQuery)
            getAll = runQuery(queryAll)
            getAllTopic = runQuery(queryAllTopic)
            getAllTopicDone = runQuery(queryAllTopicDone)
            return {
                "data": data,
                "getAll": getAll,
                "getAllTopic": getAllTopic[0]["count"],
                "getAllTopicDone": getAllTopicDone[0]["count"],
                "total": total[0]["count"]
            }
        except AssertionError as e:
            return e, 500

    # def post(self):
    #     sql = """INSERT INTO cms_elearning(pemateri_name, name_course, no_course, created_date, created_by, modified_date, modified_by, is_active) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
    #     try:
    #         returnId = runMutationQuery(
    #             sql, (request.json['pemateri_name'], request.json['name_course'], request.json['no_course'], request.json['created_date'], request.json['created_by'], request.json['modified_date'], request.json['modified_by'], request.json['is_active']))
    #         data = runQuery(
    #             'SELECT * FROM cms_elearning where id = %s' % returnId)
    #         return data
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print(error)
    #         return error, 500

    # def put(self):
    #     sql = """UPDATE cms_elearning SET pemateri_name = %s, name_course = %s, no_course = %s, created_date = %s, created_by = %s, modified_date = %s, modified_by = %s, is_active = %s WHERE id = %s RETURNING id;"""
    #     try:
    #         returnId = runMutationQuery(
    #             sql, (request.json['pemateri_name'], request.json['name_course'], request.json['no_course'], request.json['created_date'], request.json['created_by'], request.json['modified_date'], request.json['modified_by'], request.json['is_active'], request.args.get('id')))
    #         data = runQuery(
    #             'SELECT * FROM cms_elearning where id = %s' % returnId)
    #         return data
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print(error)
    #         return e, 500
