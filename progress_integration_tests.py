import unittest
import flask_testing
import json
from app import Content, app, db, Progress
from datetime import datetime


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app


    def setUp(self):
        self.p1 = Progress(EID=1, SID="G1", CID="IS111", start=datetime.fromisoformat("2021-04-01 09:15:00"),latest_lesson_reached="3",recent_content_name="Lesson 2 slides",viewed_contents="Lesson 2 slides")
        self.p2 = Progress(EID=1, SID="G2", CID="IS112", start=datetime.fromisoformat("2021-05-01 09:15:00"),latest_lesson_reached="1",recent_content_name="Lesson 1 how get free money",viewed_contents="Lesson 1 How get free money', 'Lesson 1 How to train dragons|Lesson 1 How get free money")
        self.p3 = Progress(EID=1, SID="G1", CID="IS111", start="2021-04-01 09:15:00",latest_lesson_reached="2",recent_content_name="Lesson 2 slides",viewed_contents="Lesson 2 slides")
        self.p4 = Progress(EID=1, SID="G2", CID="IS112", start="2021-05-01 09:15:00",latest_lesson_reached="1",recent_content_name="Lesson 1 how get free money",viewed_contents="Lesson 1 How to train dragons|Lesson 1 How get free money")
        self.c1 = Content(LID='1', SID='G1', CID='IS111',start='2021-04-01 09:15:00', content_type='pdf', content_name='Lesson 1 slides', link='abd.com/shared/fuie894')
        self.c2 = Content(LID='1', SID='G1', CID='IS111',start='2021-04-01 09:15:00', content_type='pdf', content_name='Lesson 1 slides part 2', link='abd.com/shared/fuie894')
        db.create_all()

    def tearDown(self):
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        self.c1 = None
        self.c2 = None

        db.session.remove()
        db.drop_all()


class TestUpdateProgress(TestApp):
    # Testing positive case where lesson is updated
    def test_update_progress_0(self):
        # adding two progress to database
        db.session.add(self.p1)
        db.session.add(self.p2)
        db.session.commit()

        # setting progress details
        request_body = {
            "EID": self.p1.EID,
            "SID": self.p1.SID,
            "CID": self.p1.CID,
            'start': datetime.isoformat(self.p1.start)
        }

        new_lesson = str(int(self.p1.latest_lesson_reached)+1)

        # calling unlock_next_lesson function via flask route
        response = self.client.post("/unlock_next_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {
                'SID': 'G1',
                'CID': 'IS111',
                'EID' : 1,
                'latest_lesson_reached': '4',
                'start': '2021-04-01 09:15:00',
                'viewed_contents': '',
                'recent_content_name': 'Lesson 2 slides'
            },
            'message': f"Latest lesson reached updated to lesson {new_lesson}"    
        })

   

    # Testing negative case where SID is not in database
    def test_update_section_EID_not_in_request(self):
        # adding two progress to database
        db.session.add(self.p1)
        db.session.add(self.p2)
        db.session.commit()

        # setting section details
        request_body = {
            "SID": self.p1.SID,
            "CID": self.p1.CID,
            'start': datetime.isoformat(self.p1.start)
        }

        # calling unlock_next_lesson function via flask route
        response = self.client.post("/unlock_next_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "EID is missing"
        })

    # Testing negative case where CID is not in database
    def test_update_section_CID_not_in_request(self):
        # adding two progress to database
        db.session.add(self.p1)
        db.session.add(self.p2)
        db.session.commit()

        # setting section details
        request_body = {
            "EID": self.p1.EID,
            "SID": self.p1.SID,
            'start': datetime.isoformat(self.p1.start)
        }

        # calling unlock_next_lesson function via flask route
        response = self.client.post("/unlock_next_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "CID is missing"
        })

    # Testing negative case where SID is not in database
    def test_update_section_start_not_in_request(self):
        # adding two progress to database
        db.session.add(self.p1)
        db.session.add(self.p2)
        db.session.commit()

        # setting section details
        request_body = {
            "EID": self.p1.EID, 
            "SID": self.p1.SID,
            "CID": self.p1.CID
        }

        # calling unlock_next_lesson function via flask route
        response = self.client.post("/unlock_next_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "start is missing"
        })

    # Testing negative case where database is empty
    def test_update_section_no_database(self):
        # setting section details
        request_body = {
            "EID": self.p1.EID,
            "SID": self.p1.SID,
            "CID": self.p1.CID,
            'start': datetime.isoformat(self.p1.start)
        }

        # calling unlock_next_lesson function via flask route
        response = self.client.post("/unlock_next_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "No lesson found"
        })

    # Testing negative case where no query return
    def test_update_section_no_query_return(self):
        # setting section details
        request_body = {
            "EID": self.p1.EID,
            "SID": self.p1.SID,
            "CID": "abcdefedede",
            'start': datetime.isoformat(self.p1.start)
        }

        # calling unlock_next_lesson function via flask route
        response = self.client.post("/unlock_next_lesson",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "No lesson found"
        })


