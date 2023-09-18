from flask_smorest import abort, Blueprint
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
    create_refresh_token,
    get_jwt_identity,
)

from db import db
from schemas import UserSchema
from models.user import UserModel
from models.token_blocklist import TokenBlocklistModel

blp = Blueprint(
    "Users",
    "users",
    description="Login, Registration and Authentication operations",
)


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first():
            abort(409, message="Esse username já existe.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "Usuario criado com sucesso"}, 201


