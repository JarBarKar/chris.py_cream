from typing import ContextManager
import unittest
import flask_testing
import json
from app import app, db, Section, Section_content
from datetime import datetime


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app

    def setUp(self):
        self.s1 = Section_content(SID='G1', CID='IS111', LID=1, QID=1, content_name='Lesson slides', content_type='pdf', link='slidelink')
        self.s2 = Section_content(SID='G1', CID='IS111', LID=1, QID=1, content_name='Lesson video', content_type='video', link='videolink')
        self.s3 = Section_content(SID='G1', CID='IS111', LID=2, QID=1, content_name='', content_type='video', link='videolink')
        
        db.create_all()


    def tearDown(self):
        self.s1 = None
        self.s2 = None
        self.s3 = None
        db.session.remove()
        db.drop_all()

### SECTION TEST CASES ###
class TestViewSectionContent(TestApp):
    # Testing function when database has all sections using TID
    def test_view_section_content_by_SID_CID(self):
        # calling view_section_content function via flask route
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID
        }
        # adding two sections to database
        db.session.add(self.s1)
        db.session.add(self.s2)
        db.session.commit()
        response = self.client.post("/view_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
                'data' :[
                {
                'SID': 'G1',
                'CID': 'IS111',
                'LID': 1,
                'QID': 1,
                'content_name': 'Lesson slides',
                'content_type': 'pdf',
                'link': 'slidelink'
                },
                {
                'SID': 'G1',
                'CID': 'IS111',
                'LID': 1,
                'QID': 1,
                'content_name': 'Lesson video',
                'content_type': 'video',
                'link': 'videolink'
                }
            ],
            'message' : f"All sections content are retrieved for section {self.s1.CID, ' ', self.s1.SID}"
        })

    # Testing failed case when there are no database
    def test_view_section_content_not_in_database(self):
        # calling view_section_content function via flask route
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID
        }

        response = self.client.post("/view_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "There are no section content retrieved"
        })

    # Testing failed case when there are no TID inserted
    def test_view_section_content_missing_SID_CID(self):
        # calling view_section_content function via flask route
        request_body = {
        }

        response = self.client.post("/view_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Section content ['SID', 'CID'] is not present, no section content is retrieved from database"
        })

    # Testing failed case when unknown TID inserted
    def test_view_section_content_unknown_SID(self):
        # calling view_section_content function via flask route
        request_body = {
            "SID": "GOOD EVENING",
            'CID': self.s1.CID
        }

        response = self.client.post("/view_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "There are no section content retrieved"
        })


class TestCreateSection(TestApp):
    # Testing positive case where section can be created
    def test_create_material(self):
        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'LID': self.s1.LID,
            'QID': self.s1.QID,
            'content_name': self.s1.content_name,
            'content_type': self.s1.content_type,
            'link': self.s1.link
        }

        # calling create_material function via flask route
        response = self.client.post("/create_material",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {'CID': 'IS111','LID': 1,'QID': 1,'SID': 'G1','content_name': 'Lesson slides','content_type': 'pdf','link': 'slidelink'},
            'message': f"Section {self.s1.content_name} has been inserted successfully into the database"
            
        })

        # Testing failed case where SID is missing
    def test_create_material_missing_SID(self):
        # setting section details
        request_body = {
            'CID': self.s1.CID,
            'LID': self.s1.LID,
            'QID': self.s1.QID,
            'content_name': self.s1.content_name,
            'content_type': self.s1.content_type,
            'link': self.s1.link
        }

        # calling create_material function via flask route
        response = self.client.post("/create_material",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Section content ['SID'] is not present, section content is not inserted successfully into the database"
        })

        # Testing failed case where SID is missing
    def test_create_course_missing_all_input(self):
        # setting section details
        request_body = {
        }

        # calling create_material function via flask route
        response = self.client.post("/create_material",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Section content ['SID', 'CID', 'LID', 'QID', 'content_name', 'content_type', 'link'] is not present, section content is not inserted successfully into the database"
        })
        
#         # Testing failed case where start datetime is missing
#     def test_create_course_missing_start(self):
#         # setting section details
#         request_body = {
#             'CID': self.s1.CID,
#             'SID': self.s1.SID,
#             'end': "01/01/0001 00:00:00",
#             'vacancy': self.s1.vacancy,
#             'TID': self.s1.TID
#         }

#         # calling create_material function via flask route
#         response = self.client.post("/create_material",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')

#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             'message': "start not found"
#         })
    
#         # Testing failed case where start datetime and CID is missing
#     def test_create_course_missing_start_CID(self):
#         # setting section details
#         request_body = {
#             'SID': self.s1.SID,
#             'end': "01/01/0001 00:00:00",
#             'vacancy': self.s1.vacancy,
#             'TID': self.s1.TID
#         }

