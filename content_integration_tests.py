from typing import ContextManager
import unittest
import flask_testing
import json
from app import app, db, Content
from datetime import datetime


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app

    def setUp(self):
        self.s1 = Content(SID='G1', CID='IS111', LID='1',start='2021-10-21 09:15:00', content_name='Lesson slides', content_type='pdf', link='slidelink')
        self.s2 = Content(SID='G1', CID='IS111', LID='1',start='2021-10-21 09:15:00', content_name='Lesson video', content_type='video', link='videolink')
        self.s3 = Content(SID='G1', CID='IS111', LID='2',start='2021-10-21 09:15:00', content_name='', content_type='video', link='videolink')
        
        db.create_all()


    def tearDown(self):
        self.s1 = None
        self.s2 = None
        self.s3 = None
        db.session.remove()
        db.drop_all()

### SECTION content TEST CASES ###
class TestViewAllSectionContent(TestApp):
    # Testing function when database has all sections using TID
    def test_view_all_section_content_by_SID_CID(self):
        # calling view_section_content function via flask route
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'start': self.s1.start
        }
        # adding two sections to database
        self.s1.start = datetime.fromisoformat(self.s1.start)
        self.s2.start = datetime.fromisoformat(self.s2.start)
        db.session.add(self.s1)
        db.session.add(self.s2)
        db.session.commit()
        response = self.client.post("/view_all_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
                'data' :[
                {
                'SID': 'G1',
                'CID': 'IS111',
                'LID': '1',
                'start': '2021-10-21 09:15:00',
                'content_name': 'Lesson slides',
                'content_type': 'pdf',
                'link': 'slidelink'
                },
                {
                'SID': 'G1',
                'CID': 'IS111',
                'LID': '1',
                'start': '2021-10-21 09:15:00',
                'content_name': 'Lesson video',
                'content_type': 'video',
                'link': 'videolink'
                }
            ],
            'message' : f"All sections content are retrieved for section {self.s1.CID, self.s1.SID}"
        })

    # Testing failed case when there are no database
    def test_view_all_section_content_not_in_database(self):
        # calling view_section_content function via flask route
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'start': self.s1.start
        }

        response = self.client.post("/view_all_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "There are no section content retrieved"
        })

    # Testing failed case when there are no TID inserted
    def test_view_all_section_content_missing_SID_CID(self):
        # calling view_section_content function via flask route
        request_body = {
        }

        response = self.client.post("/view_all_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Section content ['SID', 'CID', 'start'] is not present, no section content is retrieved from database"
        })

    # Testing failed case when unknown TID inserted
    def test_view_all_section_content_unknown_SID(self):
        # calling view_all_section_content function via flask route
        request_body = {
            "SID": "GOOD EVENING",
            'CID': self.s1.CID,
            'start': self.s1.start
        }

        response = self.client.post("/view_all_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "There are no section content retrieved"
        })

class TestViewLessonContent(TestApp):
    # Testing positive testcase 
    def test_view_content_by_SID_CID_LID(self):
        # calling view_lesson_content function via flask route
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'LID': self.s1.LID,
            'start': self.s1.start
        }
        # adding two content to database
        self.s1.start = datetime.fromisoformat(self.s1.start)
        self.s2.start = datetime.fromisoformat(self.s2.start)
        db.session.add(self.s1)
        db.session.add(self.s2)
        db.session.commit()
        response = self.client.post("/view_lesson_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
                'data' :[
                {
                'CID': 'IS111',
                'LID': '1',
                'SID': 'G1',
                'content_name': 'Lesson slides',
                'content_type': 'pdf',
                'link': 'slidelink',
                'start': '2021-10-21 09:15:00'
                },
                {
                'CID': 'IS111',
                'LID': '1',
                'SID': 'G1',
                'content_name': 'Lesson video',
                'content_type': 'video',
                'link': 'videolink',
                'start': '2021-10-21 09:15:00'
                }
            ],
            'message' : f"All content are retrieved for lesson {self.s1.CID, self.s1.SID, self.s1.LID}"
        })

    # Testing failed case when there are no database
    def test_view_all_lesson_content_not_in_database(self):
        # calling view_lesson_content function via flask route
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'LID': self.s1.LID,
            'start': self.s1.start
        }

        response = self.client.post("/view_lesson_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "There are no content retrieved"
        })

    # Testing failed case when there are no TID inserted
    def test_lesson_content_missing_SID_CID_LID(self):
        # calling view_lesson_content function via flask route
        request_body = {
        }

        response = self.client.post("/view_lesson_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Content ['SID', 'CID', 'LID', 'start'] is not present, no content is retrieved from database"
        })

    # Testing failed case when unknown SID inserted
    def test_view_lesson_content_unknown_SID(self):
        # calling view_lesson_content function via flask route
        request_body = {
            "SID": "GOOD EVENING",
            'CID': self.s1.CID,
            'LID': self.s1.LID,
            'start': self.s1.start
        }

        response = self.client.post("/view_lesson_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "There are no content retrieved"
        })

