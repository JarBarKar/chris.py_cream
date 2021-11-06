import unittest
import flask_testing
import json
from app import app, db, Quiz_questions, Quiz_record
from datetime import datetime


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True


    def create_app(self):
        return app


    def setUp(self):
        self.q1 = Quiz_questions(LID='1', SID='G1', CID='IS111', start='2021-10-21 09:15:00', question='Is the moon round?', 
                                    answer='YES', options='YES|NO', duration=2, type='ungraded')
        self.q2 = Quiz_questions(LID='1', SID='G1', CID='IS111', start='2021-10-21 09:15:00', question='Is the sun round?',
                                    answer='YES', options='YES|NO', duration=2, type='ungraded')
        self.q3 = Quiz_questions(LID='1', SID='G1', CID='IS111', start='2021-10-21 09:15:00', question='Which of these is not a planet?',
                                    answer='PLUTO', options='EARTH|MARS|JUPITER|PLUTO|VENUS', duration=2, type='ungraded')
        
        self.a1 = Quiz_record(EID=1, LID='1', SID='G1', CID='IS111', start='2021-10-21 09:15:00', question='Is the moon round?', 
                                    answer_given='YES',marks=1)
        self.a2 = Quiz_record(EID=1, LID='1', SID='G1', CID='IS111', start='2021-10-21 09:15:00', question='Is the sun round?',
                                    answer_given='NO',marks=0)
        self.a3 = Quiz_record(EID=1, LID='1', SID='G1', CID='IS111', start='2021-10-21 09:15:00', question='Which of these is not a planet?',
                                    answer_given='EARTH',marks=0)

        self.b1 = Quiz_record(EID=2, LID='1', SID='G1', CID='IS111', start='2021-10-21 09:15:00', question='Is the moon round?', 
                                    answer_given='YES',marks=1)
        self.b2 = Quiz_record(EID=2, LID='1', SID='G1', CID='IS111', start='2021-10-21 09:15:00', question='Is the sun round?',
                                    answer_given='NO',marks=0)
        self.b3 = Quiz_record(EID=2, LID='1', SID='G1', CID='IS111', start='2021-10-21 09:15:00', question='Which of these is not a planet?',
                                    answer_given='EARTH',marks=0)
        
        self.maxDiff = None
        db.create_all()


    def tearDown(self):
        self.q1 = None
        self.q2 = None
        self.q3 = None
        self.a1 = None
        self.a2 = None
        self.a3 = None

        db.session.remove()
        db.drop_all()