#         # calling create_material function via flask route
#         response = self.client.post("/create_material",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')

#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             'message': "CID,start not found"
#         })

#         # Testing failed case where start datetime, CID, SID is missing
#     def test_create_course_missing_SID_start_CID(self):
#         # setting section details
#         request_body = {
#             'end': "01/01/0001 00:00:00",
#             'vacancy': self.s1.vacancy,
#             'TID': self.s1.TID
#         }

#         # calling update_course_name function via flask route
#         response = self.client.post("/create_material",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')

#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             'message': "CID,SID,start not found"
#         })

#      # Testing failed case where start datetime, CID, SID, end, TID is missing
#     def test_create_course_missing_all(self):
#         # setting section details
#         request_body = {
#         }

#         # calling create_material function via flask route
#         response = self.client.post("/create_material",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')

#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             'message': "CID,SID,start,end,TID not found"
#         })
    
# class TestQuerySections(TestApp):
#     # Testing function when database has all sections using CID
#     def test_query_sections_by_CID(self):
#         # calling query_section function via flask route
#         request_body = {
#             'CID': self.s1.CID
#         }
#         # adding two sections to database
#         db.session.add(self.s1)
#         db.session.add(self.s2)
#         db.session.add(self.s3)
#         db.session.commit()

#         response = self.client.post("/query_section",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json') 

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json, {
#                 'data' :[
#                 {
#                 'SID': 'G1',
#                 'CID': 'IS111',
#                 'start': 'Mon, 01 Jan 0001 00:00:00 GMT',
#                 'end': 'Mon, 01 Jan 0001 00:00:00 GMT',
#                 'vacancy': 50,
#                 'TID': 1
#                 },
#                 {
#                 'SID': 'G2',
#                 'CID': 'IS111',
#                 'start': 'Mon, 01 Jan 0001 00:00:00 GMT',
#                 'end': 'Mon, 01 Jan 0001 00:00:00 GMT',
#                 'vacancy': 50,
#                 'TID': 1
#                 }
#             ],
#             'message' : f"{self.s1.CID} has been query successfully from the database"
#         })

#     # Testing failed case when there are no database
#     def test_query_section_not_in_database(self):
#         # calling query_section function via flask route
#         request_body = {
#             'CID': self.s1.CID
#         }

#         response = self.client.post("/query_section",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json') 

#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             "message": "Section cannot be query"
#         })

#     # Testing failed case when there are no CID inserted
#     def test_view_section_content_missing_CID(self):
#         # calling query_section function via flask route
#         request_body = {
#         }

#         response = self.client.post("/query_section",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json') 

#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             "message": "Section cannot be query"
#         })

#     # Testing failed case when unknown CID inserted
#     def test_view_section_content_unknown_CID(self):
#         # calling view_section_content function via flask route
#         request_body = {
#             "CID": "GOOD EVENING"
#         }

#         response = self.client.post("/query_section",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json') 

#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             "message": "Section cannot be query"
#         })
    
#     # Testing failed case when SID inserted
#     def test_view_section_content_SID(self):
#         # calling query_section function via flask route
#         request_body = {
#             "SID": "GOOD EVENING"
#         }

#         response = self.client.post("/query_section",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json') 

#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             "message": "Section cannot be query"
#         })

        
# class TestDeleteSection(TestApp):
#     # Testing positive case where section is deleted
#     def test_delete_section_in_database(self):
#         # adding one section to database
#         db.session.add(self.s1)
#         db.session.commit()
#         # setting section details
#         request_body = {
#             'SID': self.s1.SID,
#             'CID': self.s1.CID,
#             'start': "01/01/0001 00:00:00"
#         }

#         # calling delete_section function via flask route
#         response = self.client.post("/delete_section",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json, {
#             'message': f"Section {self.s1.SID} has been deleted successfully from the database"
#         })
    

#     # Testing negative case where missing SID
#     def test_delete_section_missing_SID(self):
#         # setting section details
#         request_body = {
#             'CID': self.s1.CID,
#             'start': "01/01/0001 00:00:00"
#         }

#         # calling delete_section function via flask route
#         response = self.client.post("/delete_section",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             'message': "SID not found"
#         })
    
#         # Testing negative case where missing SID
#     def test_delete_section_missing_CID(self):
#         # setting section details
#         request_body = {
#             'SID': self.s1.SID,
#             'start': "01/01/0001 00:00:00"
#         }

#         # calling delete_section function via flask route
#         response = self.client.post("/delete_section",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             'message': "CID not found"
#         })
    
#         # Testing negative case where missing SID
#     def test_delete_section_missing_start(self):
#         # setting section details
#         request_body = {
#             'SID': self.s1.SID,
#             'CID': self.s1.CID
#         }

#         # calling delete_section function via flask route
#         response = self.client.post("/delete_section",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             'message': "start not found"
#         })

#         # Testing negative case where missing SID
#     def test_delete_section_missing_all(self):
#         # setting section details
#         request_body = {
#         }

#         # calling delete_section function via flask route
#         response = self.client.post("/delete_section",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             'message': "SID,CID,start not found"
#         })
class TestUpdateSection(TestApp):
    # Testing positive case where content name is updated
    def test_update_section_content_vacancy_in_database(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            'old_SID': self.s1.SID,
            'old_CID': self.s1.CID,
            'old_LID': self.s1.LID,
            'old_QID': self.s1.QID,
            'old_content_name': self.s1.content_name,
            'old_content_type': self.s1.content_type,
            'old_link': self.s1.link,
            'content_name': 'new lesson slides'
        }

        # calling update_section_content function via flask route
        response = self.client.post("/update_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {
                'SID': 'G1',
                'CID': 'IS111',
                'LID': 1,
                'QID': 1,
                'content_name': 'new lesson slides',
                'content_type': 'pdf',
                'link': 'slidelink'
            },
            "message": f"Section content {self.s1.CID, self.s1.SID, self.s1.LID, 'new lesson slides'}'s details have been updated successfully in the database"
            
        })

