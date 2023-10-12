from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

#///////////////////////////////////////////////////////////////////////////////////

class Cakes(db.Model, SerializerMixin):
    __tablename__ = 'cakes_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    cake_bakery = db.relationship("CakeBakery", backref="cakes")

#///////////////////////////////////////////////////////////////////////////////////

class Bakeries(db.Model, SerializerMixin):
    __tablename__ = 'bakeries_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    cake_bakery = db.relationship("CakeBakery", backref="bakeries")

#///////////////////////////////////////////////////////////////////////////////////

class CakeBakery(db.Model, SerializerMixin):
    __tablename__ = 'cake_bakeries_table'

    id = db.Column(db.Integer, primary_key=True)
    cake_id = db.Column(db.Integer, db.ForeignKey("cakes_table.id"),nullable=False)
    bakery_id = db.Column(db.Integer, db.ForeignKey("bakeries_table.id"),nullable=False)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    serialize_rules=('-bakeries','-cakes')

    @validates('price')
    def validate_price(self, key, price):
        if 0 < price < 1000:
            return price
        else:
            raise ValueError("Price is not acceptable")



    