class TestViewLessonContentStatus(TestApp):
    # Testing positive case where lesson queried is latest question
    def test_view_lesson_content_status_latest_lesson(self):
        t1 = self.p4.start
        # adding two progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        self.p4.start = datetime.fromisoformat(self.p4.start)
        db.session.add(self.p4)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p4.EID,
            "SID": self.p4.SID,
            "CID": self.p4.CID,
            "start": t1,
            "LID" : "1"
        }

        # calling view_lesson_content_status function via flask route
        response = self.client.post("/view_lesson_content_status",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': ['Lesson 1 How to train dragons', 'Lesson 1 How get free money'],
            'message': f"Progress record with EID: {self.p4.EID}, SID: {self.p4.SID}, CID: {self.p4.CID}, start: {self.p4.start} has been retrieved successfully"    
        })
    

    # Testing negative case where eid missing
    def test_view_lesson_content_status_latest_lesson_missing_eid(self):
        t1 = self.p4.start
        # adding two progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        self.p4.start = datetime.fromisoformat(self.p4.start)
        db.session.add(self.p4)
        db.session.commit()

        # setting query details
        request_body = {
            "SID": self.p4.SID,
            "CID": self.p4.CID,
            "start": t1,
            "LID" : "1"
        }

        # calling view_lesson_content_status function via flask route
        response = self.client.post("/view_lesson_content_status",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"EID is missing from request body, view lesson content status failed"    
        })
    

    # Testing negative case where sid missing
    def test_view_lesson_content_status_latest_lesson_missing_sid(self):
        t1 = self.p4.start
        # adding two progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        self.p4.start = datetime.fromisoformat(self.p4.start)
        db.session.add(self.p4)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p4.EID,
            "CID": self.p4.CID,
            "start": t1,
            "LID" : "1"
        }

        # calling view_lesson_content_status function via flask route
        response = self.client.post("/view_lesson_content_status",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"SID is missing from request body, view lesson content status failed"    
        })
    

    # Testing negative case where cid missing
    def test_view_lesson_content_status_latest_lesson_missing_cid(self):
        t1 = self.p4.start
        # adding two progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        self.p4.start = datetime.fromisoformat(self.p4.start)
        db.session.add(self.p4)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p4.EID,
            "SID": self.p4.SID,
            "start": t1,
            "LID" : "1"
        }

        # calling view_lesson_content_status function via flask route
        response = self.client.post("/view_lesson_content_status",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"CID is missing from request body, view lesson content status failed"    
        })
    

    # Testing negative case where start missing
    def test_view_lesson_content_status_latest_lesson_missing_start(self):
        t1 = self.p4.start
        # adding two progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        self.p4.start = datetime.fromisoformat(self.p4.start)
        db.session.add(self.p4)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p4.EID,
            "SID": self.p4.SID,
            "CID": self.p4.CID,
            "LID" : "1"
        }

        # calling view_lesson_content_status function via flask route
        response = self.client.post("/view_lesson_content_status",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"start is missing from request body, view lesson content status failed"    
        })
    

    # Testing negative case where LID missing
    def test_view_lesson_content_status_latest_lesson_missing_lid(self):
        t1 = self.p4.start
        # adding two progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        self.p4.start = datetime.fromisoformat(self.p4.start)
        db.session.add(self.p4)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p4.EID,
            "SID": self.p4.SID,
            "CID": self.p4.CID,
            "start" : t1
        }

        # calling view_lesson_content_status function via flask route
        response = self.client.post("/view_lesson_content_status",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"LID is missing from request body, view lesson content status failed"    
        })
    

    # Testing positive case where lesson queried is not latest question
    def test_view_lesson_content_status_not_latest_lesson(self):
        t1 = self.p3.start
        # adding two progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        self.p4.start = datetime.fromisoformat(self.p4.start)
        db.session.add(self.p4)
        # adding two content to database
        self.c1.start = datetime.fromisoformat(self.c1.start)
        db.session.add(self.c1)
        self.c2.start = datetime.fromisoformat(self.c2.start)
        db.session.add(self.c2)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p3.EID,
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "start": t1,
            "LID" : "1"
        }

        # calling view_lesson_content_status function via flask route
        response = self.client.post("/view_lesson_content_status",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': ['Lesson 1 slides', 'Lesson 1 slides part 2'],
            'message': f"Progress record with EID: {self.p3.EID}, SID: {self.p3.SID}, CID: {self.p3.CID}, start: {self.p3.start} has been retrieved successfully"    
        })
    

    # Testing positive case where lesson queried is not latest question
    def test_view_lesson_content_status_not_in_database(self):
        t1 = self.p3.start
        # adding two progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        self.p4.start = datetime.fromisoformat(self.p4.start)
        db.session.add(self.p4)
        # adding two content to database
        self.c1.start = datetime.fromisoformat(self.c1.start)
        db.session.add(self.c1)
        self.c2.start = datetime.fromisoformat(self.c2.start)
        db.session.add(self.c2)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": 4,
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "start": t1,
            "LID" : "1"
        }

        # calling view_lesson_content_status function via flask route
        response = self.client.post("/view_lesson_content_status",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"Progress record with EID: 4, SID: {self.p3.SID}, CID: {self.p3.CID}, start: {t1} does not exist in the database"    
        })

