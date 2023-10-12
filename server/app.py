#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Cakes, Bakeries, CakeBakery

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

#////////////////////////////////////////////////////////////////////////////////////////////////

@app.get('/bakeries')
def get_bakeries():
    bakeries = Bakeries.query.all()
    data = [b.to_dict()for b in bakeries]
    return make_response(jsonify(data),200)

@app.get('/bakeries/<int:id>')
def get_bakeries_id(id):
    bakeries = Bakeries.query.filter(Bakeries.id == id).first()
    if not bakeries:
        return make_response(jsonify({'error': 'Bakery not found'}),404)
    
    return make_response(jsonify(bakeries.to_dict()),200)

@app.delete('/bakeries/<int:id>')
def delete_bakeries_id(id):
    bakery = Bakeries.query.filter(Bakeries.id == id).first()
    if not bakery:
        return make_response(jsonify({'error': 'Bakery ID not found'}),)
    db.session.delete(bakery)
    db.session.commit()
    return make_response(jsonify({}), 200)

#////////////////////////////////////////////////////////////////////////////////////////////////

@app.get('/cakes')
def get_cakes():
    cakes = Cakes.query.all()
    data = [c.to_dict()for c in cakes]
    return make_response(jsonify(data),200)

@app.post('/cake_bakery')
def post_bakery():
    data = request.get_json()
    try:
        new_bakery = CakeBakery(
        price=data['price'],
        cake_id=['cake_id'],
        bakery_id=['bakery_id']
        )
    except Exception:
        return "error error error "

    db.session.add(new_bakery)
    db.session.commit()

    return make_response(jsonify(new_bakery.to_dict()),200)


#////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    app.run(port=5000, debug=True)