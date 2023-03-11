from apiflask import Schema, fields as af_fields, PaginationSchema
from marshmallow import fields as mm_fields
from apiflask.validators import Range


class AuthOut(Schema):
    user_agent = af_fields.String()
    updated_at = mm_fields.DateTime()


class AuthLogsOut(Schema):
    items = af_fields.List(af_fields.Nested(AuthOut))
    pagination = af_fields.Nested(PaginationSchema)


class AuthLogsQuery(Schema):
    page = af_fields.Integer(load_default=1)
    per_page = af_fields.Integer(load_default=20, validate=Range(max=100))


class Token(Schema):
    message = af_fields.String()
    access_token = af_fields.String()
    refresh_token = af_fields.String()
