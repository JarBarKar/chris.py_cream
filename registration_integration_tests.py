import unittest
import flask_testing
import json

from sqlalchemy.sql.elements import Null
from app import app, db, Course, Academic_record, Enrollment, Section
from datetime import datetime


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app


    def setUp(self):
        self.c1 = Course(CID='IS500', name='Super Mod', prerequisites='')
        self.c2 = Course(CID='IS600', name='Super Hard Mod', prerequisites='IS500')
        self.er1 = Enrollment(EID=1, SID='G2', CID='IS500', start='2021-04-10 10:09:08')
        self.er2 = Enrollment(EID=6, SID='G90', CID='IS600', start='2021-04-10 10:09:08')
        self.cd1 = Academic_record(EID=1, SID="G2", CID="IS500", start='2021-04-10 10:09:08', status='ongoing')
        self.cd2 = Academic_record(EID=2, SID="G12", CID="IS600", start='2021-04-10 10:09:08', status='ongoing')
        self.s1 = Section(SID="G1", CID="IS500", start="2021-04-01 09:15:00", end="2021-05-01 09:15:00", vacancy=50, TID=1)
        self.s2 = Section(SID="G12", CID="IS600", start="2021-04-01 09:15:00", end="2021-05-01 09:15:00", vacancy=50, TID=0)
        
        db.create_all()


    def tearDown(self):
        # self.e1 = None
        self.c1 = None
        self.c2 = None
        self.er1 = None
        self.er2 = None
        self.cd1 = None
        self.cd2 = None
        self.s1 = None
        self.s2 = None
        db.session.remove()
        db.drop_all()


### Registration TEST CASES ###
class TestEngineerSignup(TestApp):
    # Testing positive case where all details are present in request body
    def test_engineer_signup_all_details(self):
        # creating request body for signup details
        request_body = {
            'EID': self.er1.EID,
            'SID': self.er1.SID,
            'CID': self.er1.CID,
            'start': self.er1.start
        }
        
        # calling engineer_signup function via flask route
        response = self.client.post("/engineer_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' :
                {
                'EID': self.er1.EID,
                'SID': self.er1.SID,
                'CID': self.er1.CID,
                'start': self.er1.start
                }
                ,
            'message' : f'{self.er1.EID} engineer has been updated successfully in the database'
            }) 


    # Testing negative case where EID is missing in request body
    def test_engineer_signup_eid_missing(self):
        # creating request body for signup details
        request_body = {
            'SID': self.er1.SID,
            'CID': self.er1.CID,
            'start': self.er1.start
        }
        
        # calling engineer_signup function via flask route
        response = self.client.post("/engineer_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Enrollment ['EID'] is not present,  engineer is not enrolled"
            })


    # Testing negative case where SID is missing in request body
    def test_engineer_signup_sid_missing(self):
        # creating request body for signup details
        request_body = {
            'EID': self.er1.EID,
            'CID': self.er1.CID,
            'start': self.er1.start
        }
        
        # calling engineer_signup function via flask route
        response = self.client.post("/engineer_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Enrollment ['SID'] is not present,  engineer is not enrolled"
            })


    # Testing negative case where CID is missing in request body
    def test_engineer_signup_cid_missing(self):
        # creating request body for signup details
        request_body = {
            'EID': self.er1.EID,
            'SID': self.er1.SID,
            'start': self.er1.start
        }
        
        # calling engineer_signup function via flask route
        response = self.client.post("/engineer_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Enrollment ['CID'] is not present,  engineer is not enrolled"
            })
    

class TestHRViewSignup(TestApp):
    # Testing function when database has no signups
    def test_hr_view_signup_0(self):
        # calling hr_view_signup function via flask route
        response = self.client.get("/hr_view_signup")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : 'There are no enrollment retrieved'
        })


    # Testing function when database has 1 signups
    def test_hr_view_signup_1(self):
        t1 = self.er1.start

        # adding dummy signups to database
        self.er1.start = datetime.fromisoformat(self.er1.start)
        db.session.add(self.er1)
        db.session.commit()
        
        # calling hr_view_signup function via flask route
        response = self.client.get("/hr_view_signup")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' :
                [
                {
                'EID': self.er1.EID,
                'SID': self.er1.SID,
                'CID': self.er1.CID,
                'start': t1
                }
                ]
                ,
            'message' : 'All enrollments are retrieved'
            })


    # Testing function when database has 2 signups
    def test_hr_view_signup_2(self):
        t1 = self.er1.start

        # adding dummy signups to database
        self.er1.start = datetime.fromisoformat(self.er1.start)
        db.session.add(self.er1)
        self.er2.start = datetime.fromisoformat(self.er2.start)
        db.session.add(self.er2)
        db.session.commit()
        
        # calling hr_view_signup function via flask route
        response = self.client.get("/hr_view_signup")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' :
                [
                {
                'EID': self.er1.EID,
                'SID': self.er1.SID,
                'CID': self.er1.CID,
                'start': t1
                },
                {
                'EID': self.er2.EID,
                'SID': self.er2.SID,
                'CID': self.er2.CID,
                'start': t1
                },
                ]
                ,
            'message' : 'All enrollments are retrieved'
            })


