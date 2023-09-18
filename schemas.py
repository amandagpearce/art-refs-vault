from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(
        required=True, load_only=True
    )  # load_only=True ensures the pw will never be returned to the client


class TokenBlocklist(Schema):
    token = fields.Str(required=True, load_only=True)
