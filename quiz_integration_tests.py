import unittest
import flask_testing
import json
from app import app, db, Quiz_questions
from datetime import datetime

#Group member in-charge: Alvan Tan
class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app


    def setUp(self):
        self.ugq1q1 = Quiz_questions(LID='1', SID='G2', CID='IS500', start='2021-10-21 09:15:00', question='Is the moon round?', 
                                    answer='YES', options='YES|NO', duration=2, type='ungraded')
        self.ugq1q2 = Quiz_questions(LID='1', SID='G2', CID='IS500', start='2021-10-21 09:15:00', question='Is the sun round?',
                                    answer='YES', options='YES|NO', duration=2, type='ungraded')
        self.ugq1q3 = Quiz_questions(LID='1', SID='G2', CID='IS500', start='2021-10-21 09:15:00', question='Which of these is not a planet?',
                                    answer='Pluto', options='EARTH|MARS|JUPITER|PLUTO|VENUS', duration=2, type='ungraded')
        
        self.gq1q1 = Quiz_questions(LID='2', SID='G2', CID='IS500', start='2021-10-21 09:15:00', question='Is Computational Thinking a hard module?', 
                                    answer='YES', options='YES|NO', duration=2, type='graded')
        self.gq1q2 = Quiz_questions(LID='2', SID='G2', CID='IS500', start='2021-10-21 09:15:00', question='Is Intro to Machine Learning hard?',
                                    answer='YES', options='YES|NO', duration=2, type='graded')
        self.gq1q3 = Quiz_questions(LID='2', SID='G2', CID='IS500', start='2021-10-21 09:15:00', question='What course is this code for?',
                                    answer='SPM', options='SPM|PMS|MPS|SMP|PSM', duration=2, type='graded')
        self.maxDiff = None
        db.create_all()


    def tearDown(self):
        self.ugq1q1 = None
        self.ugq1q2 = None
        self.ugq1q3 = None
        self.gq1q1 = None
        self.gq1q2 = None
        self.gq1q3 = None

        db.session.remove()
        db.drop_all()

