from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import func
from marshmallow import fields
from marshmallow import Schema
from marshmallow import post_load

from .base import Base


class Discount(Base):
    __tablename__ = 'discounts'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    percent = Column(Integer, nullable=False)
    created_date = Column(DateTime, nullable=False, server_default=func.now())
    expiration_date = Column(DateTime, nullable=False)


class DiscountSchema(Schema):

    model_class = Discount

    id = fields.Integer()
    product_id = fields.Integer(data_key='productID')
    percent = fields.Integer()
    created_date = fields.DateTime(data_key='createdDate')
    expiration_date = fields.DateTime(data_key='expirationDate')

    @post_load
    def make_address(self, data, **kwargs):
        return Discount(**data)