### QUIZ RECORD TEST CASES ###
class TestCheckQuizResult(TestApp):
    # Testing positive case where all details are present in request body
    def test_check_quiz_result_all_details(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        self.q1.start = datetime.fromisoformat(self.q1.start)
        db.session.add(self.q1)
        self.q2.start = datetime.fromisoformat(self.q2.start)
        db.session.add(self.q2)
        self.q3.start = datetime.fromisoformat(self.q3.start)
        db.session.add(self.q3)
        self.a1.start = datetime.fromisoformat(self.a1.start)
        db.session.add(self.a1)
        self.a2.start = datetime.fromisoformat(self.a2.start)
        db.session.add(self.a2)
        self.a3.start = datetime.fromisoformat(self.a3.start)
        db.session.add(self.a3)
        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'SID': self.a1.SID,
            'CID': self.a1.CID,
            'start' : t1,
            'EID': self.a1.EID
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/check_quiz_result",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'data' : [
            {
                "CID": "IS111",
                "EID": 1,
                "LID": "1",
                "SID": "G1",
                "answer_given": "YES",
                "correct_answer": "YES",
                "marks": 1,
                "options": "YES|NO",
                "question": "Is the moon round?",
                "right_wrong": "right",
                "start": "2021-10-21 09:15:00"
            },
            {
                "CID": "IS111",
                "EID": 1,
                "LID": "1",
                "SID": "G1",
                "answer_given": "NO",
                "correct_answer": "YES",
                "marks": 0,
                "options": "YES|NO",
                "question": "Is the sun round?",
                "right_wrong": "wrong",
                "start": "2021-10-21 09:15:00"
            },
            {
                "CID": "IS111",
                "EID": 1,
                "LID": "1",
                "SID": "G1",
                "answer_given": "EARTH",
                "correct_answer": "PLUTO",
                "marks": 0,
                "options": "EARTH|MARS|JUPITER|PLUTO|VENUS",
                "question": "Which of these is not a planet?",
                "right_wrong": "wrong",
                "start": "2021-10-21 09:15:00"
            }
        ]
            ,
            'message' : f"Quiz record { self.a1.CID, self.a1.SID, self.a1.LID, self.a1.EID} has been retrieved successfully from the database"
        })
    def test_check_quiz_result_no_EID(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        self.q1.start = datetime.fromisoformat(self.q1.start)
        db.session.add(self.q1)
        self.q2.start = datetime.fromisoformat(self.q2.start)
        db.session.add(self.q2)
        self.q3.start = datetime.fromisoformat(self.q3.start)
        db.session.add(self.q3)
        self.a1.start = datetime.fromisoformat(self.a1.start)
        db.session.add(self.a1)
        self.a2.start = datetime.fromisoformat(self.a2.start)
        db.session.add(self.a2)
        self.a3.start = datetime.fromisoformat(self.a3.start)
        db.session.add(self.a3)
        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'SID': self.a1.SID,
            'CID': self.a1.CID,
            'start' : t1
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/check_quiz_result",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Request ['EID'] is not present, request is not query successfully"
        })

    def test_check_quiz_result_no_EID_SID(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        self.q1.start = datetime.fromisoformat(self.q1.start)
        db.session.add(self.q1)
        self.q2.start = datetime.fromisoformat(self.q2.start)
        db.session.add(self.q2)
        self.q3.start = datetime.fromisoformat(self.q3.start)
        db.session.add(self.q3)
        self.a1.start = datetime.fromisoformat(self.a1.start)
        db.session.add(self.a1)
        self.a2.start = datetime.fromisoformat(self.a2.start)
        db.session.add(self.a2)
        self.a3.start = datetime.fromisoformat(self.a3.start)
        db.session.add(self.a3)
        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'CID': self.a1.CID,
            'start' : t1
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/check_quiz_result",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Request ['EID', 'SID'] is not present, request is not query successfully"
        })

    def test_check_quiz_result_no_input(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        self.q1.start = datetime.fromisoformat(self.q1.start)
        db.session.add(self.q1)
        self.q2.start = datetime.fromisoformat(self.q2.start)
        db.session.add(self.q2)
        self.q3.start = datetime.fromisoformat(self.q3.start)
        db.session.add(self.q3)
        self.a1.start = datetime.fromisoformat(self.a1.start)
        db.session.add(self.a1)
        self.a2.start = datetime.fromisoformat(self.a2.start)
        db.session.add(self.a2)
        self.a3.start = datetime.fromisoformat(self.a3.start)
        db.session.add(self.a3)
        db.session.commit()
        # Preparing request body
        request_body = {

        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/check_quiz_result",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Request ['EID', 'SID', 'CID', 'LID', 'start'] is not present, request is not query successfully"
        })

    def test_check_quiz_record_no_exist(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        self.q1.start = datetime.fromisoformat(self.q1.start)
        db.session.add(self.q1)
        self.q2.start = datetime.fromisoformat(self.q2.start)
        db.session.add(self.q2)
        self.q3.start = datetime.fromisoformat(self.q3.start)
        db.session.add(self.q3)
        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'SID': self.a1.SID,
            'CID': self.a1.CID,
            'start' : t1,
            'EID': self.a1.EID
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/check_quiz_result",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Quiz question {self.a1.CID, self.a1.SID, self.a1.LID, self.a1.EID} do not exist"
        })

    def test_check_quiz_question_no_exist(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        self.a1.start = datetime.fromisoformat(self.a1.start)
        db.session.add(self.a1)
        self.a2.start = datetime.fromisoformat(self.a2.start)
        db.session.add(self.a2)
        self.a3.start = datetime.fromisoformat(self.a3.start)
        db.session.add(self.a3)
        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'SID': self.a1.SID,
            'CID': self.a1.CID,
            'start' : t1,
            'EID': self.a1.EID
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/check_quiz_result",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Quiz record {self.a1.CID, self.a1.SID, self.a1.LID, self.a1.EID} do not exist"
        })

    def test_check_quiz_database_no_exist(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database

        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'SID': self.a1.SID,
            'CID': self.a1.CID,
            'start' : t1,
            'EID': self.a1.EID
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/check_quiz_result",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "message": f"Both quiz question and record {self.a1.CID, self.a1.SID, self.a1.LID, self.a1.EID} do not exist"
        })