class TestHRAssignEngineer(TestApp):
    # Testing positive case where all details are present in request body
    def test_hr_assign_engineer_all_details(self):
        # creating request body for assignment details
        request_body = {
            'EID': self.cd1.EID,
            'SID': self.cd1.SID,
            'CID': self.cd1.CID,
            'start': self.cd1.start
        }

        # calling hr_assign_engineer function via flask route
        response = self.client.post("/hr_assign_engineer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' :
                {
                'EID': self.cd1.EID,
                'SID': self.cd1.SID,
                'CID': self.cd1.CID,
                'start': self.cd1.start,
                'status': 'ongoing',
                },
            'message' : f'{self.cd1.EID} has been inserted successfully into the course details'
            })


    # Testing negative case where EID missing in request body
    def test_hr_assign_engineer_missing_eid(self):
        # creating request body for assignment details
        request_body = {
            'SID': self.cd1.SID,
            'CID': self.cd1.CID,
            'start': self.cd1.start
        }

        # calling hr_assign_engineer function via flask route
        response = self.client.post("/hr_assign_engineer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"academic record ['EID'] is not present,  engineer is not assigned"
            })


class TestHRWithdrawEngineer(TestApp):
    # Testing positive case where course detail is in database
    def test_hr_withdraw_engineer_in_database(self):
        t1 = self.cd2.start
        # adding dummy course detail into database
        self.cd2.start = datetime.fromisoformat(self.cd2.start)
        db.session.add(self.cd2)
        db.session.commit()

        # creating request body for withdraw details
        request_body = {
            'EID': self.cd2.EID,
            'SID': self.cd2.SID,
            'CID': self.cd2.CID,
            'start': t1,
        }

        # calling hr_withdraw_engineer function via flask route
        response = self.client.post("/hr_withdraw_engineer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : f'{self.cd2.EID} has been deleted successfully from course details'
            })
    

    # Testing negative case where course detail is not in database
    def test_hr_withdraw_engineer_not_in_database(self):
        # creating request body for withdraw details
        request_body = {
            'EID': self.cd2.EID,
            'SID': self.cd2.SID,
            'CID': self.cd2.CID,
            'start': self.cd2.start
        }

        # calling hr_withdraw_engineer function via flask route
        response = self.client.post("/hr_withdraw_engineer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f'academic_record {self.cd2.EID} is not present in database, engineer is not withdrawn'
            })


    # Testing negative case where EID missing
    def test_hr_withdraw_engineer_missing_eid(self):
        # creating request body for withdraw details
        request_body = {
            'SID': self.cd2.SID,
            'CID': self.cd2.CID,
            'start': self.cd2.start
        }

        # calling hr_withdraw_engineer function via flask route
        response = self.client.post("/hr_withdraw_engineer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"academic_record ['EID'] is not present, engineer is not withdrawn"
            })


    # Testing negative case where CID missing
    def test_hr_withdraw_engineer_missing_cid(self):
        # creating request body for withdraw details
        request_body = {
            'EID': self.cd2.EID,
            'SID': self.cd2.SID,
            'start': self.cd2.start
        }

        # calling hr_withdraw_engineer function via flask route
        response = self.client.post("/hr_withdraw_engineer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"academic_record ['CID'] is not present, engineer is not withdrawn"
            })


