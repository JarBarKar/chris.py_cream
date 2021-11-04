from typing import ContextManager
import unittest
import flask_testing
import json
from app import app, db, Lesson
from datetime import datetime


#Group member in-charge: Kenneth
class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app

    def setUp(self):
        self.l1 = Lesson(LID='1', CID='IS111', SID='G1', start=datetime.fromisoformat("2021-04-01 09:15:00"))
        self.l2 = Lesson(LID='2', CID='IS111', SID='G1', start=datetime.fromisoformat("2021-04-08 09:15:00"))
        self.l3 = Lesson(LID='1', CID='IS212', SID='G4', start=datetime.fromisoformat("2021-04-01 09:15:00"))
        
        db.create_all()

    def tearDown(self):

        self.l1 = None
        self.l2 = None
        self.l3 = None
        db.session.remove()
        db.drop_all()

### LESSON TEST CASES ###
class TestViewLessons(TestApp):
    # Testing function when database has 1 lesson
    def test_view_all_lessons_0(self):
        # calling view_lessons function via flask route
        db.session.add(self.l1)
        db.session.commit()
        response = self.client.get("/view_lessons")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : 'All lessons are retrieved',
            'data' : [
                {"LID":"1",
                "CID":"IS111",
                "SID":"G1",
                "start":"Thu, 01 Apr 2021 09:15:00 GMT"}
            ]
        })
    
    # Testing function when database has 2 lesson
    def test_view_all_lessons_1(self):
        # calling view_lessons function via flask route
        db.session.add(self.l1)
        db.session.add(self.l2)
        db.session.commit()
        response = self.client.get("/view_lessons")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : 'All lessons are retrieved',
            'data' : [
                {
                "LID":"1",
                "CID":"IS111",
                "SID":"G1",
                "start":"Thu, 01 Apr 2021 09:15:00 GMT"
                },
                {
                "LID":"2",
                "CID":"IS111",
                "SID":"G1",
                "start":"Thu, 08 Apr 2021 09:15:00 GMT"
                }
            ]
        })
    
    # Testing function when there is no database
    def test_view_all_lessons_fail(self):
        # calling view_lessons function via flask route
        response = self.client.get("/view_lessons")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : 'There are no lesson retrieved'
        })

class TestQueryLessons(TestApp):
    # Testing function to query lesson by SID, CID
    def test_query_lessons_0(self):
        # calling query_lessons function via flask route
        db.session.add(self.l1)
        db.session.add(self.l2)
        db.session.commit()

        request_body = {
            "SID": self.l1.SID,
            "CID": self.l1.CID
        }

        response = self.client.post("/query_lessons",
                                    data=json.dumps(request_body),
                                    content_type='application/json')   
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': [
                {
                "LID":"1",
                "CID":"IS111",
                "SID":"G1",
                "start":"Thu, 01 Apr 2021 09:15:00 GMT"
                },
                {
                "LID":"2",
                "CID":"IS111",
                "SID":"G1",
                "start":"Thu, 08 Apr 2021 09:15:00 GMT"
                }
            ],
            'message' : 'Lessons have been query successfully from the database'
        })



    # Testing negative case where database is not initiated
    def test_query_lessons_database_not_in(self):
        request_body = {
            "SID": self.l1.SID,
            "CID": self.l1.CID,
            "start": datetime.isoformat(self.l1.start),
        }
        # calling query_lessons function via flask route
        response = self.client.post("/query_lessons",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)                     
        self.assertEqual(response.json, {
            "message" : "Lessons cannot be query"
        })
    

    # Testing negative case where SID is not provided in request body
    def test_query_lessons_missing_sid(self):
        request_body = {
            "CID": self.l1.CID,
            "start": datetime.isoformat(self.l1.start)
        }
        # calling query_lessons function via flask route
        response = self.client.post("/query_lessons",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)                     
        self.assertEqual(response.json, {
            "message" : "Lessons cannot be query"
        })
    
    # Testing negative case where CID is not provided in request body
    def test_query_lessons_missing_cid(self):
        request_body = {
            "SID": self.l1.SID,
            "start": datetime.isoformat(self.l1.start)
        }
        # calling query_lessons function via flask route
        response = self.client.post("/query_lessons",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)                     
        self.assertEqual(response.json, {
            "message" : "Lessons cannot be query"
        })
    
    # Testing negative case where start is not provided in request body
    def test_query_lessons_missing_start(self):
        request_body = {
            "SID": self.l1.SID,
            "CID": self.l1.CID,
        }
        # calling query_lessons function via flask route
        response = self.client.post("/query_lessons",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)                     
        self.assertEqual(response.json, {
            "message" : "Lessons cannot be query"
        })

    # Testing negative case where wrong SID is provided in request body
    def test_query_lessons_wrong_SID(self):
        request_body = {
            "SID": "USAIN BOLT",
            "CID": self.l1.CID,
            "start": datetime.isoformat(self.l1.start)
        }
        # calling query_lessons function via flask route
        response = self.client.post("/query_lessons",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)                     
        self.assertEqual(response.json, {
            "message" : "Lessons cannot be query"
        })

    # Testing negative case where wrong SID is provided in request body
    def test_query_lessons_wrong_CID(self):
        request_body = {
            "SID": self.l1.SID,
            "CID": "POKEMON",
            "start": datetime.isoformat(self.l1.start)
        }
        # calling query_lessons function via flask route
        response = self.client.post("/query_lessons",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)                     
        self.assertEqual(response.json, {
            "message" : "Lessons cannot be query"
        })

    # Testing negative case where wrong SID is provided in request body
    def test_query_lessons_wrong_start(self):
        request_body = {
            "SID": self.l1.SID,
            "CID": self.l1.CID,
            "start": "2021-04-09 09:15:00"
        }
        # calling query_lessons function via flask route
        response = self.client.post("/query_lessons",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)                     
        self.assertEqual(response.json, {
            "message" : "Lessons cannot be query"
        })

    # Testing negative case where no request body is provided in request body
    def test_query_lessons_no_request(self):
        request_body = {
        }
        # calling query_lesson function via flask route
        response = self.client.post("/query_lessons",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)                     
        self.assertEqual(response.json, {
            "message" : "Lessons cannot be query"
        })



