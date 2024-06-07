from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01302@localhost/cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
with app.test_request_context():
    db.drop_all()
    db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}
CUPCAKE_DATA_3 = {
    'flavor': 'TestFlavor3',
    'size': 'TestSize3',
    'rating': 6.5,
    'image': 'http://test.com/cupcake3.jpg'
}

class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""
        with app.test_request_context():
            self.client = app.test_client()
            Cupcake.query.delete()

            cupcake = Cupcake(**CUPCAKE_DATA)
            db.session.add(cupcake)
            db.session.commit()
            self.cupcake = cupcake
            self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.test_request_context():
            db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)
            
    def test_update_cupcake(self):
        with app.test_client() as client:
            update_data = {
                "flavor": "UpdatedFlavor",
                "size": "UpdatedSize",
                "rating": 6.5,
                "image": "http://test.com/updated_cupcake.jpg"
                
            }
            resp = client.patch(f"/api/cupcakes/{self.cupcake_id}", json=update_data)
            
            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "UpdatedFlavor",
                    "size": "UpdatedSize",
                    "rating": 6.5,
                    "image": "http://test.com/updated_cupcake.jpg"
                }
            })
            cupcake = Cupcake.query.get(self.cupcake_id)
            self.assertEqual(cupcake.flavor, "UpdatedFlavor")
            self.assertEqual(cupcake.size, "UpdatedSize")
            self.assertEqual(cupcake.rating, 6.5)
            self.assertEqual(cupcake.image, "http://test.com/updated_cupcake.jpg")
            
    def test_delete_cupcake(self):
        with app.test_client() as client:
            resp = client.delete(f'/api/cupcakes/{self.cupcake_id}')
            self.assertEqual(resp.status_code, 200)
            
            data = resp.json
            self.assertEqual(data, {"message": "DELETED"})
            cupcake = Cupcake.query.get(self.cupcake_id)
            self.assertIsNone(cupcake)
            
            
