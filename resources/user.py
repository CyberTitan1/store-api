from models.user import User
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from flask import Blueprint, jsonify


refresh_bp = Blueprint("refresh_blueprint", __name__, url_prefix="/refresh")
logout_bp = Blueprint("logout_blueprint", __name__, url_prefix="/logout")

Users = User()
revoked_tokens = set()

parser = reqparse.RequestParser()
parser.add_argument(
    "username",
    type=str,
    required=True,
    help="Please input a valid username!"
)
parser.add_argument(
    "password",
    type=str,
    required = True,
    help="Please input a valid password!"
)


class Register_User(Resource):

    def post(self):
        try:
            data = parser.parse_args()
            user, result = Users.create_user(data["username"], data["password"])
            if user is True:
                return {
                    "msg": "User registered successfully!",
                    "id": result.id,
                    "username": result.name,
                    "password": result.password,
                }, 201     
            else:
                return {
                    "msg":"An internal error occurred!"
                }, 500
        except Exception as e:
            return{
                "msg":f"Invalid request! {e}",
            }, 400


class User(Resource):

    @jwt_required()
    def get(self, user_id):

        try:
            verify_user_id = get_jwt_identity()
            if int(verify_user_id) == user_id:
                pass
            else:
                return {
                    "msg":"Invalid user!"
                }, 401
            user, result = Users.get_user_by_id(user_id)
            if user is True:
                return {
                    "id": result.id,
                    "username": result.name,
                    "password": result.password,
                }, 200
            elif user is None:
                return {
                    "msg":"User not found!"
                }, 404
            elif user is False:
                return {
                    "msg":"An internal error occurred!"
                }, 500
        except Exception as e:
            return{
                "msg":"Invalid request!"
            }, 400

    def post(self):

        try:
            data = parser.parse_args()
            user, result = Users.verify_user_details(data["username"], data["password"])
            if user is True:
                access_token = create_access_token(identity=str(result.id))
                refresh_token = create_refresh_token(identity=str(result.id))
                return {
                    "msg": f"Logged in as {result.name}",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200
            elif user is None:
                return {
                    "msg":"User not found!"
                }, 404
            elif user is False:
                return {
                    "msg":"An internal error occurred!"
                }, 500
        except Exception as e:
            return{
                "msg":"Invalid request!",
            }, 400

    @jwt_required()
    def put(self, user_id):

        try:
            data = parser.parse_args()
            verify_user_id = get_jwt_identity()
            if int(verify_user_id) == user_id:
                pass
            else:
                return {
                    "msg":"Invalid user!"
                }, 401
            user = Users.update_user(user_id, data["username"], data["password"])
            if user is True:
                return {
                    "msg":"Updated successfully!",
                }, 200
            elif user is None:
                return{
                    "msg":"User not found!",
                }, 404
            elif user is False:
                return {
                    "msg":"An internal error occurred!"
                }, 500
        except Exception as e:
            return {
                "msg":"Invalid request!"
            }, 400





    @jwt_required()
    def delete(self, user_id):  

        try:
            verify_user_id = get_jwt_identity()
            if int(verify_user_id) == user_id:
                pass
            else:
                return {
                    "msg":"Invalid user!"
                }, 401
            user = Users.delete_user(user_id)
            if user is True:
                return {
                    "msg":"Deleted successfully!"
                }, 200
            elif user is None:
                return {
                    "msg":"User not found!"
                }, 404
            elif user is False:
                return {
                    "msg":"An internal error occurred!"
                }, 500
        except Exception as e:
            return {
                "msg":"Invalid request!"
            }, 400


@refresh_bp.route('/', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({"access_token":new_access_token}), 200


@logout_bp.route("/", methods=['POST'])
@jwt_required(verify_type=False)
def logout():
    jwt_data = get_jwt()
    jti = jwt_data["jti"]
    revoked_tokens.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200