import unittest
from flask import Flask, request, jsonify
import flask_testing
import json
from app import app, db, Course


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app


    def setUp(self):
        self.c1 = Course(CID='IS500', name='Super Mod', prerequisites='')
        self.c2 = Course(CID='IS600', name='Super Hard Mod', prerequisites='IS500')
        self.c3 = Course(CID='IS700', name='Super Super Hard Mod', prerequisites='IS500,IS600')
        
        db.create_all()


    def tearDown(self):
        self.c1 = None
        self.c2 = None
        self.c3 = None
        db.session.remove()
        db.drop_all()

### COURSE TEST CASES ###
class TestViewCourses(TestApp):
    # Testing function when database has no courses
    def test_view_all_courses_0(self):
        # calling view_courses function via flask route
        response = self.client.get("/view_courses")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : 'There are no course retrieved'
        })


    # Testing function when database has 1 course
    def test_view_all_courses_1(self):
        # adding two courses to database
        db.session.add(self.c1)
        db.session.commit()
        
        # calling view_courses function via flask route
        response = self.client.get("/view_courses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' :[
                {
                'CID': 'IS500',
                'name': 'Super Mod',
                'prerequisites': ''
                }
            ],
            'message' : 'All courses are retrieved'
            })


    # Testing function when database has 2 course
    def test_view_all_courses_2(self):
        # adding two courses to database
        db.session.add(self.c1)
        db.session.add(self.c2)
        db.session.commit()
        
        # calling view_courses function via flask route
        response = self.client.get("/view_courses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' :[
                {
                'CID': 'IS500',
                'name': 'Super Mod',
                'prerequisites': ''
                },
                {
                'CID': 'IS600',
                'name': 'Super Hard Mod',
                'prerequisites': 'IS500'
                }],
            'message' : 'All courses are retrieved'
            })


    # Testing positive case where course is in database
    def test_query_course_in_database(self):
        # adding one course to database
        db.session.add(self.c1)
        db.session.commit()
        
        request_body = {
            'id': 1,
            'CID': self.c1.CID,
            'name': self.c1.name,
            'prerequisites': self.c1.prerequisites
        }
        # calling query_course function via flask route
        response = self.client.post("/query_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')                  
        self.assertEqual(response.status_code, 200)   
        self.assertEqual(response.json, {
            'data': {
                'CID': 'IS500',
                'name': 'Super Mod',
                'prerequisites': ''
            },
            'message' : 'IS500 has been query successfully from the database'
        })


    # Testing negative case where course is not in database
    def test_query_course_not_in_database(self):
        request_body = {
            'id': 1,
            'CID': self.c1.CID,
            'name': self.c1.name,
            'prerequisites': self.c1.prerequisites
        }
        # calling query_course function via flask route
        response = self.client.post("/query_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)                     
        self.assertEqual(response.json, {
            'message' : f'{self.c1.CID} cannot be query'
        })
    

    # Testing negative case where course is not provided in request body
    def test_query_course_missing_cid(self):
        request_body = {
            'id': 1,
            'name': self.c1.name,
            'prerequisites': self.c1.prerequisites
        }
        # calling query_course function via flask route
        response = self.client.post("/query_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)                     
        self.assertEqual(response.json, {
            'message' : f'CID is missing'
        })


class TestUpdateCourse(TestApp):
    # Testing positive case where course is in database
    def test_update_course_name_in_database(self):
        # adding one course to database
        db.session.add(self.c1)
        db.session.commit()

        # setting course details
        request_body = {
            'id' : 1,
            'CID': self.c1.CID,
            'name': 'This is a new name',
            'prerequisites': self.c1.prerequisites
        }

        # calling update_course_name function via flask route
        response = self.client.post("/update_course_name",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {
                'CID': 'IS500',
                'name': 'This is a new name',
                'prerequisites': ''
            },
            'message': 'IS500 name has been updated successfully in the database'
            
        })
    

    # Testing negative case where course is not in database
    def test_update_course_name_not_in_database(self):
       
        # setting course details
        request_body = {
            'id' : 1,
            'CID': self.c1.CID,
            'name': 'This is a new name',
            'prerequisites': self.c1.prerequisites
        }

        # calling update_course_name function via flask route
        response = self.client.post("/update_course_name",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f'{self.c1.CID} name is not updated'
            
        })


    # Testing negative case where course is not in request body
    def test_update_course_name_missing_cid(self):
        # setting course details
        request_body = {
            'id' : 1,
            'name': 'This is a new name',
            'prerequisites': self.c1.prerequisites
        }

        # calling update_course_name function via flask route
        response = self.client.post("/update_course_name",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f'CID is missing'
            
        })


    # Testing positive case where course is in database
    def test_update_course_prerequisites_in_database(self):
        # adding one course to database
        db.session.add(self.c1)
        db.session.commit()

        # setting course details
        request_body = {
            'id' : 1,
            'CID': self.c1.CID,
            'name': self.c1.name,
            'prerequisites': 'IS111,IS112'
        }

        # calling update_course_name function via flask route
        response = self.client.post("/update_course_prerequisites",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'CID': 'IS500',
                'name': 'Super Mod',
                'prerequisites': 'IS111,IS112'
            },
            'message' : 'IS500 prerequisites has been updated successfully in the database'
        })


    # Testing negative case where course is not in database
    def test_update_course_prerequisites_not_in_database(self):
        # setting course details
        request_body = {
            'id' : 1,
            'CID': self.c1.CID,
            'name': self.c1.name,
            'prerequisites': 'IS111,IS112'
        }

        # calling update_course_name function via flask route
        response = self.client.post("/update_course_prerequisites",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f'{self.c1.CID} prerequisites is not updated'
        })

    
    # Testing negative case where course is not in request body
    def test_update_course_prerequisites_missing_cid(self):
        # setting course details
        request_body = {
                'id' : 1,
                'name': self.c1.name,
                'prerequisites': 'IS111,IS112'
            }

        # calling update_course_name function via flask route
        response = self.client.post("/update_course_prerequisites",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f'CID is missing'
        })


