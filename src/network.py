import ProcessUser
import ConceptMapGenerator
import base64
#!/usr/bin/env python3
import os
os.environ["FLASK_ENV"]="development"

def start(links):

    import sys
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

            print(pageNum,file=sys.stderr)

            print(ProcessUser.GetDict(), file=sys.stderr)


            return jsonify({
                "status": 'OK',
                "message": 'Compared!',
            })
            
    @app.route('/generate', methods=['POST'])

    def detectGenerateConceptMapButtonPress():
        if request.method == 'POST':
            lst = ConceptMapGenerator.GenerateMap(ProcessUser.GetDict())
            print("THE BUTTON WAS HIT", file=sys.stderr)
            dct = {}
            for tup in lst:
                dct[tup[0]] = tup[1]
            return jsonify({
                    "dictionary": dct
                })

    @app.route('/requestslides', methods=['POST'])
    
    def detectrequest():
        if request.method == 'POST':
            if request.json.get('request') == True:
                return jsonify({"jpeglinks" : links})


<<<<<<< HEAD
from flask import Flask, session, request, render_template, jsonify, redirect, url_for
from flask_restful import Api, Resource, reqparse
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import eventlet
from pymongo import MongoClient
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
import bcrypt
import requests
import base64
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

@app.route('/requestslides', methods=['POST'])
def detectrequest():
    if request.method == 'POST':
        if request.json.get('request') == True:
            images = []
            for filename in os.listdir("./ImageTest"):
                with open("./ImageTest/" + filename, "rb") as image_file:
                images.append(base64.b64encode(image_file.read()))
            return jsonify({
                "jpgs": images
            })
        

if __name__ == '__main__':
    app.run(debug='True', host='0.0.0.0', threaded=True)
    #socketio.run(app, debug='False', host='0.0.0.0')
=======
    if __name__ == 'network':
        app.run(debug='True', host='0.0.0.0')
#start()
>>>>>>> 03ff1e70257977361417af337a82c02d44bb9965
