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

fieldView = '"id","subject", "description", "created_by", "modified_by", "created_date", "modified_date", "start_event", "end_event"'


class Calendar(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from v_cms_calendar where is_active = true '
            countQuery = 'select count(id) from v_cms_calendar where is_active = true'

            # if (not request.args.get('general_filter') is None):
            #     query += ' AND "username" LIKE \'%' + \
            #         request.args.get('general_filter') + '%\''
            #     countQuery += ' AND "username" LIKE \'%' + \
            #         request.args.get('general_filter') + '%\''

            # if (not request.args.get('order') is None and not request.args.get('dir') is None):
            #     query += ' ORDER BY "%s" %s ' % (
            #         request.args.get('order'), request.args.get('dir'))

            # if (not request.args.get('take') is None and not request.args.get('skip') is None):
            #     query += ' limit %d offset %d ' % (
            #         int(request.args.get('take')), int(request.args.get('skip')))

            data = runQuery(query)
            total = runQuery(countQuery)
            return {
                "data": data,
                "total": total[0]["count"]
            }
        except AssertionError as e:
            return e, 500

    def post(self):
        sql = """INSERT INTO cms_calendar(description, subject, created_by, modified_by, created_date, modified_date, start_event, end_event, is_active, all_day) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        try:
            returnId = runMutationQuery(sql, (request.json['description'], request.json['subject'],
                                              request.json['created_by'], request.json['modified_by'], request.json['created_date'],
                                              request.json['modified_date'], request.json['start_event'], request.json['end_event'], request.json['is_active'], request.json['all_day']))
            data = runQuery(
                'SELECT * FROM v_cms_calendar where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return e, 500

    def put(self):
        sql = """UPDATE cms_calendar SET description = %s, subject = %s, created_by = %s, modified_by = %s, created_date = %s, modified_date = %s, start_event = %s, end_event = %s, is_active = %s, all_day = %s WHERE id = %s RETURNING id;"""

        try:
            returnId = runMutationQuery(sql, (request.json['description'], request.json['subject'],
                                              request.json['created_by'], request.json['modified_by'], request.json['created_date'],
                                              request.json['modified_date'], request.json['start_event'], request.json['end_event'], request.json['is_active'], request.json['all_day'], request.args.get('id')))
            data = runQuery(
                'SELECT * FROM v_cms_calendar where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return e, 500
