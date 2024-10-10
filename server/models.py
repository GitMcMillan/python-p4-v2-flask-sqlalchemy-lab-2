from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    #relationship w/Review
    reviews = db.relationship('Review', back_populates='customer')

    # Update Customer to add an association proxy named items to get a list of items through the customer's reviews relationship.
    
    items = association_proxy('reviews', 'item')

    #Customer should exclude reviews.customer
    serialize_rules = ('-reviews.customer',)

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    #relationship w/Review
    reviews = db.relationship('Review', back_populates='item')

    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
    
#add a new model class named Review that inherits from db.Model. Add the following attributes to the Review model:
class Review(db.Model, SerializerMixin):
    # a string named __tablename__ assigned to the value 'reviews'.
    __tablename__ = "reviews"
    # a column named id to store an integer that is the primary key.
    id = db.Column(db.Integer, primary_key=True)
    # a column named comment to store a string.
    comment = db.Column(db.String)
    # a column named customer_id that is a foreign key to the 'customers' table.
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    # a column named item_id that is a foreign key to the 'items' table.
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    # a relationship named customer that establishes a relationship with the Customer model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Customer.
    customer = db.relationship('Customer', back_populates="reviews")
    # a relationship named item that establishes a relationship with the Item model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Item.
    item = db.relationship('Item', back_populates="reviews")

    serialize_rules = ('-customer.reviews', '-item.reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'