### QUIZ TEST CASES ###
class TestCreateQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body
    def test_create_quiz_question_all_details(self):
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'CID': self.ugq1q1.CID,
            'start' : self.ugq1q1.start,
            'question': self.ugq1q1.question,
            'answer': self.ugq1q1.answer,
            'options': self.ugq1q1.options,
            'duration': self.ugq1q1.duration,
            'type' : self.ugq1q1.type
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/create_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'LID': self.ugq1q1.LID,
                'SID': self.ugq1q1.SID,
                'CID': self.ugq1q1.CID,
                'start': self.ugq1q1.start,
                'question': self.ugq1q1.question,
                'answer': self.ugq1q1.answer,
                'options': self.ugq1q1.options,
                'duration': self.ugq1q1.duration,
                'type': self.ugq1q1.type
            },
            'message' : f'Quiz question, {self.ugq1q1.question} ,has been inserted successfully into the database'
        })


    # Testing negative case where lid missing in request body
    def test_create_quiz_question_missing_lid(self):
        # Preparing request body
        request_body = {
            'SID': self.ugq1q1.SID,
            'CID': self.ugq1q1.CID,
            'start' : self.ugq1q1.start,
            'question': self.ugq1q1.question,
            'answer': self.ugq1q1.answer,
            'options': self.ugq1q1.options,
            'duration': self.ugq1q1.duration,
            'type' : self.ugq1q1.type
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/create_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"LID is missing from request body, quiz question creation failed"
        })

    # Testing negative case where sid missing in request body
    def test_create_quiz_question_missing_sid(self):
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'CID': self.ugq1q1.CID,
            'start' : self.ugq1q1.start,
            'question': self.ugq1q1.question,
            'answer': self.ugq1q1.answer,
            'options': self.ugq1q1.options,
            'duration': self.ugq1q1.duration,
            'type' : self.ugq1q1.type
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/create_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"SID is missing from request body, quiz question creation failed"
        })


    # Testing negative case where cid missing in request body
    def test_create_quiz_question_missing_cid(self):
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'start' : self.ugq1q1.start,
            'question': self.ugq1q1.question,
            'answer': self.ugq1q1.answer,
            'options': self.ugq1q1.options,
            'duration': self.ugq1q1.duration,
            'type' : self.ugq1q1.type
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/create_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, quiz question creation failed"
        })
    
    
    # Testing negative case where start missing in request body
    def test_create_quiz_question_missing_start(self):
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'CID' : self.ugq1q1.CID,
            'question': self.ugq1q1.question,
            'answer': self.ugq1q1.answer,
            'options': self.ugq1q1.options,
            'duration': self.ugq1q1.duration,
            'type' : self.ugq1q1.type
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/create_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"start is missing from request body, quiz question creation failed"
        })


    # Testing negative case where question missing in request body
    def test_create_quiz_question_missing_question(self):
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'CID': self.ugq1q1.CID,
            'start' : self.ugq1q1.start,
            'answer': self.ugq1q1.answer,
            'options': self.ugq1q1.options,
            'duration': self.ugq1q1.duration,
            'type' : self.ugq1q1.type
        }
        # calling create_ungraded_quiz_question function via flask route
        response = self.client.post("/create_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"question is missing from request body, quiz question creation failed"
        })


    # Testing negative case where answer missing in request body
    def test_create_quiz_question_missing_answer(self):
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'CID': self.ugq1q1.CID,
            'start' : self.ugq1q1.start,
            'question': self.ugq1q1.question,
            'options': self.ugq1q1.options,
            'duration': self.ugq1q1.duration,
            'type' : self.ugq1q1.type
        }
        # calling create_ungraded_quiz_question function via flask route
        response = self.client.post("/create_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"answer is missing from request body, quiz question creation failed"
        })


    # Testing negative case where options missing in request body
    def test_create_quiz_question_missing_options(self):
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'CID': self.ugq1q1.CID,
            'start' : self.ugq1q1.start,
            'question': self.ugq1q1.question,
            'answer': self.ugq1q1.answer,
            'duration': self.ugq1q1.duration,
            'type' : self.ugq1q1.type
        }
        # calling create_ungraded_quiz_question function via flask route
        response = self.client.post("/create_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"options is missing from request body, quiz question creation failed"
        })        


    # Testing negative case where duration missing in request body
    def test_create_quiz_question_missing_duration(self):
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'CID': self.ugq1q1.CID,
            'start' : self.ugq1q1.start,
            'question': self.ugq1q1.question,
            'answer': self.ugq1q1.answer,
            'options': self.ugq1q1.options,
            'type' : self.ugq1q1.type
        }
        # calling create_ungraded_quiz_question function via flask route
        response = self.client.post("/create_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"duration is missing from request body, quiz question creation failed"
        }) 


    # Testing negative case where type missing in request body
    def test_create_quiz_question_missing_type(self):
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'CID': self.ugq1q1.CID,
            'start' : self.ugq1q1.start,
            'question': self.ugq1q1.question,
            'answer': self.ugq1q1.answer,
            'options': self.ugq1q1.options,
            'duration' : self.ugq1q1.duration
        }
        # calling create_ungraded_quiz_question function via flask route
        response = self.client.post("/create_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"type is missing from request body, quiz question creation failed"
        })     


