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
from schemas import UserSchema, ChangePasswordSchema
from models.user import UserModel, AdminUserModel
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
            abort(409, message="Email already exists, please login.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created."}, 201


# @blp.route("/admin-register")
# class AdminUserRegister(MethodView):
#     @blp.arguments(UserSchema)
#     def post(self, user_data):
#         if AdminUserModel.query.filter(
#             AdminUserModel.username == user_data["username"]
#         ).first():
#             abort(409, message="Email already exists, please login.")

#         admin_user = AdminUserModel(
#             username=user_data["username"],
#             password=pbkdf2_sha256.hash(user_data["password"]),
#         )
#         db.session.add(admin_user)
#         db.session.commit()

#         return {"message": "User created."}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(
        self, user_id
    ):  # wont be publicly available in the api, just for testing
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        regular_user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        admin_user = AdminUserModel.query.filter(
            AdminUserModel.username == user_data["username"]
        ).first()

        if admin_user:
            user = admin_user
        else:
            user = regular_user

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            if admin_user:
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "userType": "admin",
                }
            else:
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]  # or get_jwt().get("jti")

        token = TokenBlocklistModel(token=jti)
        db.session.add(token)
        db.session.commit()

        return {"message": "User logged out."}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/change-password")
class UserChangePassword(MethodView):
    @blp.arguments(ChangePasswordSchema)
    @jwt_required()
    def put(self, user_data):
        print("user_data", user_data)
        current_user_id = get_jwt_identity()
        regular_user = UserModel.query.get(current_user_id)
        admin_user = AdminUserModel.query.get(current_user_id)

        if admin_user:
            user = admin_user
        else:
            user = regular_user

        if not user and not admin_user:
            abort(404, message="User not found.")

        print(
            "verification",
            pbkdf2_sha256.verify(user_data["current_password"], user.password),
        )

        if pbkdf2_sha256.verify(user_data["current_password"], user.password):
            # Set the new password
            user.password = pbkdf2_sha256.hash(user_data["new_password"])

            # Commit changes to the database
            db.session.commit()

            # Return a success message
            return {"message": "Password changed successfully."}
        else:
            abort(401, message="Invalid current password.")
