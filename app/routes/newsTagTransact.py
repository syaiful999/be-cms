import json
from requests import get, put, post
from flask import request
from flask_restful import Resource
from app.utils.databaseconf import runQuery
from app.utils.databaseconf import runMutationQuery
from app.utils.databaseconf import runDelete
from app.utils.databaseconf import databaseConnector
from app.utils.authenticator import checkAuthenticator
from app.utils.querystringgenerator import queryStringGenerator
import psycopg2
from psycopg2 import connect, sql


class NewsTagTransact(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from v_cms_transact_news_tag n where 1 = 1'
            countQuery = 'select count(news_id) from v_cms_transact_news_tag n where 1 = 1'

            if (not request.args.get('news_id') is None):
                query += ' AND "news_id" = \'' + \
                    request.args.get('news_id') + '\''
                countQuery += ' AND "news_id" = \'' + \
                    request.args.get('news_id') + '\''

            data = runQuery(query)
            total = runQuery(countQuery)
            return {
                "data": data,
                "total": total[0]["count"]
            }
        except AssertionError as e:
            return e, 500

    def post(self):
        sql = """INSERT INTO cms_transact_news_tag(news_id, tag_id) VALUES(%s, %s) RETURNING news_id;"""
        deleteQuery = """DELETE %s, %s) RETURNING news_id;"""
        try:
            returnId = runMutationQuery(
                sql, (request.json['news_id'], request.json['tag_id']))
            data = runQuery(
                'SELECT * FROM cms_transact_news_tag where news_id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500

    def delete(self):
        deleteQuery = """DELETE FROM cms_transact_news_tag WHERE "news_id" = %s;"""
        try:
            returnDelete = runDelete(
                deleteQuery, (request.args.get('news_id')))
            return returnDelete
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500

    def put(self):
        sql = """UPDATE cms_news_category SET field_user_id = %s, role_id = %s, user_type_id = %s, username = %s, fullname = %s, email = %s, profile_photo = %s, post_count = %s, created_by = %s, created_date = %s, modified_by = %s, modified_date = %s, is_active = %s WHERE id = %s RETURNING id;"""
        try:
            returnId = runMutationQuery(sql, (request.json['field_user_id'], request.json['role_id'], request.json['user_type_id'], request.json['username'],
                                              request.json['fullname'], request.json['email'], request.json['profile_photo'],
                                              request.json['post_count'], request.json['created_by'], request.json['created_date'],
                                              request.json['modified_by'], request.json['modified_date'], request.json['is_active'], request.args.get('id')))
            data = runQuery(
                'SELECT * FROM cms_news_category where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return e, 500
