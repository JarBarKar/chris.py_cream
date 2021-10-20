import unittest
import flask_testing
import json
from app import app, db, Graded_quiz


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app


    def setUp(self):
        self.gq1q1 = Graded_quiz(CID='IS500', LID=1, SID='G2', question='Is Aaron a boy?', 
                                    answer='YES', options='YES|NO', duration=2)
        self.gq1q2 = Graded_quiz(CID='IS500', LID=1, SID='G2', question='Is Alvan a girl?',
                                    answer='NO', options='YES|NO', duration=2)
        self.gq1q3 = Graded_quiz(CID='IS500', LID=1, SID='G2', question='Which of these is the best prof?',
                                    answer='Chris', options='CHRIS|JAMES|PETER|JACK|OLLIE', duration=2)
        self.gq2q1 = Graded_quiz(CID='IS500', LID=2, SID='G2', question='Is Ivan a boy?', 
                                    answer='YES', options='YES|NO', duration=2)
        self.gq2q2 = Graded_quiz(CID='IS500', LID=2, SID='G2', question='Is Jiancheng a girl?',
                                    answer='NO', options='YES|NO', duration=2)
        self.gq2q3 = Graded_quiz(CID='IS500', LID=2, SID='G2', question='Who is best girl in FF7?',
                                    answer='SEPHI', options='TIFA|YUFFIE|AERITH|CLOUD|SEPHI', duration=2)
        self.maxDiff = None
        db.create_all()

    def tearDown(self):
        self.gq1q1 = None
        self.gq1q2 = None
        self.gq1q3 = None
        self.gq2q1 = None
        self.gq2q2 = None
        self.gq2q3 = None

        db.session.remove()
        db.drop_all()

### GRADED QUIZ TEST CASES ###
class TestCreateGradedQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body
    def test_create_graded_quiz_question_all_details(self):
        # Preparing request body
        request_body = {
            'CID': self.gq1q1.CID,
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'question': self.gq1q1.question,
            'answer': self.gq1q1.answer,
            'options': self.gq1q1.options,
            'duration': self.gq1q1.duration
        }
        # calling create_graded_quiz_question function via flask route
        response = self.client.post("/create_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'CID': self.gq1q1.CID,
                'LID': self.gq1q1.LID,
                'SID': self.gq1q1.SID,
                'question': self.gq1q1.question,
                'answer': self.gq1q1.answer,
                'options': self.gq1q1.options,
                'duration': self.gq1q1.duration
            },
            'message' : f'Graded quiz question, {self.gq1q1.question} ,has been inserted successfully into the database'
        })


    # Testing negative case where cid missing in request body
    def test_create_graded_quiz_question_missing_cid(self):
        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'question': self.gq1q1.question,
            'answer': self.gq1q1.answer,
            'options': self.gq1q1.options,
            'duration': self.gq1q1.duration
        }
        # calling create_graded_quiz_question function via flask route
        response = self.client.post("/create_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, graded quiz question creation failed"
        })
    

    # Testing negative case where question missing in request body
    def test_create_graded_quiz_question_missing_question(self):
        # Preparing request body
        request_body = {
            'CID': self.gq1q1.CID,
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'answer': self.gq1q1.answer,
            'options': self.gq1q1.options,
            'duration': self.gq1q1.duration
        }
        # calling create_graded_quiz_question function via flask route
        response = self.client.post("/create_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"question is missing from request body, graded quiz question creation failed"
        })