#     # Testing positive case where section's TID is updated
#     def test_update_section_content_TID_in_database(self):
#         # adding one section to database
#         db.session.add(self.s1)
#         db.session.commit()

#         # setting section details
#         request_body = {
#             "SID": self.s1.SID,
#             "CID": self.s1.CID,
#             "start": "01/01/0001 00:00:00",
#             "end": "01/01/0001 00:00:00",
#             "vacancy": self.s1.vacancy,
#             "TID": 100
#         }

#         # calling update_section_content function via flask route
#         response = self.client.post("/update_section_content",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json, {
#             'data': {
#                 'SID': 'G1',
#                 'CID': 'IS111',
#                 'start': 'Mon, 01 Jan 0001 00:00:00 GMT',
#                 'end': 'Mon, 01 Jan 0001 00:00:00 GMT',
#                 'vacancy': 50,
#                 'TID': 100
#             },
#             'message': f"Section {self.s1.SID}'s details have been updated successfully in the database"
            
#         })

#     # Testing positive case where section's end is updated
#     def test_update_section_content_end_in_database(self):
#         # adding one section to database
#         db.session.add(self.s1)
#         db.session.commit()

#         # setting section details
#         request_body = {
#             "SID": self.s1.SID,
#             "CID": self.s1.CID,
#             "start": "01/01/0001 00:00:00",
#             "end": "02/01/0001 00:00:00",
#             "vacancy": self.s1.vacancy,
#             "TID": self.s1.TID
#         }

#         # calling update_section_content function via flask route
#         response = self.client.post("/update_section_content",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json, {
#             'data': {
#                 'SID': 'G1',
#                 'CID': 'IS111',
#                 'start': 'Mon, 01 Jan 0001 00:00:00 GMT',
#                 'end': 'Tue, 02 Jan 0001 00:00:00 GMT',
#                 'vacancy': 50,
#                 'TID': 1
#             },
#             'message': f"Section {self.s1.SID}'s details have been updated successfully in the database"
            
#         })

#         # Testing positive case where section's end,vacancy,TID is updated
#     def test_update_section_content_all_in_database(self):
#         # adding one section to database
#         db.session.add(self.s1)
#         db.session.commit()

#         # setting section details
#         request_body = {
#             "SID": self.s1.SID,
#             "CID": self.s1.CID,
#             "start": "01/01/0001 00:00:00",
#             "end": "02/01/0001 00:00:00",
#             "vacancy": 1,
#             "TID": 1000
#         }

#         # calling update_section_content function via flask route
#         response = self.client.post("/update_section_content",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json, {
#             'data': {
#                 'SID': 'G1',
#                 'CID': 'IS111',
#                 'start': 'Mon, 01 Jan 0001 00:00:00 GMT',
#                 'end': 'Tue, 02 Jan 0001 00:00:00 GMT',
#                 'vacancy': 1,
#                 'TID': 1000
#             },
#             'message': f"Section {self.s1.SID}'s details have been updated successfully in the database"
            
#         })
    

    # Testing negative case where SID is not in database
    def test_update_section_content_SID_not_in_database(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            'old_SID': 'do not exist',
            'old_CID': self.s1.CID,
            'old_LID': self.s1.LID,
            'old_QID': self.s1.QID,
            'old_content_name': self.s1.content_name,
            'old_content_type': self.s1.content_type,
            'old_link': self.s1.link,
            'content_name': 'new lesson slides'
        }

        # calling update_section_content function via flask route
        response = self.client.post("/update_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Section content {request_body['old_CID'], request_body['old_SID'], request_body['old_LID'], request_body['old_content_name']} do not exist"
        })