class TestReadQuiz(TestApp):
    # Testing positive case where all details are present in request body
    def test_read_quiz_all_details(self):
        #preserving the string input for comparison later
        t1 = self.ugq1q1.start

        #add dummy ungraded quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        db.session.commit()

        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'CID': self.ugq1q1.CID,
            'start' : t1
        }
        # calling read_quiz function via flask route
        response = self.client.post("/read_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : [
                {
                'LID': self.ugq1q1.LID,
                'SID': self.ugq1q1.SID,
                'CID': self.ugq1q1.CID,
                'start': t1,
                'question': self.ugq1q1.question,
                'answer': self.ugq1q1.answer,
                'options': self.ugq1q1.options,
                'duration': self.ugq1q1.duration,
                'type': self.ugq1q1.type
                },
                {
                'LID': self.ugq1q2.LID,
                'SID': self.ugq1q2.SID,
                'CID': self.ugq1q2.CID,
                'start': t1,
                'question': self.ugq1q2.question,
                'answer': self.ugq1q2.answer,
                'options': self.ugq1q2.options,
                'duration': self.ugq1q2.duration,
                'type': self.ugq1q2.type
                },
                {
                'LID': self.ugq1q3.LID,
                'SID': self.ugq1q3.SID,
                'CID': self.ugq1q3.CID,
                'start': t1,
                'question': self.ugq1q3.question,
                'answer': self.ugq1q3.answer,
                'options': self.ugq1q3.options,
                'duration': self.ugq1q3.duration,
                'type': self.ugq1q3.type
                }
            ],
            'message' : f"Quiz with LID: {self.ugq1q1.LID}, SID: {self.ugq1q1.SID}, CID: {self.ugq1q1.CID}, start: {t1} has been retrieved"
        })


    # Testing negative case where lid missing in request body
    def test_read_quiz_missing_lid(self):
        t1 = self.ugq1q1.start

        #add dummy ungraded quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        db.session.commit()

        # Preparing request body
        request_body = {
            'SID': self.ugq1q1.SID,
            'CID': self.ugq1q1.CID,
            'start' : t1
        }

        # calling read_quiz function via flask route
        response = self.client.post("/read_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        # self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"LID is missing from request body, quiz read failed"
        })


    # Testing negative case where sid missing in request body
    def test_read_quiz_missing_sid(self):
        t1 = self.ugq1q1.start

        #add dummy ungraded quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        db.session.commit()

        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'CID': self.ugq1q1.CID,
            'start' : t1
        }

        # calling read_quiz function via flask route
        response = self.client.post("/read_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        # self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"SID is missing from request body, quiz read failed"
        })


    # Testing negative case where cid missing in request body
    def test_read_quiz_missing_cid(self):
        t1 = self.ugq1q1.start

        #add dummy ungraded quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        db.session.commit()

        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'start' : t1
        }
        # calling read_quiz function via flask route
        response = self.client.post("/read_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, quiz read failed"
        })
    

    # Testing negative case where start missing in request body
    def test_read_quiz_missing_start(self):

        #add dummy ungraded quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        db.session.commit()

        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'CID' : self.ugq1q1.CID
        }
        # calling read_quiz function via flask route
        response = self.client.post("/read_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"start is missing from request body, quiz read failed"
        })
    

    # Testing negative case where quiz is not in database
    def test_read_quiz_no_quiz(self):
        # Preparing request body
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'CID': self.ugq1q1.CID,
            'start' : self.ugq1q1.start
        }
        # calling read_ungraded_quiz function via flask route
        response = self.client.post("/read_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz with LID: {self.ugq1q1.LID}, SID: {self.ugq1q1.SID}, CID: {self.ugq1q1.CID}, start: {self.ugq1q1.start} does not exist in database"
        })


class TestReadQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body
    def test_read_quiz_question_all_details(self):
        t1 = self.gq1q1.start
        
        #add dummy graded quizzes into database
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'SID': self.gq1q2.SID,
            'CID': self.gq1q2.CID,
            'start': t1,
            'question': self.gq1q2.question,
        }
        # calling read_quiz_question function via flask route
        response = self.client.post("/read_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : 
                {
                'LID': self.gq1q2.LID,
                'SID': self.gq1q2.SID,
                'CID': self.gq1q2.CID,
                'start': t1,
                'question': self.gq1q2.question,
                'answer': self.gq1q2.answer,
                'options': self.gq1q2.options,
                'duration': self.gq1q2.duration,
                'type': self.gq1q2.type
                },
            'message' : f"Quiz question \'{self.gq1q2.question}\' with LID {self.gq1q2.LID}, SID {self.gq1q2.SID}, CID {self.gq1q2.CID}, start {self.gq1q2.start} has been retrieved"
        })


    # Testing negative case where lid missing in request body
    def test_read_quiz_question_missing_lid(self):
        t1 = self.gq1q1.start
        
        #add dummy graded quizzes into database
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'SID': self.gq1q2.SID,
            'CID': self.gq1q2.CID,
            'start': t1,
            'question': self.gq1q2.question
        }
        # calling read_quiz_question function via flask route
        response = self.client.post("/read_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"LID is missing from request body, quiz question read failed"
        })


    # Testing negative case where sid missing in request body
    def test_read_quiz_question_missing_sid(self):
        t1 = self.gq1q1.start
        
        #add dummy graded quizzes into database
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'CID': self.gq1q2.CID,
            'start': t1,
            'question': self.gq1q2.question
        }
        # calling read_quiz_question function via flask route
        response = self.client.post("/read_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"SID is missing from request body, quiz question read failed"
        })


    # Testing negative case where cid missing in request body
    def test_read_quiz_question_missing_cid(self):
        t1 = self.gq1q1.start
        
        #add dummy graded quizzes into database
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'SID': self.gq1q2.SID,
            'start': t1,
            'question': self.gq1q2.question,
        }
        # calling read_quiz_question function via flask route
        response = self.client.post("/read_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, quiz question read failed"
        })
    

    # Testing negative case where start missing in request body
    def test_read_quiz_question_missing_start(self):
        t1 = self.gq1q1.start
        
        #add dummy graded quizzes into database
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'SID': self.gq1q2.SID,
            'CID': self.gq1q2.CID,
            'question': self.gq1q2.question,
        }
        # calling read_quiz_question function via flask route
        response = self.client.post("/read_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"start is missing from request body, quiz question read failed"
        })


    # Testing negative case where question missing in request body
    def test_read_quiz_question_missing_question(self):
        t1 = self.gq1q1.start
        
        #add dummy graded quizzes into database
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)

        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'SID': self.gq1q2.SID,
            'CID': self.gq1q2.CID,
            'start': t1,
        }
        # calling read_quiz_question function via flask route
        response = self.client.post("/read_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"question is missing from request body, quiz question read failed"
        })
    

    # Testing negative case where quiz is not in database
    def test_read_quiz_question_no_quiz(self):
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'SID': self.gq1q2.SID,
            'CID': self.gq1q2.CID,
            'question': self.gq1q2.question,
            'start': self.gq1q2.start,
        }
        # calling read_quiz function via flask route
        response = self.client.post("/read_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.gq1q2.question}\' with LID {self.gq1q2.LID}, SID {self.gq1q2.SID}, CID {self.gq1q2.CID}, start {self.gq1q2.start} does not exist in database"
        })


class TestUpdateQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body, changing answer to NO
    def test_update_quiz_question_all_details_change_answer_and_options(self):
        t1 = self.gq1q2.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'SID': self.gq1q2.SID,
            'CID': self.gq1q2.CID,
            'question': self.gq1q2.question,
            'start': t1,
            'answer': 'HELLO',
            'options': 'HELLO|HI|BYE'
        }
        # calling update_quiz_question function via flask route
        response = self.client.post("/update_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'LID': self.gq1q2.LID,
                'SID': self.gq1q2.SID,
                'CID': self.gq1q2.CID,
                'question': self.gq1q2.question,
                'start': t1,
                'answer': 'HELLO',
                'options': 'HELLO|HI|BYE',
                'duration': self.gq1q2.duration,
                'type': self.gq1q2.type
            },
            'message' : f"Quiz question \'{self.gq1q2.question}\' has been updated"
            
        })


    # Testing positive case where all details are present in request body, changing duration to 5, type to ungraded
    def test_update_quiz_question_all_details_change_duration_and_type(self):
        t1 = self.gq1q2.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'SID': self.gq1q2.SID,
            'CID': self.gq1q2.CID,
            'question': self.gq1q2.question,
            'start': t1,
            'duration': 5,
            'type': 'ungraded'
        }
        # calling update_quiz_question function via flask route
        response = self.client.post("/update_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : {
                'LID': self.gq1q2.LID,
                'SID': self.gq1q2.SID,
                'CID': self.gq1q2.CID,
                'question': self.gq1q2.question,
                'start': t1,
                'answer': self.gq1q2.answer,
                'options': self.gq1q2.options,
                'duration': 5,
                'type': 'ungraded'
            },
            'message' : f"Quiz question \'{self.gq1q2.question}\' has been updated"
            
        })
    

    # Testing negative case where lid missing in request body
    def test_update_quiz_question_missing_lid(self):
        t1 = self.gq1q2.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        
        # Preparing request body
        request_body = {
            'SID': self.gq1q2.SID,
            'CID': self.gq1q2.CID,
            'question': self.gq1q2.question,
            'start': t1,
            'duration': 5,
            'type': 'ungraded'
        }
        # calling update_quiz_question function via flask route
        response = self.client.post("/update_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"LID is missing from request body, quiz update failed"
        })
    
    
    # Testing negative case where sid missing in request body
    def test_update_quiz_question_missing_sid(self):
        t1 = self.gq1q2.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'CID': self.gq1q2.CID,
            'question': self.gq1q2.question,
            'start': t1,
            'duration': 5,
            'type': 'ungraded'
        }
        # calling update_quiz_question function via flask route
        response = self.client.post("/update_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"SID is missing from request body, quiz update failed"
        })
    

    # Testing negative case where cid missing in request body
    def test_update_quiz_question_missing_cid(self):
        t1 = self.gq1q2.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'SID': self.gq1q2.SID,
            'question': self.gq1q2.question,
            'start': t1,
            'duration': 5,
            'type': 'ungraded'
        }
        # calling update_quiz_question function via flask route
        response = self.client.post("/update_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, quiz update failed"
        })
    

    # Testing negative case where question missing in request body
    def test_update_quiz_question_missing_question(self):
        t1 = self.gq1q2.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'SID': self.gq1q2.SID,
            'CID': self.gq1q2.CID,
            'start': t1,
            'duration': 5,
            'type': 'ungraded'
        }
        # calling update_quiz_question function via flask route
        response = self.client.post("/update_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"question is missing from request body, quiz update failed"
        })
    

    # Testing negative case where start missing in request body
    def test_update_quiz_question_missing_start(self):
        t1 = self.gq1q2.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'SID': self.gq1q2.SID,
            'CID': self.gq1q2.CID,
            'question': self.gq1q2.question,
            'duration': 5,
            'type': 'ungraded'
        }
        # calling update_quiz_question function via flask route
        response = self.client.post("/update_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"start is missing from request body, quiz update failed"
        })
    

    # Testing negative case where quiz is not in database
    def test_update_quiz_question_no_quiz(self):
        # Preparing request body
        request_body = {
            'LID': self.gq1q2.LID,
            'SID': self.gq1q2.SID,
            'CID': self.gq1q2.CID,
            'question': self.gq1q2.question,
            'start': self.gq1q2.start,
            'duration': 5,
            'type': 'ungraded'
        }
        # calling read_quiz function via flask route
        response = self.client.post("/update_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.gq1q2.question}\' with LID {self.gq1q2.LID}, SID {self.gq1q2.SID}, CID {self.gq1q2.CID}, start {self.gq1q2.start} does not exist in database"
        })