class TestReadGradedQuiz(TestApp):
    # Testing positive case where all details are present in request body
    def test_read_graded_quiz_all_details(self):
        
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
        db.session.commit()
        # Preparing request body
        request_body = {
            'CID': self.gq1q1.CID,
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
        }
        # calling read_graded_quiz function via flask route
        response = self.client.post("/read_graded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : [
                {
                'CID': self.gq1q1.CID,
                'LID': self.gq1q1.LID,
                'SID': self.gq1q1.SID,
                'question': self.gq1q1.question,
                'answer': self.gq1q1.answer,
                'options': self.gq1q1.options,
                'duration': self.gq1q1.duration
                },
                {
                'CID': self.gq1q2.CID,
                'LID': self.gq1q2.LID,
                'SID': self.gq1q2.SID,
                'question': self.gq1q2.question,
                'answer': self.gq1q2.answer,
                'options': self.gq1q2.options,
                'duration': self.gq1q2.duration
                },
                {
                'CID': self.gq1q3.CID,
                'LID': self.gq1q3.LID,
                'SID': self.gq1q3.SID,
                'question': self.gq1q3.question,
                'answer': self.gq1q3.answer,
                'options': self.gq1q3.options,
                'duration': self.gq1q3.duration
                }
            ],
            'message' : f"Quiz with CID {self.gq1q1.CID}, LID {self.gq1q1.LID}, SID {self.gq1q1.SID} has been retrieved"
        })


    # Testing negative case where cid missing in request body
    def test_read_graded_quiz_missing_cid(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
        }
        # calling read_graded_quiz function via flask route
        response = self.client.post("/read_graded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, graded quiz read failed"
        })
    

    # Testing negative case where sid missing in request body
    def test_read_graded_quiz_missing_sid(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
        # Preparing request body
        request_body = {
            'CID': self.gq1q1.CID,
            'LID': self.gq1q1.LID,
        }
        # calling read_graded_quiz function via flask route
        response = self.client.post("/read_graded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"SID is missing from request body, graded quiz read failed"
        })
    

    # Testing negative case where quiz is not in database
    def test_read_graded_quiz_no_quiz(self):
        # Preparing request body
        request_body = {
            'CID': self.gq1q1.CID,
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
        }
        # calling read_graded_quiz function via flask route
        response = self.client.post("/read_graded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz with CID {self.gq1q1.CID} LID {self.gq1q1.LID} SID {self.gq1q1.SID} does not exist in database"
        })


class TestReadGradedQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body
    def test_read_graded_quiz_question_all_details(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'CID': self.gq1q1.CID,
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'question': self.gq1q1.question,
        }
        # calling read_graded_quiz_question function via flask route
        response = self.client.post("/read_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : 
                {
                'CID': self.gq1q1.CID,
                'LID': self.gq1q1.LID,
                'SID': self.gq1q1.SID,
                'question': self.gq1q1.question,
                'answer': self.gq1q1.answer,
                'options': self.gq1q1.options,
                'duration': self.gq1q1.duration
                },
            'message' : f"Quiz question \'{self.gq1q1.question}\' with CID {self.gq1q1.CID}, LID {self.gq1q1.LID}, SID {self.gq1q1.SID} has been retrieved"
        })


    # Testing negative case where cid missing in request body
    def test_read_graded_quiz_question_missing_cid(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'question': self.gq1q1.question,
        }
        # calling read_graded_quiz_question function via flask route
        response = self.client.post("/read_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, graded quiz question read failed"
        })
    

    # Testing negative case where question missing in request body
    def test_read_graded_quiz_question_missing_sid(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'CID': self.gq1q1.CID,
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
        }
        # calling read_graded_quiz_question function via flask route
        response = self.client.post("/read_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"question is missing from request body, graded quiz question read failed"
        })
    

    # Testing negative case where quiz is not in database
    def test_read_graded_quiz_question_no_quiz(self):
        # Preparing request body
        request_body = {
            'CID': self.gq1q1.CID,
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'question': self.gq1q1.question,
        }
        # calling read_graded_quiz function via flask route
        response = self.client.post("/read_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.gq1q1.question}\' with CID {self.gq1q1.CID} LID {self.gq1q1.LID} SID {self.gq1q1.SID} does not exist in database"
        })


class TestUpdateGradedQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body, changing answer to NO
    def test_update_graded_quiz_question_all_details_change_answer(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
        
        # Preparing request body
        request_body = {
            'CID': self.gq2q2.CID,
            'LID': self.gq2q2.LID,
            'SID': self.gq2q2.SID,
            'question' : self.gq2q2.question,
            'answer' : 'NO'
        }
        # calling update_graded_quiz_question function via flask route
        response = self.client.post("/update_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'CID': self.gq2q2.CID,
                'LID': self.gq2q2.LID,
                'SID': self.gq2q2.SID,
                'question' : self.gq2q2.question,
                'answer' : 'NO',
                'options' : self.gq2q2.options,
                'duration': self.gq2q2.duration
            },
            'message' : f"Quiz question \'{self.gq2q2.question}\' has been updated"
            
        })

    # Testing positive case where all details are present in request body, changing options to YES|NO|MAYBE
    def test_update_graded_quiz_question_all_details_change_options(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
        
        # Preparing request body
        request_body = {
            'CID': self.gq2q2.CID,
            'LID': self.gq2q2.LID,
            'SID': self.gq2q2.SID,
            'question' : self.gq2q2.question,
            'options' : 'YES|NO|MAYBE'
        }
        # calling update_graded_quiz_question function via flask route
        response = self.client.post("/update_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'CID': self.gq2q2.CID,
                'LID': self.gq2q2.LID,
                'SID': self.gq2q2.SID,
                'question' : self.gq2q2.question,
                'answer' : self.gq2q2.answer,
                'options' : 'YES|NO|MAYBE',
                'duration': self.gq2q2.duration
            },
            'message' : f"Quiz question \'{self.gq2q2.question}\' has been updated"
            
        })
    

    # Testing negative case where cid missing in request body
    def test_update_graded_quiz_question_missing_cid(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
        
        # Preparing request body
        request_body = {
            'LID': self.gq2q2.LID,
            'SID': self.gq2q2.SID,
            'question' : self.gq2q2.question,
            'options' : 'YES|NO|MAYBE',
            'duration': self.gq2q2.duration
        }
        # calling update_graded_quiz_question function via flask route
        response = self.client.post("/update_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, graded quiz update failed"
        })
    

    # Testing negative case where lid missing in request body
    def test_update_graded_quiz_question_missing_lid(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
        
        # Preparing request body
        request_body = {
            'CID': self.gq2q2.CID,
            'SID': self.gq2q2.SID,
            'question' : self.gq2q2.question,
            'options' : 'YES|NO|MAYBE',
            'duration': self.gq2q2.duration
        }
        # calling update_graded_quiz_question function via flask route
        response = self.client.post("/update_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"LID is missing from request body, graded quiz update failed"
        })


class TestDeleteGradedQuiz(TestApp):
    # Testing positive case where all details are present in request body
    def test_delete_graded_quiz_all_details(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
    
        # Preparing request body
        request_body = {
            'CID': self.gq2q1.CID,
            'LID': self.gq2q1.LID,
            'SID': self.gq2q1.SID,
        }
        # calling delete_graded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_graded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : f"Quiz with the CID {self.gq2q1.CID} LID {self.gq2q1.LID} SID {self.gq2q1.SID} has been deleted successfully"
        })
        # calling read_graded_quiz function via flask route, making sure quiz no longer exists in database
        response = self.client.post("/read_graded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json, {
            'message' : f"Quiz with CID {self.gq2q1.CID} LID {self.gq2q1.LID} SID {self.gq2q1.SID} does not exist in database"
        })
        # calling read_graded_quiz function via flask route, making sure other quizzes have not been affected
        request_body = {
            'CID': self.gq1q1.CID,
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
        }
        response = self.client.post("/read_graded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json, {
            'data' : [
                {
                'CID': self.gq1q1.CID,
                'LID': self.gq1q1.LID,
                'SID': self.gq1q1.SID,
                'question': self.gq1q1.question,
                'answer': self.gq1q1.answer,
                'options': self.gq1q1.options,
                'duration': self.gq1q1.duration
                },
                {
                'CID': self.gq1q2.CID,
                'LID': self.gq1q2.LID,
                'SID': self.gq1q2.SID,
                'question': self.gq1q2.question,
                'answer': self.gq1q2.answer,
                'options': self.gq1q2.options,
                'duration': self.gq1q2.duration
                },
                {
                'CID': self.gq1q3.CID,
                'LID': self.gq1q3.LID,
                'SID': self.gq1q3.SID,
                'question': self.gq1q3.question,
                'answer': self.gq1q3.answer,
                'options': self.gq1q3.options,
                'duration': self.gq1q3.duration
                }
            ],
            'message' : f"Quiz with CID {self.gq1q1.CID}, LID {self.gq1q1.LID}, SID {self.gq1q1.SID} has been retrieved"
        })
    

    # Testing negative case where quiz is not in database
    def test_delete_graded_quiz_no_quiz(self):
        # Preparing request body
        request_body = {
            'CID': self.gq2q1.CID,
            'LID': self.gq2q1.LID,
            'SID': self.gq2q1.SID,
        }
        # calling delete_graded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_graded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz with the CID {self.gq2q1.CID} LID {self.gq2q1.LID} SID {self.gq2q1.SID} does not exist in the database"
        })
    

    # Testing negative case where cid is missing in request body
    def test_delete_graded_quiz_missing_cid(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
        # Preparing request body
        request_body = {
            'LID': self.gq2q1.LID,
            'SID': self.gq2q1.SID,
        }
        # calling delete_graded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_graded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, graded quiz deletion failed"
        })
    

    # Testing negative case where lid is missing in request body
    def test_delete_graded_quiz_missing_lid(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
        # Preparing request body
        request_body = {
            'CID': self.gq2q1.CID,
            'SID': self.gq2q1.SID,
        }
        # calling delete_graded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_graded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"LID is missing from request body, graded quiz deletion failed"
        })


class TestDeleteGradedQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body
    def test_delete_graded_quiz_question_all_details(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
    
        # Preparing request body
        request_body = {
            'CID': self.gq2q2.CID,
            'LID': self.gq2q2.LID,
            'SID': self.gq2q2.SID,
            'question' : self.gq2q2.question
        }
        # calling delete_graded_quiz_question function via flask route, checking if deletion went through
        response = self.client.post("/delete_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.gq2q2.question}\' with the CID {self.gq2q1.CID} LID {self.gq2q1.LID} SID {self.gq2q1.SID} has been deleted successfully"
        })
        # calling read_graded_quiz_question function via flask route, making sure quiz question have been deleted from database
        response = self.client.post("/read_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.gq2q2.question}\' with CID {self.gq2q2.CID} LID {self.gq2q2.LID} SID {self.gq2q2.SID} does not exist in database",
        })
        # calling read_graded_quiz function via flask route, making sure other quiz questions have not been affected
        request_body = {
            'CID': self.gq2q2.CID,
            'LID': self.gq2q2.LID,
            'SID': self.gq2q2.SID,
        }
        response = self.client.post("/read_graded_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json, {
            'data' : [
                {
                'CID': self.gq2q1.CID,
                'LID': self.gq2q1.LID,
                'SID': self.gq2q1.SID,
                'question': self.gq2q1.question,
                'answer': self.gq2q1.answer,
                'options': self.gq2q1.options,
                'duration': self.gq2q1.duration
                },
                {
                'CID': self.gq2q3.CID,
                'LID': self.gq2q3.LID,
                'SID': self.gq2q3.SID,
                'question': self.gq2q3.question,
                'answer': self.gq2q3.answer,
                'options': self.gq2q3.options,
                'duration': self.gq2q3.duration
                }
            ],
            'message' : f"Quiz with CID {self.gq2q2.CID}, LID {self.gq2q2.LID}, SID {self.gq2q2.SID} has been retrieved"
        })
    

    # Testing negative case where quiz question is not in database
    def test_delete_graded_quiz_question_no_quiz(self):
        # Preparing request body
        request_body = {
            'CID': self.gq2q1.CID,
            'LID': self.gq2q1.LID,
            'SID': self.gq2q1.SID,
            'question': self.gq2q1.question,
        }
        # calling delete_graded_quiz_question function via flask route, checking if deletion went through
        response = self.client.post("/delete_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.gq2q1.question}\' with the CID {self.gq2q1.CID} LID {self.gq2q1.LID} SID {self.gq2q1.SID} does not exist in the database"
        })
    

    # Testing negative case where cid is missing in request body
    def test_delete_graded_quiz_question_missing_cid(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
        # Preparing request body
        request_body = {
            'LID': self.gq2q1.LID,
            'SID': self.gq2q1.SID,
            'question': self.gq2q1.question,
        }
        # calling delete_graded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, graded quiz question deletion failed"
        })
    

    # Testing negative case where lid is missing in request body
    def test_delete_graded_quiz_question_missing_lid(self):
        #add dummy graded quizzes into database
        db.session.add(self.gq1q1)
        db.session.add(self.gq1q2)
        db.session.add(self.gq1q3)
        db.session.add(self.gq2q1)
        db.session.add(self.gq2q2)
        db.session.add(self.gq2q3)
        # Preparing request body
        request_body = {
            'CID': self.gq2q1.CID,
            'LID': self.gq2q1.LID,
            'SID': self.gq2q1.SID,
        }
        # calling delete_graded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_graded_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
                                    
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"question is missing from request body, graded quiz question deletion failed"
        })
    
### GRADED QUIZ TEST CASES ###

if __name__ == '__main__':
    unittest.main()
