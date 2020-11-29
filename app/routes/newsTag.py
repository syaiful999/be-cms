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
from flask import jsonify


class NewsTag(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from cms_news_tag u where is_active = true ORDER BY tag_name ASC'
            countQuery = 'select count(id) from cms_news_tag c where is_active = true'
            data = runQuery(query)
            total = runQuery(countQuery)
            return {
                "data": data,
                "total": total[0]["count"]
            }
        except AssertionError as e:
            return e, 500

    def post(self):
        sql = """INSERT INTO cms_news_tag(tag_name, is_active) VALUES(%s, %s) RETURNING id;"""
        try:
            isExist = runQuery(
                'SELECT * FROM cms_news_tag where UPPER(tag_name) = \'%s\'' % request.json['tag_name'].upper())
            if (isExist):
                return jsonify(
                    http_code=409,
                    message='Data is already exist'
                )
            else:
                returnId = runMutationQuery(
                    sql, (request.json['tag_name'], request.json['is_active']))
                data = runQuery(
                    'SELECT * FROM cms_news_tag where id = %s' % returnId)
                return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500