class TestDeleteQuiz(TestApp):
    # Testing positive case where all details are present in request body
    def test_delete_quiz_all_details(self):
        t1 = self.gq1q1.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
    
        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'CID': self.gq1q1.CID,
            'start': t1
            
        }
        # calling delete_ungraded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : f"Quiz with LID: {self.gq1q1.LID}, SID: {self.gq1q1.SID}, CID: {self.gq1q1.CID}, start: {self.gq1q1.start} has been deleted successfully"
        })
        # calling read_quiz function via flask route, making sure quiz no longer exists in database
        response = self.client.post("/read_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            'message' : f"Quiz with LID: {self.gq1q1.LID}, SID: {self.gq1q1.SID}, CID: {self.gq1q1.CID}, start: {self.gq1q1.start} does not exist in database"
        })
        # calling read_quiz function via flask route, making sure other quizzes have not been affected
        request_body = {
            'LID': self.ugq1q1.LID,
            'SID': self.ugq1q1.SID,
            'CID': self.ugq1q1.CID,
            'start': t1
        }
        response = self.client.post("/read_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            'data' : [
                {
                'LID': self.ugq1q1.LID,
                'SID': self.ugq1q1.SID,
                'CID': self.ugq1q1.CID,
                'start': t1,
                'question': self.ugq1q1.question,
                'answer': self.ugq1q1.answer,
                'options': self.ugq1q1.options,
                'duration': self.ugq1q1.duration,
                'type': self.ugq1q1.type
                },
                {
                'LID': self.ugq1q2.LID,
                'SID': self.ugq1q2.SID,
                'CID': self.ugq1q2.CID,
                'start': t1,
                'question': self.ugq1q2.question,
                'answer': self.ugq1q2.answer,
                'options': self.ugq1q2.options,
                'duration': self.ugq1q2.duration,
                'type': self.ugq1q2.type
                },
                {
                'LID': self.ugq1q3.LID,
                'SID': self.ugq1q3.SID,
                'CID': self.ugq1q3.CID,
                'start': t1,
                'question': self.ugq1q3.question,
                'answer': self.ugq1q3.answer,
                'options': self.ugq1q3.options,
                'duration': self.ugq1q3.duration,
                'type': self.ugq1q3.type
                }
            ],
            'message' : f"Quiz with LID: {self.ugq1q1.LID}, SID: {self.ugq1q1.SID}, CID: {self.ugq1q1.CID}, start: {self.ugq1q1.start} has been retrieved"
        })
    

    # Testing negative case where quiz is not in database
    def test_delete_quiz_no_quiz(self):
        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'CID': self.gq1q1.CID,
            'start': self.gq1q1.start
        }
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        
        # calling delete_ungraded_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz with LID: {self.gq1q1.LID}, SID: {self.gq1q1.SID}, CID: {self.gq1q1.CID}, start: {self.gq1q1.start} does not exist in the database"
        })
    

    # Testing negative case where lid is missing in request body
    def test_delete_quiz_missing_lid(self):
        t1 = self.gq1q1.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)

        # Preparing request body
        request_body = {
            'SID': self.gq1q1.SID,
            'CID': self.gq1q1.CID,
            'start': t1
        }
        # calling delete_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"LID is missing from request body, quiz deletion failed"
        })


    # Testing negative case where sid is missing in request body
    def test_delete_quiz_missing_sid(self):
        t1 = self.gq1q1.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)

        # Preparing request body
        request_body = {
            
            'LID': self.gq1q1.LID,
            'CID': self.gq1q1.CID,
            'start': t1
        }
        # calling delete_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"SID is missing from request body, quiz deletion failed"
        })


    # Testing negative case where cid is missing in request body
    def test_delete_quiz_missing_cid(self):
        t1 = self.gq1q1.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)

        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'start': t1
        }
        # calling delete_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, quiz deletion failed"
        })
    

    # Testing negative case where start is missing in request body
    def test_delete_quiz_missing_start(self):
        t1 = self.gq1q1.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)

        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'CID': self.gq1q1.CID
        }
        # calling delete_quiz function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"start is missing from request body, quiz deletion failed"
        })
    

