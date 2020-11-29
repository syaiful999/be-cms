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


class News(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from v_cms_news n where is_active = true '
            countQuery = 'select count(id) from v_cms_news n where is_active = true '

            if (not request.args.get('category') is None):
                query += ' AND "news_category_id" = \'' + \
                    request.args.get('category') + '\''
                countQuery += ' AND "news_category_id" = \'' + \
                    request.args.get('category') + '\''

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
        sql = """INSERT INTO cms_news(news_title, news_content, news_category_id, is_quote, is_highlight, status_id, created_date, created_by, modified_date, modified_by, is_active, news_image, news_image_2, news_image_3, file_image) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        try:
            returnId = runMutationQuery(
                sql, (request.json['news_title'], request.json['news_content'], request.json['news_category_id'], request.json['is_quote'], request.json['is_highlight'], request.json['status_id'], request.json['created_date'], request.json['created_by'], request.json['modified_date'], request.json['modified_by'], request.json['is_active'], request.json['news_image'], request.json['news_image_2'], request.json['news_image_3'], request.json['file_image']))
            data = runQuery(
                'SELECT * FROM cms_news where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500

    def put(self):
        sql = """UPDATE cms_news SET news_title = %s, news_content = %s, news_category_id = %s, is_quote = %s, is_highlight = %s, status_id = %s, created_date = %s, created_by = %s, modified_date = %s, modified_by = %s, is_active = %s, news_image = %s, news_image_2 = %s, news_image_3 = %s, file_image = %s WHERE id = %s RETURNING id;"""
        try:
            returnId = runMutationQuery(
                sql, (request.json['news_title'], request.json['news_content'], request.json['news_category_id'], request.json['is_quote'], request.json['is_highlight'], request.json['status_id'], request.json['created_date'], request.json['created_by'], request.json['modified_date'], request.json['modified_by'], request.json['is_active'], request.json['news_image'], request.json['news_image_2'], request.json['news_image_3'], request.json['file_image'], request.args.get('id')))
            data = runQuery(
                'SELECT * FROM cms_news where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return e, 500
