from flask import Flask, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01302@localhost/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():
    connect_db(app)
    db.create_all()
    
@app.route('/api/cupcakes')
def list_cupcakes():
    """GET Cupcake Data Return JSON {cupcakes:[{id, flavor, size, rating, image}, ...]}"""
    all_cupcakes = [cupcake.cupcakes_to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """GET Cupcake Data By ID Return JSON"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.cupcakes_to_dict())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create Cupcake POST route"""
    new_cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'], image=request.json['image'])
    db.session.add(new_cupcake)
    db.session.commit()
    resp_json = jsonify(cupcake=new_cupcake.cupcakes_to_dict())
    return (resp_json, 201)