from marshmallow import Schema, RAISE, fields


class BaseSchema(Schema):

    class Meta:
        unknown = RAISE


class ImageQuery(BaseSchema):
    zoom = fields.Float(required=True)
    top = fields.Integer(required=True)
    left = fields.Integer(required=True)
    right = fields.Integer(required=True)
    bottom = fields.Integer(required=True)
