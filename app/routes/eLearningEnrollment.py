import json
from requests import get, put, post
from flask import request
from flask_restful import Resource
from app.utils.databaseconf import runQuery
from app.utils.databaseconf import runDelete
from app.utils.databaseconf import runMutationQuery
from app.utils.databaseconf import databaseConnector
from app.utils.authenticator import checkAuthenticator
from app.utils.querystringgenerator import queryStringGenerator
import psycopg2
from psycopg2 import connect, sql


class ELearningEnrollment(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from elearning_enrollment where "is_active" = true '
            countQuery = 'select count(id) from elearning_enrollment where "is_active" = true '

            if (not request.args.get('id_course') is None):
                query += ' AND "id_course" = \'' + \
                    request.args.get('id_course') + '\''
                countQuery += ' AND "id_course" = \'' + \
                    request.args.get('id_course') + '\''

            if (not request.args.get('date_filter') is None):
                query += ' AND created_date::date = \'' + \
                    request.args.get('date_filter') + '\''
                countQuery += ' AND created_date::date = \'' + \
                    request.args.get('date_filter') + '\''

            if (not request.args.get('status_filter') is None):
                query += ' AND "status_name" = \'' + \
                    request.args.get('status_filter') + '\''
                countQuery += ' AND "status_name" = \'' + \
                    request.args.get('status_filter') + '\''

            if (not request.args.get('general_filter') is None):
                query += ' AND "news_title" LIKE \'%' + \
                    request.args.get('general_filter') + '%\''
                countQuery += ' AND "news_title" LIKE \'%' + \
                    request.args.get('general_filter') + '%\''

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
        sql = """INSERT INTO elearning_enrollment(id_course, id_user, is_active, created_by, created_date, modified_by, modified_date) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        try:
            returnId = runMutationQuery(
                sql, (request.json['id_course'], request.json['id_user'], request.json['is_active'], request.json['created_by'], request.json['created_date'], request.json['modified_by'], request.json['modified_date']))
            data = runQuery(
                'SELECT * FROM elearning_enrollment where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500

    def put(self):
        sql = """UPDATE elearning_enrollment SET id_course = %s, id_user = %s, is_active = %s, created_by = %s, created_date = %s, modified_by = %s, modified_date = %s WHERE id = %s RETURNING id;"""
        try:
            returnId = runMutationQuery(
                sql, (request.json['id_course'], request.json['id_user'], request.json['is_active'], request.json['created_by'], request.json['created_date'], request.json['modified_by'], request.json['modified_date'], request.args.get('id')))
            data = runQuery(
                'SELECT * FROM elearning_enrollment where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return e, 500

    def delete(self):
        deleteQuery = """DELETE FROM elearning_enrollment WHERE "id" = %s;"""
        deleteQueryVideo = """DELETE FROM elearning_enrollment_video WHERE "id_topik" = %s;"""
        try:
            returnDelete = runDelete(deleteQuery, (request.args.get('id')))
            returnDeleteVideo = runDelete(
                deleteQueryVideo, (request.args.get('id')))
            return returnDelete
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500
