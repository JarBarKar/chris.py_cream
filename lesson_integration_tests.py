from typing import ContextManager
import unittest
import flask_testing
import json
from app import app, db, Lesson


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app

    def setUp(self):
        self.s1 = Lesson(SID='G1', CID='IS111', LID='1')
        self.s2 = Lesson(SID='G1', CID='IS111', LID='2')
        self.s3 = Lesson(SID='G2', CID='IS111', LID='1')
        
        db.create_all()


    def tearDown(self):
        self.s1 = None
        self.s2 = None
        self.s3 = None
        db.session.remove()
        db.drop_all()



class TestDeleteLesson(TestApp):
    # Testing positive case where content name is updated
    def test_delete_lesson(self):
        # adding one lesson to database
        db.session.add(self.s1)
        db.session.commit()

        # setting lesson details
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'LID': self.s1.LID,
        }

        # calling delete function via flask route
        response = self.client.post("/delete_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": f"Lesson { self.s1.CID, self.s1.SID, self.s1.LID} has been deleted successfully from the database"    
        })

    def test_delete_missing_CID(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'LID': self.s1.LID,
        }

        # calling delete_lesson function via flask route
        response = self.client.post("/delete_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Lesson ['CID'] is not present, lesson is not successfully deleted"
        })

    def test_delete_lesson_not_in_database(self):
        # adding one lesson to database

        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'LID': self.s1.LID,
        }

        # calling delete_lesson function via flask route
        response = self.client.post("/delete_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Lesson {self.s1.CID, self.s1.SID, self.s1.LID} do not exist"
        })



# ### SECTION TEST CASES ###

if __name__ == '__main__':
    unittest.main()
