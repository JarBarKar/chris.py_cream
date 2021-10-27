import unittest
import flask_testing
import json
from app import app, db, Section
from datetime import datetime


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app

    def setUp(self):
        self.s1 = Section(SID='G1', CID='IS111', start=datetime.fromisoformat("2021-04-01 09:15:00"), end=datetime.fromisoformat("2021-05-01 09:15:00"), vacancy=50, TID=1)
        self.s2 = Section(SID='G2', CID='IS111', start=datetime.fromisoformat("2021-04-01 09:15:00"), end=datetime.fromisoformat("2021-05-01 09:15:00"), vacancy=50, TID=1)
        self.s3 = Section(SID='G3', CID='IS333', start=datetime.fromisoformat("2021-04-01 09:15:00"), end=datetime.fromisoformat("2021-06-01 09:15:00"), vacancy=50, TID=3)
        
        db.create_all()


    def tearDown(self):
        self.s1 = None
        self.s2 = None
        self.s3 = None
        db.session.remove()
        db.drop_all()

### SECTION TEST CASES ###
class TestViewSections(TestApp):
    # Testing function when database has all sections using TID
    def test_view_sections_by_TID_0(self):
        # calling view_sections function via flask route
        request_body = {
            'TID': self.s1.TID
        }
        # adding two sections to database
        db.session.add(self.s1)
        db.session.add(self.s2)
        db.session.commit()


        response = self.client.post("/view_sections",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
                'data' :[
                {
                'SID': 'G1',
                'CID': 'IS111',
                'start': 'Thu, 01 Apr 2021 09:15:00 GMT',
                'end': 'Sat, 01 May 2021 09:15:00 GMT',
                'vacancy': 50,
                'TID': 1
                },
                {
                'SID': 'G2',
                'CID': 'IS111',
                'start': 'Thu, 01 Apr 2021 09:15:00 GMT',
                'end': 'Sat, 01 May 2021 09:15:00 GMT',
                'vacancy': 50,
                'TID': 1
                }
            ],
            'message' : f"All sections are retrieved for Trainer's ID {self.s1.TID}"
        })

    # Testing failed case when there are no database
    def test_view_sections_not_in_database(self):
        # calling create_sections function via flask route
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'start':datetime.isoformat(self.s1.start),
            'end': datetime.isoformat(self.s1.end),
            'vacancy': self.s1.vacancy,
            'TID': self.s1.TID
        }

        response = self.client.post("/view_sections",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "There are no sections retrieved"
        })

    # Testing failed case when there are no TID inserted
    def test_view_sections_missing_TID(self):
        # calling view_sections function via flask route
        request_body = {
        }

        response = self.client.post("/view_sections",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "TID is not found"
        })

    # Testing failed case when unknown TID inserted
    def test_view_sections_unknown_TID(self):
        # calling view_sections function via flask route
        request_body = {
            "TID": "GOOD EVENING"
        }

        response = self.client.post("/view_sections",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "There are no sections retrieved"
        })


class TestCreateSection(TestApp):
    # Testing positive case where section can be created
    def test_create_section(self):
        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'start':datetime.isoformat(self.s1.start),
            'end': datetime.isoformat(self.s1.end),
            'vacancy': self.s1.vacancy,
            'TID': self.s1.TID
        }

        # calling create_section function via flask route
        response = self.client.post("/create_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {
                'SID': 'G1',
                'CID': 'IS111',
                'start': 'Thu, 01 Apr 2021 09:15:00 GMT',
                'end': 'Sat, 01 May 2021 09:15:00 GMT',
                'vacancy': 50,
                'TID': 1
            },
            'message': f"Section {self.s1.SID} has been inserted successfully into the database"
        })

        # Testing failed case where SID is missing
    def test_create_course_missing_SID(self):
        # setting section details
        request_body = {
            'CID': self.s1.CID,
            'start':datetime.isoformat(self.s1.start),
            'end': datetime.isoformat(self.s1.end),
            'vacancy': self.s1.vacancy,
            'TID': self.s1.TID
        }

        # calling create_section function via flask route
        response = self.client.post("/create_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': "SID not found"
        })

        # Testing failed case where SID is missing
    def test_create_course_missing_CID(self):
        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'start':datetime.isoformat(self.s1.start),
            'end': datetime.isoformat(self.s1.end),
            'vacancy': self.s1.vacancy,
            'TID': self.s1.TID
        }

        # calling create_section function via flask route
        response = self.client.post("/create_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': "CID not found"
        })
        
        # Testing failed case where start datetime is missing
    def test_create_course_missing_start(self):
        # setting section details
        request_body = {
            'CID': self.s1.CID,
            'SID': self.s1.SID,
            'end': datetime.isoformat(self.s1.end),
            'vacancy': self.s1.vacancy,
            'TID': self.s1.TID
        }

        # calling create_section function via flask route
        response = self.client.post("/create_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': "start not found"
        })
    
        # Testing failed case where start datetime and CID is missing
    def test_create_course_missing_start_CID(self):
        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'end': datetime.isoformat(self.s1.end),
            'vacancy': self.s1.vacancy,
            'TID': self.s1.TID
        }

        # calling create_section function via flask route
        response = self.client.post("/create_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': "CID,start not found"
        })

        # Testing failed case where start datetime, CID, SID is missing
    def test_create_course_missing_SID_start_CID(self):
        # setting section details
        request_body = {
            'end': datetime.isoformat(self.s1.end),
            'vacancy': self.s1.vacancy,
            'TID': self.s1.TID
        }

        # calling update_course_name function via flask route
        response = self.client.post("/create_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': "CID,SID,start not found"
        })

     # Testing failed case where start datetime, CID, SID, end, TID is missing
    def test_create_course_missing_all(self):
        # setting section details
        request_body = {
        }

        # calling create_section function via flask route
        response = self.client.post("/create_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': "CID,SID,start,end,TID,vacancy not found"
        })
    