class TestViewLatestContentAccessed(TestApp):
    # Testing positive case where all details are given
    def test_view_latest_content_accessed_all_details(self):
        t1 = self.p3.start
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p3.EID,
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "start": t1,
            "content_name" : self.c1.content_name
        }

        # calling view_latest_content_accessed function via flask route
        response = self.client.post("/view_latest_content_accessed",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'EID': self.p3.EID,
                'SID': self.p3.SID,
                'CID': self.p3.CID,
                'start': t1,
                'latest_lesson_reached': self.p3.latest_lesson_reached,
                'recent_content_name': self.c1.content_name,
                'viewed_contents': self.p3.viewed_contents
            },
            'message': f"Progress record with EID: {self.p3.EID}, SID: {self.p3.SID}, CID: {self.p3.CID}, start: {t1} has been updated successfully"    
        })
    

    # Testing negative case where EID missing
    def test_view_latest_content_accessed_missing_eid(self):
        t1 = self.p3.start
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "start": t1,
            "content_name" : self.c1.content_name
        }

        # calling view_latest_content_accessed function via flask route
        response = self.client.post("/view_latest_content_accessed",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"EID is missing from request body, view latest content accessed failed"    
        })
    

    # Testing negative case where SID missing
    def test_view_latest_content_accessed_missing_sid(self):
        t1 = self.p3.start
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p3.EID,
            "CID": self.p3.CID,
            "start": t1,
            "content_name" : self.c1.content_name
        }

        # calling view_latest_content_accessed function via flask route
        response = self.client.post("/view_latest_content_accessed",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"SID is missing from request body, view latest content accessed failed"    
        })
    

    # Testing negative case where CID missing
    def test_view_latest_content_accessed_missing_cid(self):
        t1 = self.p3.start
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p3.EID,
            "SID": self.p3.SID,
            "start": t1,
            "content_name" : self.c1.content_name
        }

        # calling view_latest_content_accessed function via flask route
        response = self.client.post("/view_latest_content_accessed",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"CID is missing from request body, view latest content accessed failed"    
        })
    

    # Testing negative case where start missing
    def test_view_latest_content_accessed_missing_start(self):
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p3.EID,
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "content_name" : self.c1.content_name
        }

        # calling view_latest_content_accessed function via flask route
        response = self.client.post("/view_latest_content_accessed",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"start is missing from request body, view latest content accessed failed"    
        })
    

    # Testing negative case where content name missing
    def test_view_latest_content_accessed_missing_content_name(self):
        t1 = self.p3.start
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p3.EID,
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "start": t1
        }

        # calling view_latest_content_accessed function via flask route
        response = self.client.post("/view_latest_content_accessed",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"content_name is missing from request body, view latest content accessed failed"    
        })


    # Testing negative case where record not in database
    def test_view_latest_content_accessed_not_in_database(self):
        t1 = self.p3.start
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": 2,
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "start": t1,
            "content_name" : self.c1.content_name
        }

        # calling view_latest_content_accessed function via flask route
        response = self.client.post("/view_latest_content_accessed",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"Progress record with EID: 2, SID: {self.p3.SID}, CID: {self.p3.CID}, start: {self.p3.start} does not exist in the database"    
        })


