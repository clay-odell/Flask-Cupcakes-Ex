from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Connect to Database"""
    db.app = app
    db.init_app(app)
    
"""Models for Cupcake app."""

class Cupcake(db.Model):
    """Cupcake Model"""
    __tablename__ = 'cupcakes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default='https://tinyurl.com/demo-self')
    
    def cupcakes_to_dict(self):
        """Serialize a Cupcake SQLALCHEMY obj to dictionary"""
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }
    