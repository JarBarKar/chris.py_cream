import unittest
import flask_testing
import json
from app import app, db, Ungraded_quiz


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app


    def setUp(self):
        self.ugq1q1 = Ungraded_quiz(CID='IS500', LID=1, SID='G2', question='Is the moon round?', 
                                    answer='YES', options='YES|NO')
        self.ugq1q2 = Ungraded_quiz(CID='IS500', LID=1, SID='G2', question='Is the sun round?',
                                    answer='YES', options='YES|NO')
        self.ugq1q3 = Ungraded_quiz(CID='IS500', LID=1, SID='G2', question='Which of these is not a planet?',
                                    answer='Pluto', options='EARTH|MARS|JUPITER|PLUTO|VENUS')
        
        self.ugq2q1 = Ungraded_quiz(CID='IS500', LID=2, SID='G2', question='Is Computational Thinking a hard module?', 
                                    answer='YES', options='YES|NO')
        self.ugq2q2 = Ungraded_quiz(CID='IS500', LID=2, SID='G2', question='Is Intro to Machine Learning hard?',
                                    answer='YES', options='YES|NO')
        self.ugq2q3 = Ungraded_quiz(CID='IS500', LID=2, SID='G2', question='What course is this code for?',
                                    answer='SPM', options='SPM|PMS|MPS|SMP|PSM')
        self.maxDiff = None
        db.create_all()


    def tearDown(self):
        self.ugq1q1 = None
        self.ugq1q2 = None
        self.ugq1q3 = None
        self.ugq2q1 = None
        self.ugq2q2 = None
        self.ugq2q3 = None

        db.session.remove()
        db.drop_all()

### UNGRADED QUIZ TEST CASES ###
class TestCreateUngradedQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body
    def test_create_ungraded_quiz_question_all_details(self):
        # Preparing request body
        request_body = {
            'CID': self.ugq1q1.CID,
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'question': self.ugq1q1.question,
            'answer': self.ugq1q1.answer,
            'options': self.ugq1q1.options
        }
        # calling create_ungraded_quiz_question function via flask route
        response = self.client.post("/create_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'CID': self.ugq1q1.CID,
                'LID': self.ugq1q1.LID,
                'SID': self.ugq1q1.SID,
                'question': self.ugq1q1.question,
                'answer': self.ugq1q1.answer,
                'options': self.ugq1q1.options
            },
            'message' : f'Ungraded quiz question, {self.ugq1q1.question} ,has been inserted successfully into the database'
        })


    # Testing negative case where cid missing in request body
    def test_create_ungraded_quiz_question_missing_cid(self):
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'question': self.ugq1q1.question,
            'answer': self.ugq1q1.answer,
            'options': self.ugq1q1.options
        }
        # calling create_ungraded_quiz_question function via flask route
        response = self.client.post("/create_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, ungraded quiz question creation failed"
        })
    

    # Testing negative case where question missing in request body
    def test_create_ungraded_quiz_question_missing_question(self):
        # Preparing request body
        request_body = {
            'CID': self.ugq1q1.CID,
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'answer': self.ugq1q1.answer,
            'options': self.ugq1q1.options
        }
        # calling create_ungraded_quiz_question function via flask route
        response = self.client.post("/create_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"question is missing from request body, ungraded quiz question creation failed"
        })


