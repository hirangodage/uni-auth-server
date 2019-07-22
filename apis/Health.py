from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import  jwt_required
from flask import Flask,jsonify,request,flash,redirect,send_file
import logging

health = Namespace('health', description='Service availability and health check')
logger = logging.getLogger('health')
@health.route('/with-un-auth')
class MainService(Resource):
      def post(self):
            return "working",200
      def get(self):
            logger.info('health check get')
            return "working",200

@health.route('/with-auth')
class MainService(Resource):
      @jwt_required
      def post(self):
            return "working",200

      @jwt_required
      def get(self):
            logger.info('health check get')
            return "working",200
