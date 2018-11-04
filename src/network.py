import ProcessUser
import ProcessPDF


#!/usr/bin/env python3


from flask import Flask, session, request, render_template, jsonify, redirect, url_for
from flask_restful import Api, Resource, reqparse
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import eventlet
from pymongo import MongoClient
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
import bcrypt
import requests
from flask_cors import CORS
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)
api = Api(app)
socketio = SocketIO(app)

ID = 0
        
@app.route('/savepoints', methods=['POST'])
def detectPattern():
    if request.method == 'POST':
        clickpoints = []
        clickpoints.append(request.json.get('x1', None)/100)
        clickpoints.append(request.json.get('y1', None)/100)
        clickpoints.append(request.json.get('x2', None)/100)
        clickpoints.append(request.json.get('y2', None)/100)
        pageNum = request.json.get('pageNum', None)
        fileName = request.json.get('fileName', None)

        ProcessUser.FindSelectedElements(clickpoints,pageNum,fileName)

        return jsonify({
            "status": 'OK',
            "message": 'Compared!',
        })

if __name__ == '__main__':
    app.run(debug='True', host='0.0.0.0', threaded=True)
    #socketio.run(app, debug='False', host='0.0.0.0')