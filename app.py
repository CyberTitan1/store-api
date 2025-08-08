from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
import datetime
import os
from resources.user import refresh_bp, Register_User, revoked_tokens, User, logout_bp

base_app = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user.db")
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "eximius"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=45)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{base_app}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


jwt = JWTManager(app)
api = Api(app)


@app.before_request
def my_request():
    db.create_all()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in revoked_tokens


app.register_blueprint(refresh_bp)
app.register_blueprint(logout_bp)


api.add_resource(User, '/users/<int:user_id>', '/users')
api.add_resource(Register_User, '/register')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