class TestUpdateViewedContents(TestApp):
    # Testing positive case where all details are given, example 1
    def test_update_viewed_contents_latest_lesson_new_content(self):
        t1 = self.p3.start
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p3.EID,
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "start": t1,
            "content_name" : "How are you",
            "LID" : "2"
        }

        # calling update_viewed_contents function via flask route
        response = self.client.post("/update_viewed_contents",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'EID': self.p3.EID,
                'SID': self.p3.SID,
                'CID': self.p3.CID,
                'start': t1,
                'latest_lesson_reached': self.p3.latest_lesson_reached,
                'recent_content_name': self.p3.recent_content_name,
                'viewed_contents':  "Lesson 2 slides|How are you"
            },
            'message': f"Progress record with EID: {self.p3.EID}, SID: {self.p3.SID}, CID: {self.p3.CID}, start: {self.p3.start} has been updated successfully"    
        })
    
    # Testing positive case where all details are given, example 2
    def test_update_viewed_contents_latest_lesson_new_content_2(self):
        t1 = self.p4.start
        # adding one progress to database
        self.p4.start = datetime.fromisoformat(self.p4.start)
        db.session.add(self.p4)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p4.EID,
            "SID": self.p4.SID,
            "CID": self.p4.CID,
            "start": t1,
            "content_name" : "Try This",
            "LID" : "1"
        }

        # calling update_viewed_contents function via flask route
        response = self.client.post("/update_viewed_contents",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'EID': self.p4.EID,
                'SID': self.p4.SID,
                'CID': self.p4.CID,
                'start': t1,
                'latest_lesson_reached': self.p4.latest_lesson_reached,
                'recent_content_name': self.p4.recent_content_name,
                'viewed_contents':  "Lesson 1 How to train dragons|Lesson 1 How get free money|Try This"
            },
            'message': f"Progress record with EID: {self.p4.EID}, SID: {self.p4.SID}, CID: {self.p4.CID}, start: {self.p4.start} has been updated successfully"    
        })


    # Testing negative case where lesson is not latest lesson
    def test_update_viewed_contents_not_latest_lesson(self):
        t1 = self.p3.start
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p3.EID,
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "start": t1,
            "content_name" : "How are you",
            "LID" : "1"
        }

        # calling update_viewed_contents function via flask route
        response = self.client.post("/update_viewed_contents",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"LID 1 is not the latest lesson, no update is needed."    
        })
    

    # Testing negative case where EID missing
    def test_update_viewed_contents_missing_eid(self):
        t1 = self.p3.start
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "start": t1,
            "content_name" : "How are you",
            "LID" : "1"
        }

        # calling update_viewed_contents function via flask route
        response = self.client.post("/update_viewed_contents",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"EID is missing from request body, update viewed contents failed"    
        })
    

    # Testing negative case where content_name missing
    def test_update_viewed_contents_missing_content_name(self):
        t1 = self.p3.start
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": self.p3.EID,
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "start": t1,
            "LID" : "1"
        }

        # calling update_viewed_contents function via flask route
        response = self.client.post("/update_viewed_contents",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"content_name is missing from request body, update viewed contents failed"    
        })


    # Testing negative case where record not in database
    def test_update_viewed_contents_not_in_database(self):
        t1 = self.p3.start
        # adding one progress to database
        self.p3.start = datetime.fromisoformat(self.p3.start)
        db.session.add(self.p3)
        db.session.commit()

        # setting query details
        request_body = {
            "EID": 10,
            "SID": self.p3.SID,
            "CID": self.p3.CID,
            "start": t1,
            "content_name" : "How are you",
            "LID" : "1"
        }

        # calling update_viewed_contents function via flask route
        response = self.client.post("/update_viewed_contents",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f"Progress record with EID: 10, SID: {self.p3.SID}, CID: {self.p3.CID}, start: {t1} does not exist in the database"    
        })

if __name__ == '__main__':
    #For jenkins
    # import xmlrunner
    # unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    #For local tests
    unittest.main()