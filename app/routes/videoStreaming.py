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


class VideoStreaming(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from v_cms_video_streaming n where is_active = true '
            # query = 'select * from v_cms_video_streaming n where is_active = true and status_name = ' + "'Published'"
            countQuery = 'select count(id) from v_cms_video_streaming n where is_active = true '

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
                query += ' AND "title" LIKE \'%' + \
                    request.args.get('general_filter') + '%\''
                countQuery += ' AND "title" LIKE \'%' + \
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
        sql = """INSERT INTO cms_video_streaming(title, description, status_id, created_date, created_by, modified_date, modified_by, is_active, file_video,video_name) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s) RETURNING id;"""
        try:
            returnId = runMutationQuery(
                sql, (request.json['title'], request.json['description'], request.json['status_id'], request.json['created_date'], request.json['created_by'], request.json['modified_date'], request.json['modified_by'], request.json['is_active'], request.json['file_video'], request.json['video_name']))
            data = runQuery(
                'SELECT * FROM cms_video_streaming where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500

    def put(self):
        sql = """UPDATE cms_video_streaming SET title = %s, description = %s, status_id = %s, created_date = %s, created_by = %s, modified_date = %s, modified_by = %s, is_active = %s, file_video = %s, video_name= %s WHERE id = %s RETURNING id;"""
        try:
            returnId = runMutationQuery(
                sql, (request.json['title'], request.json['description'], request.json['status_id'], request.json['created_date'], request.json['created_by'], request.json['modified_date'], request.json['modified_by'], request.json['is_active'], request.json['file_video'], request.json['video_name'], request.args.get('id')))
            data = runQuery(
                'SELECT * FROM cms_video_streaming where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return e, 500
