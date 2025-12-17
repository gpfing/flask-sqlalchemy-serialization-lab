from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', backref='reviews')
    item = db.relationship('Item', backref='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.rating}>'
    
class ReviewSchema(Schema):
    id = fields.Int()
    comment = fields.Str()
    customer_id = fields.Int()
    item_id = fields.Int()

    customer = fields.Nested('CustomerSchema', only=['id', 'name'])
    item = fields.Nested('ItemSchema', only=['id', 'name', 'price'])

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class CustomerSchema(Schema):
    id = fields.Int()
    name = fields.Str()

    reviews = fields.Nested('ReviewSchema', many=True, only=['id', 'comment', 'item'])

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class ItemSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Float()

    reviews = fields.Nested('ReviewSchema', many=True, only=['id', 'comment', 'customer'])