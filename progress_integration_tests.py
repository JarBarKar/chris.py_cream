import unittest
import flask_testing
import json
from app import app, db, Progress
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
        db.create_all()

    def tearDown(self):
        self.gq1q1 = None
        self.gq1q2 = None

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


if __name__ == '__main__':
    #For jenkins
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    #For local tests
    # unittest.main()