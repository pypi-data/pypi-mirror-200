from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from marshmallow import fields
from marshmallow import Schema
from marshmallow import post_load
from .image import ImageSchema

from .base import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    category_id = Column(ForeignKey('categories.id'), nullable=False)
    name = Column(String(50), nullable=False)
    number = Column(String(25), nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    image = relationship('Image', foreign_keys='Image.product_id')


class ProductSchema(Schema):

    model_class = Product

    id = fields.Integer()
    category_id = fields.Integer(data_key='categoryID')
    name = fields.String()
    number = fields.String()
    price = fields.Integer()
    quantity = fields.Integer()
    description = fields.String()

    image = fields.Nested(ImageSchema)

    @post_load
    def make_address(self, data, **kwargs):
        return Product(**data)
