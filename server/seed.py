from random import choice as rc
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from models import db, Bakeries

with app.app_context():
    b1 = Bakeries(name="test", address="test")
    db.session.add(b1)
    db.session.commit()