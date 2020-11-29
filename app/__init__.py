""" init server and route. """

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from app.routes.root import RootRoute
from app.routes.user import User
from app.routes.role import Role
from app.routes.auth import Auth
from app.routes.employee import Employee
from app.routes.newsCategory import NewsCategory
from app.routes.newsTag import NewsTag
from app.routes.news import News
from app.routes.newsTagTransact import NewsTagTransact
from app.routes.newsStatus import NewsStatus
from app.routes.videoStreaming import VideoStreaming
from app.routes.videoStreamingStatus import VideoStreamingStatus
from app.routes.training import Training
from app.routes.calendar import Calendar
from app.routes.eLearning import ELearning
from app.routes.eLearningTopic import ELearningTopic
from app.routes.eLearningTopicVideo import ELearningTopicVideo
from app.routes.eLearningEnrollment import ELearningEnrollment
from app.routes.userEnrollment import userEnrollment
from app.routes.enrollmentTransact import EnrollmentTransact

app = Flask(__name__)
api = Api(app)


def init_route(server):
    '''Nothing returned, add route for API'''
    server.add_resource(RootRoute, '/')
    server.add_resource(User, '/user')
    server.add_resource(Role, '/role')
    server.add_resource(Auth, '/auth')
    server.add_resource(Employee, '/employee')
    api.add_resource(NewsCategory, '/news-category')
    api.add_resource(NewsTag, '/news-tag')
    api.add_resource(News, '/news')
    api.add_resource(NewsTagTransact, '/news-transact')
    api.add_resource(NewsStatus, '/news-status')
    api.add_resource(VideoStreaming, '/video-streaming')
    api.add_resource(VideoStreamingStatus, '/video-streaming-status')
    api.add_resource(Training, '/training')
    api.add_resource(Calendar, '/calendar')
    api.add_resource(ELearning, '/elearning')
    api.add_resource(ELearningTopic, '/elearning-topic')
    api.add_resource(ELearningTopicVideo, '/elearning-video')
    api.add_resource(ELearningEnrollment, '/elearning-enroll')
    api.add_resource(userEnrollment, '/user-enrollment')
    api.add_resource(EnrollmentTransact, '/transactEnrollment')

CORS(app)
init_route(api)
