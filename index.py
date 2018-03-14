# Copyright 2017 Jacques Berger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import render_template
from flask_cors import CORS, cross_origin
from flask import g
from flask import request
from flask import redirect
from flask import session
from flask import Response
from flask import jsonify
from flask import make_response
from flask import abort
from backend.database import Database
import hashlib
import uuid
import json
from functools import wraps

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def start_page():
    username = None
    if "id" in session:
        username = get_db().get_session(session["id"])
    return True


@app.route('/confirmation')
def confirmation_page():
    return True


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        pass
    else:
        username = request.json["username"]
        password = request.json["password"]
        email = request.json["email"]
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        gender = request.json['gender']
        phone = request.json['phone']
        # Vérifier que les champs ne sont pas vides
        # if username == "" or password == "" or email == "":
        #     return True

        # TODO Faire la validation du formulaire
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
        db = get_db()
        db.create_user(username, 'New', salt, hashed_password, first_name, last_name, gender, phone, email)

        return make_response(jsonify({'success': 'ok'}), 200)


@app.route('/login', methods=["POST"])
def log_user():
    username = request.json["username"]
    password = request.json["password"]
    # Vérifier que les champs ne sont pas vides
    if username == "" or password == "":
        return False

    user = get_db().get_user_login_info(username)
    if user is None:
        abort(404)

    salt = user[0]
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    if hashed_password == user[1]:
        # Accès autorisé
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, username)
        session["id"] = id_session
        return make_response(jsonify({'user': username}), 200)
    else:
        return make_response(jsonify({'ok': 'false'}), 401)


@app.route('/<query>', methods=["POST", "GET"])
@cross_origin()
def process_query(query):
    if query == 'trending':
        trending = get_db().get_trending()
        data={
            'results':trending
        }
        response = jsonify(data)
        response.status_code = 200
        return response
    elif query == 'most_watched':
        most_watched = get_db().get_most_watched()
        data={
            'results':most_watched
        }
        response = jsonify(data)
        response.status_code = 200
        return response
    else:
        query = json.loads(query)
        print(query)
        query_result = get_db().get_query(query)
        data={
            'results':query_result
        }
        response = jsonify(data)
        response.status_code = 200
        return response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# @app.route('/trending', methods=["POST"])
# def trending():
#     trending = get_db().get_trending()
#     response = jsonify(trending)
#     return response
#
#
# @app.route('/most_watched', methods=["POST"])
# def most_watched():
#     most_watched = get_db().get_most_watched()
#     response = jsonify(most_watched)
#     return response


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)
    return decorated


@app.route('/logout')
@authentication_required
def logout():
    if "id" in session:
        id_session = session["id"]
        session.pop('id', None)
        get_db().delete_session(id_session)
    return redirect("/")


def is_authenticated(session):
    return "id" in session


def send_unauthorized():
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


app.secret_key = "(*&*&322387he738220)(*(*22347657"


if __name__ == '__main__':
    app.run()