#     # Testing negative case where CID is not in database
#     def test_update_section_content_CID_not_in_database(self):
#         # adding one section to database
#         db.session.add(self.s1)
#         db.session.commit()

#         # setting section details
#         request_body = {
#             "SID": self.s1.SID,
#             "CID": "GOOD NIGHT",
#             "start": "01/01/0001 00:00:00",
#             "end": "01/01/0001 00:00:00",
#             "vacancy": self.s1.CID,
#             "TID": self.s1.TID
#         }

#         # calling update_section_content function via flask route
#         response = self.client.post("/update_section_content",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             "message": "Section is not found"
#         })
    
#     # Testing negative case where CID is not in database
#     def test_update_section_content_start_not_in_database(self):
#         # adding one section to database
#         db.session.add(self.s1)
#         db.session.commit()

#         # setting section details
#         request_body = {
#             "SID": self.s1.SID,
#             "CID": self.s1.CID,
#             "start": "blah",
#             "end": "01/01/0001 00:00:00",
#             "vacancy": self.s1.CID,
#             "TID": self.s1.TID
#         }

#         # calling update_section_content function via flask route
#         response = self.client.post("/update_section_content",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             "message": "Section is not found"
#         })

#     # Testing negative case where section is never in the database
#     def test_update_section_content_not_in_database(self):

#         # setting section details
#         request_body = {
#             "SID": self.s1.SID,
#             "CID": self.s1.CID,
#             "start": "01/01/0001 00:00:00",
#             "end": "01/01/0001 00:00:00",
#             "vacancy": self.s1.CID,
#             "TID": self.s1.TID
#         }

#         # calling update_section_content function via flask route
#         response = self.client.post("/update_section_content",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             "message": "Section is not found"
#         })
    
#     # Testing negative case where section is never in the database
#     def test_update_section_content_CID_not_in_request(self):

#         # setting section details
#         request_body = {
#             "SID": self.s1.SID,
#             "start": "01/01/0001 00:00:00",
#             "end": "01/01/0001 00:00:00",
#             "vacancy": self.s1.CID,
#             "TID": self.s1.TID
#         }

#         # calling update_section_content function via flask route
#         response = self.client.post("/update_section_content",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             "message": "CID not found"
#         })
    
#     def test_update_section_content_SID_not_in_request(self):

#         # setting section details
#         request_body = {
#             "CID" : self.s1.CID,
#             "start": "01/01/0001 00:00:00",
#             "end": "01/01/0001 00:00:00",
#             "vacancy": self.s1.CID,
#             "TID": self.s1.TID
#         }

#         # calling update_section_content function via flask route
#         response = self.client.post("/update_section_content",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {
#             "message": "SID not found"
#         })
    
    def test_update_section_content_missing_SID(self):
        # setting section details
        request_body = {
            'old_CID': self.s1.CID,
            'old_LID': self.s1.LID,
            'old_QID': self.s1.QID,
            'old_content_name': self.s1.content_name,
            'old_content_type': self.s1.content_type,
            'old_link': self.s1.link,
            'content_name': 'new lesson slides'
        }

        # calling update_section_content function via flask route
        response = self.client.post("/update_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Section content ['old_SID'] is not present, section content is not inserted successfully into the database"
        })
    
    def test_update_section_content_empty_request(self):
        # setting section details
        request_body = {
        }

        # calling update_section_content function via flask route
        response = self.client.post("/update_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Section content ['old_SID', 'old_CID', 'old_LID', 'old_QID', 'old_content_name', 'old_content_type', 'old_link'] is not present, section content is not inserted successfully into the database"
        })


class TestDeleteSectionMateria(TestApp):
    # Testing positive case where content name is updated
    def test_delete_section_content(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'LID': self.s1.LID,
            'QID': self.s1.QID,
            'content_name': self.s1.content_name,
        }

        # calling update_section_content function via flask route
        response = self.client.post("/delete_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "message": f"Section content { self.s1.CID, self.s1.SID, self.s1.LID, self.s1.content_name} has been deleted successfully from the database"    
        })

    def test_delete_section_content_missing_CID(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'LID': self.s1.LID,
            'QID': self.s1.QID,
            'content_name': self.s1.content_name,
        }

        # calling update_section_content function via flask route
        response = self.client.post("/delete_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Section content ['CID'] is not present, section content is not successfully deleted"
        })

    def test_delete_section_content_not_in_database(self):
        # adding one section to database

        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'LID': self.s1.LID,
            'QID': self.s1.QID,
            'content_name': self.s1.content_name,
        }

        # calling update_section_content function via flask route
        response = self.client.post("/delete_section_content",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Section content {self.s1.CID, self.s1.SID, self.s1.LID, self.s1.content_name} do not exist"
        })



# ### SECTION TEST CASES ###

if __name__ == '__main__':
    unittest.main()
