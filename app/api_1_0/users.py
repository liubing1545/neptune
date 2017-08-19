from flask import jsonify, request, abort, url_for, g
from flask_httpauth import HTTPBasicAuth
from . import api
from .errors import unauthorized, forbidden
from .. import db
from ..models import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(user_email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@api.before_request
@auth.login_required
def before_request():
    pass


# @api.route('/users', methods=['POST'])
# def new_user():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     if username is None or password is None:
#         abort(400)    # missing arguments
#     if User.query.filter_by(username=username).first() is not None:
#         abort(400)    # existing user
#     user = User(username=username)
#     user.hash_password(password)
#     db.session.add(user)
#     db.session.commit()
#     return (jsonify({'username': user.username}), 201,
#             {'Location': url_for('get_user', id=user.id, _external=True)})


# @api.route('/users/<int:id>')
# def get_user(id):
#     user = User.query.get(id)
#     if not user:
#         abort(400)
#     return jsonify({'username': user.username})


@api.route('/token')
def get_auth_token():
    token = g.current_user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@api.route('/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'hello, %s!' % g.current_user.user_name})