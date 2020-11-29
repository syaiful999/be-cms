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


class ELearningTopic(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            query = 'select * from cms_elearning_topic n where 1 = 1 '
            countQuery = 'select count(id) from cms_elearning_topic n where 1 = 1 '

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
        sql = """INSERT INTO cms_elearning_topic(id_course, judul_topik, deskripsi) VALUES(%s, %s, %s) RETURNING id;"""
        try:
            returnId = runMutationQuery(
                sql, (request.json['id_course'], request.json['judul_topik'], request.json['deskripsi']))
            data = runQuery(
                'SELECT * FROM cms_elearning_topic where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500

    def put(self):
        sql = """UPDATE cms_elearning_topic SET id_course = %s, judul_topik = %s, deskripsi = %s WHERE id = %s RETURNING id;"""
        try:
            returnId = runMutationQuery(
                sql, (request.json['id_course'], request.json['judul_topik'], request.json['deskripsi'], request.args.get('id')))
            data = runQuery(
                'SELECT * FROM cms_elearning_topic where id = %s' % returnId)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return e, 500

    def delete(self):
        deleteQuery = """DELETE FROM cms_elearning_topic WHERE "id" = %s;"""
        deleteQueryVideo = """DELETE FROM cms_elearning_topic_video WHERE "id_topik" = %s;"""
        try:
            returnDelete = runDelete(deleteQuery, (request.args.get('id')))
            returnDeleteVideo = runDelete(
                deleteQueryVideo, (request.args.get('id')))
            return returnDelete
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error, 500
