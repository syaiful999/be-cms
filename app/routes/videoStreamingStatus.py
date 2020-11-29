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


class VideoStreamingStatus(Resource):
    def __init__(self):
        isAuth = checkAuthenticator(request.headers["Authorization"])
        if not isAuth:
            raise TypeError('UNAUTHORIZED')

    def get(self):
        try:
            queryStringData = queryStringGenerator(request.args)
            query = 'select * from cms_config_video_streaming_status r ' + queryStringData
            data = runQuery(query)
            total = runQuery(
                'select count(id) from cms_config_video_streaming_status r ' + queryStringData)
            return {
                "data": data,
                "total": total[0]["count"]
            }
        except AssertionError as e:
            return e, 500