class TestCheckSubmitQuiz(TestApp):
    # Testing positive case where all details are present in request body
    def test_submit_quiz_details_ungraded(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'SID': self.a1.SID,
            'CID': self.a1.CID,
            'start' : t1,
            'EID': self.a1.EID,
            'QAMarks': [{
                'question': self.a1.question,
                'answer': self.a1.answer_given,
                'marks': self.a1.marks
            },
            {
                'question': self.a2.question,
                'answer': self.a2.answer_given,
                'marks': self.a2.marks
            },
            {
                'question': self.a3.question,
                'answer': self.a3.answer_given,
                'marks': self.a3.marks
            },
            ],
            'type': 'ungraded'
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/submit_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : f"Quiz record { self.a1.CID, self.a1.SID, self.a1.LID, self.a1.EID} has been inserted successfully into the database."
        })



    def test_submit_quiz_details_graded_pass(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'SID': self.a1.SID,
            'CID': self.a1.CID,
            'start' : t1,
            'EID': self.a1.EID,
            'QAMarks': [{
                'question': self.a1.question,
                'answer': self.a1.answer_given,
                'marks': 1
            },
            {
                'question': self.a2.question,
                'answer': self.a2.answer_given,
                'marks': 1
            },
            {
                'question': self.a3.question,
                'answer': self.a3.answer_given,
                'marks': 1
            },
            ],
            'type': 'graded'
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/submit_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : f"Quiz record { self.a1.CID, self.a1.SID, self.a1.LID, self.a1.EID} has been inserted successfully into the database.Engineer passed the course"
        })


    def test_submit_quiz_details_graded_fail(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'SID': self.a1.SID,
            'CID': self.a1.CID,
            'start' : t1,
            'EID': self.a1.EID,
            'QAMarks': [{
                'question': self.a1.question,
                'answer': self.a1.answer_given,
                'marks': self.a1.marks
            },
            {
                'question': self.a2.question,
                'answer': self.a2.answer_given,
                'marks': self.a2.marks
            },
            {
                'question': self.a3.question,
                'answer': self.a3.answer_given,
                'marks': self.a3.marks
            },
            ],
            'type': 'graded'
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/submit_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'message' : f"Quiz record { self.a1.CID, self.a1.SID, self.a1.LID, self.a1.EID} has been inserted successfully into the database.Engineer failed the course"
        })

    def test_submit_quiz_already_present_ungraded(self):
        t1 = self.b1.start
        #add dummy ungraded quizzes into database
        self.a1.start = datetime.fromisoformat(self.a1.start)
        db.session.add(self.a1)
        self.a2.start = datetime.fromisoformat(self.a2.start)
        db.session.add(self.a2)
        self.a3.start = datetime.fromisoformat(self.a3.start)
        db.session.add(self.a3)
        db.session.commit()
        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'SID': self.a1.SID,
            'CID': self.a1.CID,
            'start' : t1,
            'EID': self.a1.EID,
            'QAMarks': [{
                'question': self.a1.question,
                'answer': self.a1.answer_given,
                'marks': self.a1.marks
            },
            {
                'question': self.a2.question,
                'answer': self.a2.answer_given,
                'marks': self.a2.marks
            },
            {
                'question': self.a3.question,
                'answer': self.a3.answer_given,
                'marks': self.a3.marks
            },
            ],
            'type': 'ungraded'
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/submit_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Record { self.a1.CID, self.a1.SID, self.a1.LID, self.a1.EID} already exist, submission fail"
        })


    def test_submit_quiz_no_SID_ungraded(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'CID': self.a1.CID,
            'start' : t1,
            'EID': self.a1.EID,
            'QAMarks': [{
                'question': self.a1.question,
                'answer': self.a1.answer_given,
                'marks': self.a1.marks
            },
            {
                'question': self.a2.question,
                'answer': self.a2.answer_given,
                'marks': self.a2.marks
            },
            {
                'question': self.a3.question,
                'answer': self.a3.answer_given,
                'marks': self.a3.marks
            },
            ],
            'type': 'ungraded'
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/submit_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz record ['SID'] is not present, quiz submittion is not successfully"
        })


    def test_submit_quiz_no_SID_CID(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        # Preparing request body
        request_body = {
            'LID': self.a1.LID,
            'start' : t1,
            'EID': self.a1.EID,
            'QAMarks': [{
                'question': self.a1.question,
                'answer': self.a1.answer_given,
                'marks': self.a1.marks
            },
            {
                'question': self.a2.question,
                'answer': self.a2.answer_given,
                'marks': self.a2.marks
            },
            {
                'question': self.a3.question,
                'answer': self.a3.answer_given,
                'marks': self.a3.marks
            },
            ],
            'type': 'ungraded'
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/submit_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz record ['SID', 'CID'] is not present, quiz submittion is not successfully"
        })


    def test_submit_quiz_nothing(self):
        t1 = self.a1.start
        #add dummy ungraded quizzes into database
        # Preparing request body
        request_body = {
        }
        # calling create_quiz_question function via flask route
        response = self.client.post("/submit_quiz",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            'message' : f"Quiz record ['EID', 'SID', 'CID', 'LID', 'start', 'QAMarks', 'type'] is not present, quiz submittion is not successfully"
        })
### QUIZ TEST CASES ###

if __name__ == '__main__':
    #For jenkins
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    #For local tests
    # unittest.main()
