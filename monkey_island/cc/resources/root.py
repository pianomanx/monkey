from datetime import datetime

from flask import request
import flask_restful

from cc.database import mongo

from cc.utils import init_collections

__author__ = 'Barak'


class Root(flask_restful.Resource):
    def get(self, action=None):
        if not action:
            action = request.args.get('action')
        if not action:
            return {
                'status': 'OK',
                'mongo': str(mongo.db),
            }
        elif action == "reset":
            mongo.db.config.drop()
            mongo.db.monkey.drop()
            mongo.db.telemetry.drop()
            mongo.db.usernames.drop()
            mongo.db.passwords.drop()
            mongo.db.node.drop()
            mongo.db.edge.drop()
            init_collections()
            return {
                'status': 'OK',
            }
        elif action == "killall":
            mongo.db.monkey.update({}, {'$set': {'config.alive': False, 'modifytime': datetime.now()}}, upsert=False,
                                   multi=True)
            return {
                'status': 'OK',
            }
        else:
            return {'status': 'BAD',
                    'reason': 'unknown action'}