class TestCreateCourse(TestApp):
    # Testing positive case where all details are present in request body
    def test_create_lesson_all_details_0(self):
        # setting course details
        request_body = {
            "LID": self.l1.LID,
            "SID": self.l1.SID,
            "CID": self.l1.CID,
            "start": datetime.isoformat(self.l1.start)
        }

        # calling create_lesson function via flask route
        response = self.client.post("/create_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message':'Lesson has been inserted successfully into the database',
            'data': {
                    "CID": "IS111",
                    "SID": "G1",
                    "LID": "1",
                    "start": "Thu, 01 Apr 2021 09:15:00 GMT"
                }
        })


    # Testing positive case where all details are present in request body
    def test_create_lesson_all_details_1(self):
        # setting course details
        request_body = {
            "LID": self.l3.LID,
            "SID": self.l3.SID,
            "CID": self.l3.CID,
            "start": datetime.isoformat(self.l1.start)
        }

        # calling create_lesson function via flask route
        response = self.client.post("/create_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message':'Lesson has been inserted successfully into the database',
            'data': {
                    "CID": "IS212",
                    "SID": "G4",
                    "LID": "1",
                    "start": "Thu, 01 Apr 2021 09:15:00 GMT"
                }
        })
    

    # Testing negative case where LID is missing in request body
    def test_create_lesson_missing_lid(self):
        # setting course details
        request_body = {
            "SID": self.l3.SID,
            "CID": self.l3.CID,
            "start": datetime.isoformat(self.l1.start)
        }

        # calling create_lesson function via flask route
        response = self.client.post("/create_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message':'LID is missing'
        })

    # Testing negative case where CID is missing in request body
    def test_create_lesson_missing_cid(self):
        # setting lesson details
        request_body = {
            "LID": self.l3.LID,
            "SID": self.l3.SID,
            "start": datetime.isoformat(self.l1.start)
        }

        # calling create_lesson function via flask route
        response = self.client.post("/create_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message':'CID is missing'
        })

    
    # Testing negative case where start is missing in request body
    def test_create_lesson_missing_start(self):
        # setting lesson details
        request_body = {
            "LID": self.l3.LID,
            "SID": self.l3.SID,
            "CID": self.l3.CID
        }

        # calling create_lesson function via flask route
        response = self.client.post("/create_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message':'start is missing'
        })

        # Testing negative case where start and CID is missing in request body
    def test_create_lesson_missing_start_CID(self):
        # setting lesson details
        request_body = {
            "LID": self.l3.LID,
            "SID": self.l3.SID,
        }

        # calling create_lesson function via flask route
        response = self.client.post("/create_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message':'CID,start is missing'
        })

    # Testing negative case where all request is missing in request body
    def test_create_lesson_all_missing(self):
        # setting lesson details
        request_body = {
        }

        # calling create_lesson function via flask route
        response = self.client.post("/create_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message':'LID,SID,CID,start is missing'
        })

    # Testing negative case where start format is wrong
    def test_create_lesson_start_wrong(self):
        # setting lesson details
        request_body = {
            "LID": 10,
            "SID": self.l3.SID,
            "CID": self.l3.CID,
            "start": "0001 00:00:00"
        }

        # calling create_lesson function via flask route
        response = self.client.post("/create_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message':'Lesson is not inserted successfully into the database'
        })
          


class TestDeleteLesson(TestApp):
    # Testing positive case where content name is updated
    def test_delete_lesson(self):
        # adding one lesson to database
        db.session.add(self.l1)
        db.session.commit()

        # setting lesson details
        request_body = {
            'SID': self.l1.SID,
            'CID': self.l1.CID,
            'LID': self.l1.LID,
            "start": datetime.isoformat(self.l1.start)
        }

        # calling delete function via flask route
        response = self.client.post("/delete_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": f"Lesson { self.l1.CID, self.l1.SID, self.l1.LID, datetime.isoformat(self.l1.start)} has been deleted successfully from the database"    
        })

    def test_delete_missing_CID(self):
        # adding one section to database
        db.session.add(self.l1)
        db.session.commit()

        # setting section details
        request_body = {
            'SID': self.l1.SID,
            'LID': self.l1.LID,
            "start": datetime.isoformat(self.l1.start)
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
            'SID': self.l1.SID,
            'CID': self.l1.CID,
            'LID': self.l1.LID,
            "start": datetime.isoformat(self.l1.start)
        }

        # calling delete_lesson function via flask route
        response = self.client.post("/delete_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Lesson {self.l1.CID, self.l1.SID, self.l1.LID, datetime.isoformat(self.l1.start)} do not exist"
        })


# ### LESSON TEST CASES ###



if __name__ == '__main__':
    #For jenkins
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    #For local tests
    # unittest.main()