class TestQuerySections(TestApp):
    # Testing function when database has all sections using CID
    def test_query_sections_by_CID(self):
        # calling query_section function via flask route
        request_body = {
            'CID': self.s1.CID
        }
        # adding two sections to database
        db.session.add(self.s1)
        db.session.add(self.s2)
        db.session.add(self.s3)
        db.session.commit()

        response = self.client.post("/query_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
                'data' :[
                {
                'SID': 'G1',
                'CID': 'IS111',
                'start': 'Thu, 01 Apr 2021 09:15:00 GMT',
                'end': 'Sat, 01 May 2021 09:15:00 GMT',
                'vacancy': 50,
                'TID': 1
                },
                {
                'SID': 'G2',
                'CID': 'IS111',
                'start': 'Thu, 01 Apr 2021 09:15:00 GMT',
                'end': 'Sat, 01 May 2021 09:15:00 GMT',
                'vacancy': 50,
                'TID': 1
                }
            ],
            'message' : f"{self.s1.CID} has been query successfully from the database"
        })

    # Testing failed case when there are no database
    def test_query_section_not_in_database(self):
        # calling query_section function via flask route
        request_body = {
            'CID': self.s1.CID
        }

        response = self.client.post("/query_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Section cannot be query"
        })

    # Testing failed case when there are no CID inserted
    def test_view_sections_missing_CID(self):
        # calling query_section function via flask route
        request_body = {
        }

        response = self.client.post("/query_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Section cannot be query"
        })

    # Testing failed case when unknown CID inserted
    def test_view_sections_unknown_CID(self):
        # calling view_sections function via flask route
        request_body = {
            "CID": "GOOD EVENING"
        }

        response = self.client.post("/query_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Section cannot be query"
        })
    
    # Testing failed case when SID inserted
    def test_view_sections_SID(self):
        # calling query_section function via flask route
        request_body = {
            "SID": "GOOD EVENING"
        }

        response = self.client.post("/query_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json') 

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Section cannot be query"
        })

        
class TestDeleteSection(TestApp):
    # Testing positive case where section is deleted
    def test_delete_section_in_database(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()
        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID,
            'start': datetime.isoformat(self.s1.start)
        }

        # calling delete_section function via flask route
        response = self.client.post("/delete_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message': f"Section {self.s1.SID} has been deleted successfully from the database"
        })
    

    # Testing negative case where missing SID
    def test_delete_section_missing_SID(self):
        # setting section details
        request_body = {
            'CID': self.s1.CID,
            'start': datetime.isoformat(self.s1.start)
        }

        # calling delete_section function via flask route
        response = self.client.post("/delete_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': "SID not found"
        })
    
        # Testing negative case where missing SID
    def test_delete_section_missing_CID(self):
        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'start': datetime.isoformat(self.s1.start)
        }

        # calling delete_section function via flask route
        response = self.client.post("/delete_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': "CID not found"
        })
    
        # Testing negative case where missing SID
    def test_delete_section_missing_start(self):
        # setting section details
        request_body = {
            'SID': self.s1.SID,
            'CID': self.s1.CID
        }

        # calling delete_section function via flask route
        response = self.client.post("/delete_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': "start not found"
        })

        # Testing negative case where missing SID
    def test_delete_section_missing_all(self):
        # setting section details
        request_body = {
        }

        # calling delete_section function via flask route
        response = self.client.post("/delete_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': "SID,CID,start not found"
        })