class TestReadUngradedQuiz(TestApp):
    # Testing positive case where all details are present in request body
    def test_read_ungraded_quiz_all_details(self):
        
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
        db.session.commit()
        # Preparing request body
        request_body = {
            'CID': self.ugq1q1.CID,
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
        }
        # calling read_ungraded_quiz function via flask route
        response = self.client.post("/read_ungraded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : [
                {
                'CID': self.ugq1q1.CID,
                'LID': self.ugq1q1.LID,
                'SID': self.ugq1q1.SID,
                'question': self.ugq1q1.question,
                'answer': self.ugq1q1.answer,
                'options': self.ugq1q1.options
                },
                {
                'CID': self.ugq1q2.CID,
                'LID': self.ugq1q2.LID,
                'SID': self.ugq1q2.SID,
                'question': self.ugq1q2.question,
                'answer': self.ugq1q2.answer,
                'options': self.ugq1q2.options
                },
                {
                'CID': self.ugq1q3.CID,
                'LID': self.ugq1q3.LID,
                'SID': self.ugq1q3.SID,
                'question': self.ugq1q3.question,
                'answer': self.ugq1q3.answer,
                'options': self.ugq1q3.options
                }
            ],
            'message' : f"Quiz with CID {self.ugq1q1.CID}, LID {self.ugq1q1.LID}, SID {self.ugq1q1.SID} has been retrieved"
        })


    # Testing negative case where cid missing in request body
    def test_read_ungraded_quiz_missing_cid(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
        }
        # calling read_ungraded_quiz function via flask route
        response = self.client.post("/read_ungraded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, ungraded quiz read failed"
        })
    

    # Testing negative case where sid missing in request body
    def test_read_ungraded_quiz_missing_sid(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
        # Preparing request body
        request_body = {
            'CID': self.ugq1q1.CID,
            'LID': self.ugq1q1.LID,
        }
        # calling read_ungraded_quiz function via flask route
        response = self.client.post("/read_ungraded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"SID is missing from request body, ungraded quiz read failed"
        })
    

    # Testing negative case where quiz is not in database
    def test_read_ungraded_quiz_no_quiz(self):
        # Preparing request body
        request_body = {
            'CID': self.ugq1q1.CID,
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
        }
        # calling read_ungraded_quiz function via flask route
        response = self.client.post("/read_ungraded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz with CID {self.ugq1q1.CID} LID {self.ugq1q1.LID} SID {self.ugq1q1.SID} does not exist in database"
        })


class TestReadUngradedQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body
    def test_read_ungraded_quiz_question_all_details(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'CID': self.ugq1q1.CID,
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'question': self.ugq1q1.question,
        }
        # calling read_ungraded_quiz_question function via flask route
        response = self.client.post("/read_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : 
                {
                'CID': self.ugq1q1.CID,
                'LID': self.ugq1q1.LID,
                'SID': self.ugq1q1.SID,
                'question': self.ugq1q1.question,
                'answer': self.ugq1q1.answer,
                'options': self.ugq1q1.options
                },
            'message' : f"Quiz question \'{self.ugq1q1.question}\' with CID {self.ugq1q1.CID}, LID {self.ugq1q1.LID}, SID {self.ugq1q1.SID} has been retrieved"
        })


    # Testing negative case where cid missing in request body
    def test_read_ungraded_quiz_question_missing_cid(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'question': self.ugq1q1.question,
        }
        # calling read_ungraded_quiz_question function via flask route
        response = self.client.post("/read_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, ungraded quiz question read failed"
        })
    

    # Testing negative case where question missing in request body
    def test_read_ungraded_quiz_question_missing_sid(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'CID': self.ugq1q1.CID,
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
        }
        # calling read_ungraded_quiz_question function via flask route
        response = self.client.post("/read_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"question is missing from request body, ungraded quiz question read failed"
        })
    

    # Testing negative case where quiz is not in database
    def test_read_ungraded_quiz_question_no_quiz(self):
        # Preparing request body
        request_body = {
            'CID': self.ugq1q1.CID,
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'question': self.ugq1q1.question,
        }
        # calling read_ungraded_quiz function via flask route
        response = self.client.post("/read_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.ugq1q1.question}\' with CID {self.ugq1q1.CID} LID {self.ugq1q1.LID} SID {self.ugq1q1.SID} does not exist in database"
        })


class TestUpdateUngradedQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body, changing answer to NO
    def test_update_ungraded_quiz_question_all_details_change_answer(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
        
        # Preparing request body
        request_body = {
            'CID': self.ugq2q2.CID,
            'LID': self.ugq2q2.LID,
            'SID': self.ugq2q2.SID,
            'question' : self.ugq2q2.question,
            'answer' : 'NO'
        }
        # calling update_ungraded_quiz_question function via flask route
        response = self.client.post("/update_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'CID': self.ugq2q2.CID,
                'LID': self.ugq2q2.LID,
                'SID': self.ugq2q2.SID,
                'question' : self.ugq2q2.question,
                'answer' : 'NO',
                'options' : self.ugq2q2.options
            },
            'message' : f"Quiz question \'{self.ugq2q2.question}\' has been updated"
            
        })

    # Testing positive case where all details are present in request body, changing options to YES|NO|MAYBE
    def test_update_ungraded_quiz_question_all_details_change_options(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
        
        # Preparing request body
        request_body = {
            'CID': self.ugq2q2.CID,
            'LID': self.ugq2q2.LID,
            'SID': self.ugq2q2.SID,
            'question' : self.ugq2q2.question,
            'options' : 'YES|NO|MAYBE'
        }
        # calling update_ungraded_quiz_question function via flask route
        response = self.client.post("/update_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'CID': self.ugq2q2.CID,
                'LID': self.ugq2q2.LID,
                'SID': self.ugq2q2.SID,
                'question' : self.ugq2q2.question,
                'answer' : self.ugq2q2.answer,
                'options' : 'YES|NO|MAYBE'
            },
            'message' : f"Quiz question \'{self.ugq2q2.question}\' has been updated"
            
        })
    

    # Testing negative case where cid missing in request body
    def test_update_ungraded_quiz_question_missing_cid(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
        
        # Preparing request body
        request_body = {
            'LID': self.ugq2q2.LID,
            'SID': self.ugq2q2.SID,
            'question' : self.ugq2q2.question,
            'options' : 'YES|NO|MAYBE'
        }
        # calling update_ungraded_quiz_question function via flask route
        response = self.client.post("/update_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, ungraded quiz update failed"
        })
    

    # Testing negative case where lid missing in request body
    def test_update_ungraded_quiz_question_missing_lid(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
        
        # Preparing request body
        request_body = {
            'CID': self.ugq2q2.CID,
            'SID': self.ugq2q2.SID,
            'question' : self.ugq2q2.question,
            'options' : 'YES|NO|MAYBE'
        }
        # calling update_ungraded_quiz_question function via flask route
        response = self.client.post("/update_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"LID is missing from request body, ungraded quiz update failed"
        })


class TestDeleteUngradedQuiz(TestApp):
    # Testing positive case where all details are present in request body
    def test_delete_ungraded_quiz_all_details(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
    
        # Preparing request body
        request_body = {
            'CID': self.ugq2q1.CID,
            'LID': self.ugq2q1.LID,
            'SID': self.ugq2q1.SID,
        }
        # calling delete_ungraded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_ungraded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : f"Quiz with the CID {self.ugq2q1.CID} LID {self.ugq2q1.LID} SID {self.ugq2q1.SID} has been deleted successfully"
        })
        # calling read_ungraded_quiz function via flask route, making sure quiz no longer exists in database
        response = self.client.post("/read_ungraded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            'message' : f"Quiz with CID {self.ugq2q1.CID} LID {self.ugq2q1.LID} SID {self.ugq2q1.SID} does not exist in database"
        })
        # calling read_ungraded_quiz function via flask route, making sure other quizzes have not been affected
        request_body = {
            'CID': self.ugq1q1.CID,
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
        }
        response = self.client.post("/read_ungraded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            'data' : [
                {
                'CID': self.ugq1q1.CID,
                'LID': self.ugq1q1.LID,
                'SID': self.ugq1q1.SID,
                'question': self.ugq1q1.question,
                'answer': self.ugq1q1.answer,
                'options': self.ugq1q1.options
                },
                {
                'CID': self.ugq1q2.CID,
                'LID': self.ugq1q2.LID,
                'SID': self.ugq1q2.SID,
                'question': self.ugq1q2.question,
                'answer': self.ugq1q2.answer,
                'options': self.ugq1q2.options
                },
                {
                'CID': self.ugq1q3.CID,
                'LID': self.ugq1q3.LID,
                'SID': self.ugq1q3.SID,
                'question': self.ugq1q3.question,
                'answer': self.ugq1q3.answer,
                'options': self.ugq1q3.options
                }
            ],
            'message' : f"Quiz with CID {self.ugq1q1.CID}, LID {self.ugq1q1.LID}, SID {self.ugq1q1.SID} has been retrieved"
        })
    

    # Testing negative case where quiz is not in database
    def test_delete_ungraded_quiz_no_quiz(self):
        # Preparing request body
        request_body = {
            'CID': self.ugq2q1.CID,
            'LID': self.ugq2q1.LID,
            'SID': self.ugq2q1.SID,
        }
        # calling delete_ungraded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_ungraded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz with the CID {self.ugq2q1.CID} LID {self.ugq2q1.LID} SID {self.ugq2q1.SID} does not exist in the database"
        })
    

    # Testing negative case where cid is missing in request body
    def test_delete_ungraded_quiz_missing_cid(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
        # Preparing request body
        request_body = {
            'LID': self.ugq2q1.LID,
            'SID': self.ugq2q1.SID,
        }
        # calling delete_ungraded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_ungraded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, ungraded quiz deletion failed"
        })
    

    # Testing negative case where lid is missing in request body
    def test_delete_ungraded_quiz_missing_lid(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
        # Preparing request body
        request_body = {
            'CID': self.ugq2q1.CID,
            'SID': self.ugq2q1.SID,
        }
        # calling delete_ungraded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_ungraded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"LID is missing from request body, ungraded quiz deletion failed"
        })


class TestDeleteUngradedQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body
    def test_delete_ungraded_quiz_question_all_details(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
    
        # Preparing request body
        request_body = {
            'CID': self.ugq2q2.CID,
            'LID': self.ugq2q2.LID,
            'SID': self.ugq2q2.SID,
            'question' : self.ugq2q2.question
        }
        # calling delete_ungraded_quiz_question function via flask route, checking if deletion went through
        response = self.client.post("/delete_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.ugq2q2.question}\' with the CID {self.ugq2q1.CID} LID {self.ugq2q1.LID} SID {self.ugq2q1.SID} has been deleted successfully"
        })
        # calling read_ungraded_quiz_question function via flask route, making sure quiz question have been deleted from database
        response = self.client.post("/read_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.ugq2q2.question}\' with CID {self.ugq2q2.CID} LID {self.ugq2q2.LID} SID {self.ugq2q2.SID} does not exist in database",
        })
        # calling read_ungraded_quiz function via flask route, making sure other quiz questions have not been affected
        request_body = {
            'CID': self.ugq2q2.CID,
            'LID': self.ugq2q2.LID,
            'SID': self.ugq2q2.SID,
        }
        response = self.client.post("/read_ungraded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            'data' : [
                {
                'CID': self.ugq2q1.CID,
                'LID': self.ugq2q1.LID,
                'SID': self.ugq2q1.SID,
                'question': self.ugq2q1.question,
                'answer': self.ugq2q1.answer,
                'options': self.ugq2q1.options
                },
                {
                'CID': self.ugq2q3.CID,
                'LID': self.ugq2q3.LID,
                'SID': self.ugq2q3.SID,
                'question': self.ugq2q3.question,
                'answer': self.ugq2q3.answer,
                'options': self.ugq2q3.options
                }
            ],
            'message' : f"Quiz with CID {self.ugq2q2.CID}, LID {self.ugq2q2.LID}, SID {self.ugq2q2.SID} has been retrieved"
        })
    

    # Testing negative case where quiz question is not in database
    def test_delete_ungraded_quiz_question_no_quiz(self):
        # Preparing request body
        request_body = {
            'CID': self.ugq2q1.CID,
            'LID': self.ugq2q1.LID,
            'SID': self.ugq2q1.SID,
            'question': self.ugq2q1.question,
        }
        # calling delete_ungraded_quiz_question function via flask route, checking if deletion went through
        response = self.client.post("/delete_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.ugq2q1.question}\' with the CID {self.ugq2q1.CID} LID {self.ugq2q1.LID} SID {self.ugq2q1.SID} does not exist in the database"
        })
    

    # Testing negative case where cid is missing in request body
    def test_delete_ungraded_quiz_question_missing_cid(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
        # Preparing request body
        request_body = {
            'LID': self.ugq2q1.LID,
            'SID': self.ugq2q1.SID,
            'question': self.ugq2q1.question,
        }
        # calling delete_ungraded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, ungraded quiz question deletion failed"
        })
    

    # Testing negative case where lid is missing in request body
    def test_delete_ungraded_quiz_question_missing_lid(self):
        #add dummy ungraded quizzes into database
        db.session.add(self.ugq1q1)
        db.session.add(self.ugq1q2)
        db.session.add(self.ugq1q3)
        db.session.add(self.ugq2q1)
        db.session.add(self.ugq2q2)
        db.session.add(self.ugq2q3)
        # Preparing request body
        request_body = {
            'CID': self.ugq2q1.CID,
            'LID': self.ugq2q1.LID,
            'SID': self.ugq2q1.SID,
        }
        # calling delete_ungraded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_ungraded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"question is missing from request body, ungraded quiz question deletion failed"
        })
    
### UNGRADED QUIZ TEST CASES ###

if __name__ == '__main__':
    unittest.main()