class TestDeleteQuizQuestion(TestApp):
    # Testing positive case where all details are present in request body
    def test_delete_quiz_question_all_details(self):
        t1 = self.gq1q1.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
    
        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'CID': self.gq1q1.CID,
            'start': t1,
            'question': self.gq1q1.question
        }
        # calling delete_quiz_question function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.gq1q1.question}\' with LID: {self.gq1q1.LID}, SID: {self.gq1q1.SID}, CID: {self.gq1q1.CID}, start: {self.gq1q1.start} has been deleted successfully"
        })
        # calling read_quiz_question function via flask route, making sure quiz question have been deleted from database
        response = self.client.post("/read_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.gq1q1.question}\' with LID {self.gq1q1.LID}, SID {self.gq1q1.SID}, CID {self.gq1q1.CID}, start {self.gq1q1.start} does not exist in database",
        })
        # calling read_quiz function via flask route, making sure other quiz questions have not been affected
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'CID': self.gq1q1.CID,
            'start': t1
        }
        response = self.client.post("/read_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.json, {
            'data' : [
                {
                'LID': self.gq1q2.LID,
                'SID': self.gq1q2.SID,
                'CID': self.gq1q2.CID,
                'start': t1,
                'question': self.gq1q2.question,
                'answer': self.gq1q2.answer,
                'options': self.gq1q2.options,
                'duration': self.gq1q2.duration,
                'type': self.gq1q2.type
                },
                {
                'LID': self.gq1q3.LID,
                'SID': self.gq1q3.SID,
                'CID': self.gq1q3.CID,
                'start': t1,
                'question': self.gq1q3.question,
                'answer': self.gq1q3.answer,
                'options': self.gq1q3.options,
                'duration': self.gq1q3.duration,
                'type': self.gq1q3.type
                }
            ],
            'message' : f"Quiz with LID: {self.gq1q1.LID}, SID: {self.gq1q1.SID}, CID: {self.gq1q1.CID}, start: {t1} has been retrieved"
        })


    # Testing negative case where quiz question is not in database
    def test_delete_quiz_question_no_question(self):
        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'CID': self.gq1q1.CID,
            'start': self.gq1q1.start,
            'question': self.gq1q1.question
        }
        # calling delete_quiz_question function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz question \'{self.gq1q1.question}\' with LID: {self.gq1q1.LID}, SID: {self.gq1q1.SID}, CID: {self.gq1q1.CID}, start: {self.gq1q1.start} does not exist in the database"
        })
    

    # Testing negative case where lid is missing in request body
    def test_delete_quiz_question_missing_lid(self):
        t1 = self.gq1q1.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        # Preparing request body
        request_body = {
            'SID': self.gq1q1.SID,
            'CID': self.gq1q1.CID,
            'start': t1,
            'question': self.gq1q1.question
        }
        # calling delete_quiz_question function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"LID is missing from request body, quiz question deletion failed"
        })


    # Testing negative case where sid is missing in request body
    def test_delete_quiz_question_missing_sid(self):
        t1 = self.gq1q1.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'CID': self.gq1q1.CID,
            'start': t1,
            'question': self.gq1q1.question
        }
        # calling delete_quiz_question function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"SID is missing from request body, quiz question deletion failed"
        })


    # Testing negative case where cid is missing in request body
    def test_delete_quiz_question_missing_cid(self):
        t1 = self.gq1q1.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'start': t1,
            'question': self.gq1q1.question
        }
        # calling delete_quiz_question function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"CID is missing from request body, quiz question deletion failed"
        })
    

    # Testing negative case where start is missing in request body
    def test_delete_quiz_question_missing_start(self):
        t1 = self.gq1q1.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'CID': self.gq1q1.CID,
            'question': self.gq1q1.question
        }
        # calling delete_quiz_question function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"start is missing from request body, quiz question deletion failed"
        })
    

    # Testing negative case where question is missing in request body
    def test_delete_quiz_question_missing_question(self):
        t1 = self.gq1q1.start

        #add dummy quizzes into database
        self.ugq1q1.start = datetime.fromisoformat(self.ugq1q1.start)
        db.session.add(self.ugq1q1)
        self.ugq1q2.start = datetime.fromisoformat(self.ugq1q2.start)
        db.session.add(self.ugq1q2)
        self.ugq1q3.start = datetime.fromisoformat(self.ugq1q3.start)
        db.session.add(self.ugq1q3)
        self.gq1q1.start = datetime.fromisoformat(self.gq1q1.start)
        db.session.add(self.gq1q1)
        self.gq1q2.start = datetime.fromisoformat(self.gq1q2.start)
        db.session.add(self.gq1q2)
        self.gq1q3.start = datetime.fromisoformat(self.gq1q3.start)
        db.session.add(self.gq1q3)
        # Preparing request body
        request_body = {
            'LID': self.gq1q1.LID,
            'SID': self.gq1q1.SID,
            'CID': self.gq1q1.CID,
            'start': t1
        }
        # calling delete_quiz_question function via flask route, checking if deletion went through
        response = self.client.post("/delete_quiz_question",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"question is missing from request body, quiz question deletion failed"
        })
    
### QUIZ TEST CASES ###

if __name__ == '__main__':
    #For jenkins
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    #For local tests
    # unittest.main()
