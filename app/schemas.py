from marshmallow import Schema, fields, validate, validates, ValidationError

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=4, max=20))
    email = fields.Email(required=True)
    image_file = fields.Str(dump_only=True)
    # Load_only=True means it is only parsed during deserialization (input) and not returned in output
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8, max=19))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=100))
    date_posted = fields.DateTime(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=50))
    user_id = fields.Int(dump_only=True)