class TestHRApproveSignup(TestApp):
    # Testing positive case where enrollment detail is in database
    def test_hr_approve_signup_in_database(self):
        t1 = self.er1.start

        # adding dummy enrollment into database
        self.er1.start = datetime.fromisoformat(self.er1.start)
        db.session.add(self.er1)
        db.session.commit()

        # creating request body for course details
        request_body = {
            'EID': self.er1.EID,
            'SID': self.er1.SID,
            'CID': self.er1.CID,
            'start': t1,
        }

        # calling hr_approve_signup function via flask route
        response = self.client.post("/hr_approve_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : 
                {
                'EID': self.er1.EID,
                'SID': self.er1.SID,
                'CID': self.er1.CID,
                'start': t1,
                'status': 'ongoing',
                },
            'message' : f'{self.er1.EID} prerequisites has been moved successfully from Enrollment to academic_record'
            })
    

    # Testing negative case where enrollment detail is not in database
    def test_hr_approve_signup_not_in_database(self):
        # creating request body for course details
        request_body = {
            'EID': self.er1.EID,
            'SID': self.er1.SID,
            'CID': self.er1.CID,
            'start': self.er1.start
        }

        # calling hr_approve_signup function via flask route
        response = self.client.post("/hr_approve_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f'Academic record {self.cd1.EID} is not present, engineer is not enrolled'
            })


    # Testing negative case where EID is missing 
    def test_hr_approve_signup_missing_eid(self):
        t1 = self.er1.start
        # adding dummy enrollment into database
        self.er1.start = datetime.fromisoformat(self.er1.start)
        db.session.add(self.er1)
        db.session.commit

        # creating request body for course details
        request_body = {
            'SID': self.er1.SID,
            'CID': self.er1.CID,
            'start': t1
        }

        # calling hr_approve_signup function via flask route
        response = self.client.post("/hr_approve_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Academic record ['EID'] is not present, engineer is not enrolled"
            })


    
class TestHRRejectSignup(TestApp):
    # Testing positive case where enrollment detail is in database
    def test_hr_reject_signup_in_database(self):
        t1 = self.er2.start
        # adding dummy enrollment into database
        self.er2.start = datetime.fromisoformat(self.er2.start)
        db.session.add(self.er2)
        db.session.commit()

        # creating request body for course details
        request_body = {
            'EID': self.er2.EID,
            'SID': self.er2.SID,
            'CID': self.er2.CID,
            'start': t1
        }

        # calling hr_reject_signup function via flask route
        response = self.client.post("/hr_reject_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {

            'message' : f'{self.er2.EID} has been deleted successfully from Enrollment'
            
            })


    # Testing negative case where enrollment detail is not in database
    def test_hr_reject_signup_not_in_database(self):

        #creating request body for course details
        request_body = {
            'EID': self.er2.EID,
            'SID': self.er2.SID,
            'CID': self.er2.CID,
            'start': self.er2.start
        }

        # calling hr_reject_signup function via flask route
        response = self.client.post("/hr_reject_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {

            'message' : f'Enrollment {self.er2.EID} is not present in database,  engineer is not rejected'
            
            })


    # Testing negative case where EID is missing
    def test_hr_reject_signup_missing_eid(self):
        t1 = self.er2.start
        # adding dummy enrollment into database
        self.er2.start = datetime.fromisoformat(self.er2.start)
        db.session.add(self.er2)
        db.session.commit()

        # creating request body for course details
        request_body = {
            'SID': self.er2.SID,
            'CID': self.er2.CID,
            'start': t1
        }

        # calling hr_reject_signup function via flask route
        response = self.client.post("/hr_reject_signup",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {

            'message' : f"Academic record ['EID'] is not present, signup is not rejected"
            
            })


class TestHRAssignTrainer(TestApp):
    def test_hr_assign_trainer(self):
        t1 = self.s1.start
        # adding dummy course into database
        self.s1.start = datetime.fromisoformat(self.s1.start)
        self.s1.end = datetime.fromisoformat(self.s1.end)
        db.session.add(self.s1)
        db.session.commit()

        # creating request body for course 
        request_body = {
            'CID' : self.s1.CID, 
            'SID' : self.s1.SID, 
            'start' : t1, 
            'TID' : self.s1.TID
        }

        # calling hr_assign_trainer function via flask route
        response = self.client.post("/hr_assign_trainer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : 
                {
                'CID' : self.s1.CID, 
                'SID' : self.s1.SID, 
                'TID' : self.s1.TID,
                'end': '2021-05-01 09:15:00',
                'start': '2021-04-01 09:15:00',
                'vacancy': 50
                },
            "message": f"TID {self.s1.TID} has been assigned to section"
            })

    def test_hr_assign_trainer_no_overwrite(self):
        t1 = self.s2.start
        # adding dummy course into database
        self.s2.start = datetime.fromisoformat(self.s2.start)
        self.s2.end = datetime.fromisoformat(self.s2.end)
        db.session.add(self.s2)
        db.session.commit()

        # creating request body for course 
        request_body = {
            'CID' : self.s2.CID, 
            'SID' : self.s2.SID, 
            'start' : t1, 
            'TID' : self.s2.TID
        }

        # calling hr_assign_trainer function via flask route
        response = self.client.post("/hr_assign_trainer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : 
                {
                'CID' : self.s2.CID, 
                'SID' : self.s2.SID, 
                'TID' : self.s2.TID,
                'end': '2021-05-01 09:15:00',
                'start': '2021-04-01 09:15:00',
                'vacancy': 50
                },
            "message": f"TID {self.s2.TID} has been assigned to section"
            
            })

    def test_hr_assign_trainer_no_tid(self):
        t1 = self.s2.start
        # adding dummy course into database
        self.s2.start = datetime.fromisoformat(self.s2.start)
        self.s2.end = datetime.fromisoformat(self.s2.end)
        db.session.add(self.s2)
        db.session.commit()

        # creating request body for course 
        request_body = {
            'CID' : self.s2.CID, 
            'SID' : self.s2.SID, 
            'start' : t1, 
        }

        # calling hr_assign_trainer function via flask route
        response = self.client.post("/hr_assign_trainer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Section ['TID'] is not present, trainer is not assigned"
            
            })

    def test_hr_assign_trainer_nothing(self):
        t1 = self.s2.start
        # adding dummy course into database
        self.s2.start = datetime.fromisoformat(self.s2.start)
        self.s2.end = datetime.fromisoformat(self.s2.end)
        db.session.add(self.s2)
        db.session.commit()

        # creating request body for course 
        request_body = {
        }

        # calling hr_assign_trainer function via flask route
        response = self.client.post("/hr_assign_trainer",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Section ['CID', 'SID', 'TID', 'start'] is not present, trainer is not assigned"
            
            })