class TestUpdateSection(TestApp):
    # Testing positive case where section's vacancy is updated
    def test_update_section_vacancy_in_database(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            "SID": self.s1.SID,
            "CID": self.s1.CID,
            'start': datetime.isoformat(self.s1.start),
            "end": datetime.isoformat(self.s1.end),
            "vacancy": 10,
            "TID": self.s1.TID
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {
                'SID': 'G1',
                'CID': 'IS111',
                'start': 'Thu, 01 Apr 2021 09:15:00 GMT',
                'end': 'Sat, 01 May 2021 09:15:00 GMT',
                'vacancy': 10,
                'TID': 1
            },
            'message': f"Section {self.s1.SID}'s details have been updated successfully in the database"
            
        })

    # Testing positive case where section's TID is updated
    def test_update_section_TID_in_database(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            "SID": self.s1.SID,
            "CID": self.s1.CID,
            'start': datetime.isoformat(self.s1.start),
            "end": datetime.isoformat(self.s1.end),
            "vacancy": self.s1.vacancy,
            "TID": 100
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {
                'SID': 'G1',
                'CID': 'IS111',
                'start': 'Thu, 01 Apr 2021 09:15:00 GMT',
                'end': 'Sat, 01 May 2021 09:15:00 GMT',
                'vacancy': 50,
                'TID': 100
            },
            'message': f"Section {self.s1.SID}'s details have been updated successfully in the database"
            
        })

    # Testing positive case where section's end is updated
    def test_update_section_end_in_database(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            "SID": self.s1.SID,
            "CID": self.s1.CID,
            'start': datetime.isoformat(self.s1.start),
            "end": "2021-08-01 09:15:00",
            "vacancy": self.s1.vacancy,
            "TID": self.s1.TID
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {
                'SID': 'G1',
                'CID': 'IS111',
                'start': 'Thu, 01 Apr 2021 09:15:00 GMT',
                'end': 'Sun, 01 Aug 2021 09:15:00 GMT',
                'vacancy': 50,
                'TID': 1
            },
            'message': f"Section {self.s1.SID}'s details have been updated successfully in the database"
            
        })

    # Testing positive case where section's end,vacancy,TID is updated
    def test_update_section_all_in_database(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            "SID": self.s1.SID,
            "CID": self.s1.CID,
            'start': datetime.isoformat(self.s1.start),
            "end": "2021-08-01 09:15:00",
            "vacancy": 1,
            "TID": 1000
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {
                'SID': 'G1',
                'CID': 'IS111',
                'start': 'Thu, 01 Apr 2021 09:15:00 GMT',
                'end': 'Sun, 01 Aug 2021 09:15:00 GMT',
                'vacancy': 1,
                'TID': 1000
            },
            'message': f"Section {self.s1.SID}'s details have been updated successfully in the database"
            
        })
    

    # Testing negative case where SID is not in database
    def test_update_section_SID_not_in_database(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            "SID": "HELLO GOOD NIGHT",
            "CID": self.s1.CID,
            "start": datetime.isoformat(self.s1.start),
            "end": datetime.isoformat(self.s1.end),
            "vacancy": self.s1.CID,
            "TID": self.s1.TID
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Section is not found"
        })

    # Testing negative case where CID is not in database
    def test_update_section_CID_not_in_database(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            "SID": self.s1.SID,
            "CID": "GOOD NIGHT",
            "start": datetime.isoformat(self.s1.start),
            "end": datetime.isoformat(self.s1.end),
            "vacancy": self.s1.CID,
            "TID": self.s1.TID
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Section is not found"
        })
    
    # Testing negative case where start is not in database
    def test_update_section_start_not_in_database(self):
        # adding one section to database
        db.session.add(self.s1)
        db.session.commit()

        # setting section details
        request_body = {
            "SID": self.s1.SID,
            "CID": self.s1.CID,
            "start": "ETHEREUM TO THE MOON",
            "end": "31/12/9999 23:59:59",
            "vacancy": self.s1.CID,
            "TID": self.s1.TID
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Section is not found"
        })

    # Testing negative case where section is never in the database
    def test_update_section_not_in_database(self):

        # setting section details
        request_body = {
            "SID": self.s1.SID,
            "CID": self.s1.CID,
            "start": datetime.isoformat(self.s1.start),
            "end": datetime.isoformat(self.s1.end),
            "vacancy": self.s1.CID,
            "TID": self.s1.TID
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "Section is not found"
        })
    
    # Testing negative case where section is never in the database
    def test_update_section_CID_not_in_request(self):
        # setting section details
        request_body = {
            "SID": self.s1.SID,
            "start": datetime.isoformat(self.s1.start),
            "end": datetime.isoformat(self.s1.end),
            "vacancy": self.s1.CID,
            "TID": self.s1.TID
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "CID not found"
        })
    
    def test_update_section_SID_not_in_request(self):

        # setting section details
        request_body = {
            "CID" : self.s1.CID,
            "start": datetime.isoformat(self.s1.start),
            "end": datetime.isoformat(self.s1.end),
            "vacancy": self.s1.CID,
            "TID": self.s1.TID
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "SID not found"
        })
    
    def test_update_section_start_not_in_request(self):
        # setting section details
        request_body = {
            "SID": self.s1.SID,
            "CID": self.s1.CID,
            "end": datetime.isoformat(self.s1.end),
            "vacancy": self.s1.CID,
            "TID": self.s1.TID
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "start not found"
        })
    
    def test_update_section_empty_request(self):
        # setting section details
        request_body = {
        }

        # calling update_section function via flask route
        response = self.client.post("/update_section",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": "SID,CID,start,end,vacancy,TID not found"
        })

### SECTION TEST CASES ###

if __name__ == '__main__':
    #For jenkins
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    #For local tests
    # unittest.main()
