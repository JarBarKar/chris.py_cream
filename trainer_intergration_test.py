import unittest
import flask_testing
import json
from app import app, db, Trainer

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app

    def setUp(self):
        self.t1 = Trainer(TID=1, name='Chris', password = '123', phone = 123, email = 'chris@abc.com', address = 'SMU')
        self.t2 = Trainer(TID=2, name='Tom', password = '456', phone = 456, email = 'tom@abc.com', address = 'NTU')
        self.t3 = Trainer(TID=3, name='Jerry', password = '789', phone = 789, email = 'jerry@abc.com', address = 'NUS')
        db.create_all()


    def tearDown(self):
        self.t1 = None
        self.t2 = None
        self.t3 = None
        db.session.remove()
        db.drop_all()

class TestViewTrainers(TestApp):
    # Testing function when database has no courses
    def test_view_trainers_database_empty(self):
        # calling view_courses function via flask route
        response = self.client.get("/view_trainers")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : 'There are no trainer retrieved'
        })


    # Testing function when database has 1 course
    def test_view_all_trainers(self):
        # adding two courses to database
        db.session.add(self.t1)
        db.session.add(self.t2)
        db.session.add(self.t3)
        db.session.commit()
        
        # calling view_courses function via flask route
        response = self.client.get("/view_trainers")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : 'All trainers are retrieved',
            'data' :[
                {'TID': 1, 'address': 'SMU', 'email': 'chris@abc.com', 'name': 'Chris', 'password': '123', 'phone': 123}, 
                {'TID': 2, 'address': 'NTU', 'email': 'tom@abc.com', 'name': 'Tom', 'password': '456', 'phone': 456}, 
                {'TID': 3, 'address': 'NUS', 'email': 'jerry@abc.com', 'name': 'Jerry', 'password': '789', 'phone': 789}
            ]
            
            })

if __name__ == '__main__':
    # #For jenkins
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    #For local tests
    # unittest.main()