class TestEngineerWithdraw(TestApp):
    # Testing positive case where enrollment detail is in database
    def test_engineer_withdraw(self):
        t1 = self.er2.start
        # adding dummy enrollment into database
        self.er2.start = datetime.fromisoformat(self.er2.start)
        db.session.add(self.er2)
        db.session.commit()

        # creating request body for course details
        request_body = {
            'EID': self.er2.EID,
            'SID': self.er2.SID,
            'CID': self.er2.CID,
            'start': t1
        }

        # calling hr_reject_signup function via flask route
        response = self.client.post("/engineer_withdraw",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {

            'message' : f'{self.er2.EID} has been deleted successfully from Enrollment'
            
            })


    # Testing negative case where enrollment detail is not in database
    def test_engineer_withdraw_not_in_database(self):

        #creating request body for course details
        request_body = {
            'EID': self.er2.EID,
            'SID': self.er2.SID,
            'CID': self.er2.CID,
            'start': self.er2.start
        }

        # calling hr_reject_signup function via flask route
        response = self.client.post("/engineer_withdraw",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {

            'message' : f'Enrollment {self.er2.EID} is not present in database, engineer is not withdraw'
            
            })


    # Testing negative case where EID is missing
    def test_engineer_withdraw_missing_eid(self):
        t1 = self.er2.start
        # adding dummy enrollment into database
        self.er2.start = datetime.fromisoformat(self.er2.start)
        db.session.add(self.er2)
        db.session.commit()

        # creating request body for course details
        request_body = {
            'SID': self.er2.SID,
            'CID': self.er2.CID,
            'start': t1
        }

        # calling hr_reject_signup function via flask route
        response = self.client.post("/engineer_withdraw",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {

            'message' : f"Academic record ['EID'] is not present, signup is not withdraw"
            
            })


class TestViewEnrollmentByEID(TestApp):
    # Testing function when database has no signups
    def test_view_enrollment_no_EID(self):
        # calling hr_view_signup function via flask route

        request_body = {
        }
        response = self.client.post("/view_enrollment_by_EID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : 'EID is missing'
        })


    # Testing function when database has 1 signups
    def test_view_enrollment_by_EID(self):
        t1 = self.er1.start

        # adding dummy signups to database
        self.er1.start = datetime.fromisoformat(self.er1.start)
        db.session.add(self.er1)
        db.session.add(self.c1)
        db.session.commit()

        request_body = {
            'EID': self.er1.EID
            }
        
        # calling hr_view_signup function via flask route
        response = self.client.post("/view_enrollment_by_EID",
                            data=json.dumps(request_body),
                            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' :
                [
                {
                'EID': self.er1.EID,
                'SID': self.er1.SID,
                'CID': self.er1.CID,
                'start': t1,
                'course_name': self.c1.name
                }
                ]
                ,
            'message' : 'All enrolled sections are retrieved'
            })


    # Testing function when database has 2 signups
    def test_view_enrollment_by_EID_no_enrollment(self):
        t1 = self.er1.start

        # adding dummy signups to database

        request_body = {
            'EID': self.er1.EID
            }
        
        # calling hr_view_signup function via flask route
        response = self.client.post("/view_enrollment_by_EID",
                            data=json.dumps(request_body),
                            content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : 'There are no section enrolled'
            })

### Registration TEST CASES ###

if __name__ == '__main__':
    #For jenkins
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    #For local tests
    # unittest.main()