class TestCreateCourse(TestApp):
    # Testing positive case where all details are present in request body
    def test_create_course_all_details(self):
        # setting course details
        request_body = {
            'CID': self.c1.CID,
            'name': self.c1.name,
            'prerequisites': self.c1.prerequisites
        }

        # calling create_course function via flask route
        response = self.client.post("/create_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {
                'CID': 'IS500',
                'name': 'Super Mod',
                'prerequisites': ''
                },
            'message':'Super Mod has been inserted successfully into the database'
        })
    

    # Testing positive case where all details are present in request body,but prerequisites is empty
    def test_create_course_all_details_prerequisites_empty(self):
        # setting course details
        request_body = {
            'CID': self.c2.CID,
            'name': self.c2.name,
            'prerequisites': ''
        }

        # calling create_course function via flask route
        response = self.client.post("/create_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data': {
                'CID': 'IS600',
                'name': 'Super Hard Mod',
                'prerequisites': ''
                },
            'message':f'{self.c2.name} has been inserted successfully into the database'
        })
    


    # Testing negative case where CID is missing in request body
    def test_create_course_missing_cid(self):
        # setting course details
        request_body = {
            'name': self.c1.name,
            'prerequisites': self.c1.prerequisites
        }

        # calling create_course function via flask route
        response = self.client.post("/create_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message':f'{self.c1.name} is not inserted successfully into the database'
        })


    # Testing negative case where name is missing in request body
    def test_create_course_missing_name(self):
        # setting course details
        request_body = {
            'CID' : self.c1.CID,
            'prerequisites': self.c1.prerequisites
        }

        # calling create_course function via flask route
        response = self.client.post("/create_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message':f'Course name is not inserted successfully into the database'
        })


    # Testing negative case where prerequisites is missing in request body
    def test_create_course_missing_prerequisites(self):
        # setting course details
        request_body = {
            'CID' : self.c1.CID,
            'name': self.c1.name
        }

        # calling create_course function via flask route
        response = self.client.post("/create_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
    
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message':f'{self.c1.name} is not inserted successfully into the database'
        })
    

        
class TestDeleteCourse(TestApp):
    # Testing positive case where course is in database
    def test_delete_course_in_database(self):
        # adding one course to database
        db.session.add(self.c2)
        db.session.commit()
        # setting course details
        request_body = {
            'CID': self.c2.CID,
            'name': self.c2.name,
            'prerequisites': self.c2.prerequisites
        }

        # calling create_course function via flask route
        response = self.client.post("/delete_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message': f'{self.c2.CID} has been deleted successfully from the database'
        })
    

    # Testing negative case where course is not in database
    def test_delete_course_not_in_database(self):
        # setting course details
        request_body = {
            'CID': self.c2.CID,
            'name': self.c2.name,
            'prerequisites': self.c2.prerequisites
        }

        # calling create_course function via flask route
        response = self.client.post("/delete_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f'{self.c2.CID} is not deleted'
        })


    # Testing negative case where course is not in request body
    def test_delete_course_missing_cid(self):
        # setting course details
        request_body = {
            'name': self.c2.name,
            'prerequisites': self.c2.prerequisites
        }

        # calling create_course function via flask route
        response = self.client.post("/delete_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message': f'CID is missing'
        })
### COURSE TEST CASES ###

if __name__ == '__main__':
    unittest.main()