class TestCreateContent(TestApp):
    # Testing positive case where content can be created
    def test_create_material(self):
        # setting content details
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'LID': self.s1.LID,
            'start': self.s1.start,
            'content_name': self.s1.content_name,
            'content_type': self.s1.content_type,
            'link': self.s1.link
        }

        # calling create_material function via flask route
        response = self.client.post("/create_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {'CID': 'IS111','LID': '1','SID': 'G1','content_name': 'Lesson slides','content_type': 'pdf', 'link': 'slidelink','start': '2021-10-21 09:15:00'},
            'message': f"Content {self.s1.content_name} has been inserted successfully into the database"
            
        })

        # Testing failed case where SID is missing
    def test_create_content_missing_SID(self):
        # setting content details
        request_body = {
            'CID': self.s1.CID,
            'LID': self.s1.LID,
            'start': self.s1.start,
            'content_name': self.s1.content_name,
            'content_type': self.s1.content_type,
            'link': self.s1.link
        }

        # calling create_material function via flask route
        response = self.client.post("/create_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Content ['SID'] is not present, content is not inserted successfully into the database"
        })

        # Testing failed case where SID is missing
    def test_create_course_missing_all_input(self):
        # setting content details
        request_body = {
        }

        # calling create_material function via flask route
        response = self.client.post("/create_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Content ['SID', 'CID', 'LID', 'start', 'content_name', 'content_type', 'link'] is not present, content is not inserted successfully into the database"
        })
        

class TestUpdateContent(TestApp):
    # Testing positive case where content name is updated
    def test_update_content(self):
        # adding one content to database
        t1 = self.s1.start
        self.s1.start = datetime.fromisoformat(self.s1.start)
        db.session.add(self.s1)
        db.session.commit()

        # setting content details
        request_body = {
            'old_SID': self.s1.SID,
            'old_CID': self.s1.CID,
            'old_LID': self.s1.LID,
            'old_start': t1,
            'old_content_name': self.s1.content_name,
            'old_content_type': self.s1.content_type,
            'old_link': self.s1.link,
            'content_name': 'new lesson slides'
        }

        # calling update_content function via flask route
        response = self.client.post("/update_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {
                'SID': 'G1',
                'CID': 'IS111',
                'LID': '1',
                'start': '2021-10-21 09:15:00',
                'content_name': 'new lesson slides',
                'content_type': 'pdf',
                'link': 'slidelink'
            },
            "message": f"Content {self.s1.CID, self.s1.SID, self.s1.LID, 'new lesson slides'}'s details have been updated successfully in the database"
            
        })

    

    # Testing negative case where SID is not in database
    def test_update_content_SID_not_in_database(self):
        # adding one content to database
        t1 = self.s1.start
        self.s1.start = datetime.fromisoformat(self.s1.start)
        db.session.add(self.s1)
        db.session.commit()

        # setting content details
        request_body = {
            'old_SID': 'do not exist',
            'old_CID': self.s1.CID,
            'old_LID': self.s1.LID,
            'old_start': t1,
            'old_content_name': self.s1.content_name,
            'old_content_type': self.s1.content_type,
            'old_link': self.s1.link,
            'content_name': 'new lesson slides'
        }

        # calling update_content function via flask route
        response = self.client.post("/update_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Content {request_body['old_CID'], request_body['old_SID'], request_body['old_LID'], request_body['old_content_name']} do not exist"
        })

    
    def test_update_content_missing_SID(self):
        t1 = self.s1.start
        self.s1.start = datetime.fromisoformat(self.s1.start)
        # setting content details
        request_body = {
            'old_CID': self.s1.CID,
            'old_LID': self.s1.LID,
            'old_start': t1,
            'old_content_name': self.s1.content_name,
            'old_content_type': self.s1.content_type,
            'old_link': self.s1.link,
            'content_name': 'new lesson slides'
        }

        # calling update_content function via flask route
        response = self.client.post("/update_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Content ['old_SID'] is not present, content is not inserted successfully into the database"
        })
    
    def test_update_content_empty_request(self):
        self.s1.start = datetime.fromisoformat(self.s1.start)
        # setting content details
        request_body = {
        }

        # calling update_content function via flask route
        response = self.client.post("/update_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Content ['old_SID', 'old_CID', 'old_LID', 'old_start', 'old_content_name', 'old_content_type', 'old_link'] is not present, content is not inserted successfully into the database"
        })


class TestDeleteMateria(TestApp):
    # Testing positive case where content name is updated
    def test_delete_content(self):
        # adding one content to database
        t1 = self.s1.start
        self.s1.start = datetime.fromisoformat(self.s1.start)
        db.session.add(self.s1)
        db.session.commit()

        # setting content details
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'LID': self.s1.LID,
            'start': t1,
            'content_name': self.s1.content_name,
        }

        # calling delete_content function via flask route
        response = self.client.post("/delete_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": f"Content { self.s1.CID, self.s1.SID, self.s1.LID, self.s1.content_name} has been deleted successfully from the database"    
        })

    def test_delete_content_missing_CID(self):
        # adding one content to database
        t1 = self.s1.start
        self.s1.start = datetime.fromisoformat(self.s1.start)
        db.session.add(self.s1)
        db.session.commit()

        # setting content details
        request_body = {
            'SID': self.s1.SID,
            'LID': self.s1.LID,
            'start': t1,
            'content_name': self.s1.content_name,
        }

        # calling delete_content function via flask route
        response = self.client.post("/delete_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Content ['CID'] is not present, content is not successfully deleted"
        })

    def test_delete_content_not_in_database(self):
        # adding no content to database
        t1 = self.s1.start
        self.s1.start = datetime.fromisoformat(self.s1.start)
        # setting content details
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'LID': self.s1.LID,
            'start': t1,
            'content_name': self.s1.content_name,
        }

        # calling delete_content function via flask route
        response = self.client.post("/delete_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Content {self.s1.CID, self.s1.SID, self.s1.LID, self.s1.content_name} do not exist"
        })



# ### CONTENT TEST CASES ###

if __name__ == '__main__':
    #For jenkins
    # import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    
    # For local tests
    # unittest.main()
