import json
from requests import get, put, post
from flask import request
from flask_restful import Resource
from app.utils.databaseconf import runQuery
from app.utils.authenticator import checkAuthenticator
from app.utils.querystringgenerator import queryStringGenerator

fieldView = '"id", "room_no", "is_active", "created_date"'
class RootRoute(Resource):
    def __init__(self):
      isAuth = checkAuthenticator(request.headers["Authorization"])
      if not isAuth:
        raise TypeError('UNAUTHORIZED')

    def get(self):
      try:
        queryStringData = queryStringGenerator(request.args)
        query = 'select ' + fieldView + ' from master_room mr ' + queryStringData
        data = runQuery(query)
        return data
      except AssertionError as e:
        return e, 500

    def post(self):
        return request.json

    def put(self, param):
        return param
