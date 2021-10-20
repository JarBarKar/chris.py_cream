
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from datetime import datetime

from sqlalchemy.sql.elements import Null

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@127.0.0.1:3306/spm_lms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

print('hello')

### Course Class ###
class Course(db.Model):
    __tablename__ = 'course'
    CID = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    prerequisites= db.Column(db.String(64), nullable=False)


    def __init__(self, CID, name, prerequisites):
        self.CID = CID
        self.name = name
        self.prerequisites = prerequisites

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {"CID": self.CID, "name": self.name, 
        "prerequisites": self.prerequisites}

    def list_of_prerequisites(self):
        return self.prerequisites.split(',')
### Course Class ###


### Academic record Class ###
class Academic_record(db.Model):
    __tablename__ = 'academic_record'
    EID = db.Column(db.Integer(), primary_key=True)
    SID = db.Column(db.String(64), primary_key=True)
    CID = db.Column(db.String(64), primary_key=True)
    QID = db.Column(db.Integer(), nullable=True)
    status = db.Column(db.String(64), nullable=False)
    quiz_result = db.Column(db.Integer(), nullable=False)


    def __init__(self, EID, SID, CID, QID, status, quiz_result):
        self.EID = EID
        self.SID = SID
        self.CID = CID
        self.QID = QID
        self.status = status
        self.quiz_result = quiz_result

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {"CID": self.CID, "EID": self.EID, "SID": self.SID, "QID": self.QID, "status": self.status, "quiz_result": self.quiz_result}
### Academic record Class ###


### Enrollment Class ###
class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    EID = db.Column(db.Integer(), primary_key=True)
    SID = db.Column(db.String(64), primary_key=True)
    CID = db.Column(db.String(64), primary_key=True)


    def __init__(self, EID, SID, CID):
        self.EID = EID
        self.SID = SID
        self.CID = CID

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {"CID": self.CID, "EID": self.EID, "SID": self.SID}
### Enrollment Class ###


### Section Class ###
class Section(db.Model):
    __tablename__ = 'section'
    SID = db.Column(db.String(64), primary_key=True)
    CID = db.Column(db.String(64), primary_key=True)
    start = db.Column(db.DateTime, nullable=False, primary_key=True)
    end = db.Column(db.DateTime, nullable=False)
    vacancy = db.Column(db.Integer(), nullable=False)
    TID = db.Column(db.Integer(), nullable=False)


    def __init__(self, SID, CID, start, end, vacancy, TID):
        self.SID = SID
        self.CID = CID
        self.start = start
        self.end = end
        self.vacancy = vacancy
        self.TID = TID


    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {"SID": self.SID, "CID": self.CID, "start": self.start, "end": self.end ,"vacancy": self.vacancy, "TID": self.TID}
### Section Class ###


### Trainer Class ###
class Trainer(db.Model):
    __tablename__ = 'trainer'
    TID = db.Column(db.Integer(), nullable=False, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.Integer(),nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)

    def __init__(self, TID, name, password, phone, email, address):
        self.TID = TID
        self.name = name
        self.password = password
        self.phone = phone
        self.email = email
        self.address = address


    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {"TID": self.TID, "name": self.name, "password": self.password, "phone": self.phone, "email": self.email, "address": self.address}
### Trainer Class ###

# NEED TO CHANGE, REMOVE THIS AFTER CHANGE
### Section_content Class ###
class Section_content(db.Model):
    __tablename__ = 'section_content'
    SID = db.Column(db.String(64), primary_key=True)
    CID = db.Column(db.String(64), primary_key=True)
    content_name = db.Column(db.String(64), primary_key=True)
    QID = db.Column(db.Integer(), nullable=True)
    content_type = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __init__(self, SID, CID, QID, content_name, content_type, link):
        self.SID = SID
        self.CID = CID
        self.QID = QID
        self.content_type = content_type
        self.content_name = content_name
        self.link = link


    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {"SID": self.SID, "CID": self.CID, "QID": self.QID, "content_type": self.content_type ,"content_name": self.content_name, "link": self.link}
### Section_content Class ###

### Lesson Class ###
class Lesson(db.Model):
    __tablename__ = 'lesson'
    LID = db.Column(db.String(64), primary_key=True)
    SID = db.Column(db.String(64), primary_key=True)
    CID = db.Column(db.String(64), primary_key=True)

    
    def __init__(self, LID, SID, CID):
        self.LID = LID
        self.SID = SID
        self.CID = CID


    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result


    def json(self):
        return {"LID": self.LID, "SID": self.SID, "CID": self.CID}
### Lesson Class ###

### Ungraded Quiz Class ###
class Ungraded_quiz(db.Model):
    __tablename__ = 'ungraded_quiz'
    LID = db.Column(db.Integer(), primary_key=True)
    CID = db.Column(db.String(64), primary_key=True)
    SID = db.Column(db.String(64), primary_key=True)
    question = db.Column(db.String(64), primary_key=True)
    answer = db.Column(db.String(64), nullable=False)
    options = db.Column(db.String(64), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)


    def __init__(self, LID, CID, SID, question, answer, options, duration):
        self.LID = LID
        self.CID = CID
        self.SID = SID
        self.question = question
        self.answer = answer
        self.options = options
        self.duration = duration


    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {"CID": self.CID, "LID": self.LID, "SID": self.SID,  "question": self.question,
                "answer":self.answer, "options":self.options, "duration":self.duration}
### Ungraded Quiz Class ###


### Graded Quiz Class ###
class Graded_quiz(db.Model):
    __tablename__ = 'Graded_quiz'
    LID = db.Column(db.Integer(), primary_key=True)
    CID = db.Column(db.String(64), primary_key=True)
    SID = db.Column(db.String(64), primary_key=True)
    question = db.Column(db.String(64), primary_key=True)
    answer = db.Column(db.String(64), nullable=False)
    options = db.Column(db.String(64), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)


    def __init__(self, LID, CID, SID, question, answer, options, duration):
        self.LID = LID
        self.CID = CID
        self.SID = SID
        self.question = question
        self.answer = answer
        self.options = options
        self.duration = duration


    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {"CID": self.CID, "LID": self.LID, "SID": self.SID,  "question": self.question,
                "answer":self.answer, "options":self.options, "duration":self.duration}
### Graded Quiz Class ###


### Start of API points for Course CRUD ###
@app.route("/view_courses", methods=['GET'])
#view all courses
def view_all_courses():
    retrieved_courses = Course.query.all()
    courses = [course.to_dict() for course in retrieved_courses]
    if courses:
        return jsonify(
            {
                "message": "All courses are retrieved",
                "data": courses
            }
        ), 200
    return jsonify(
        {
            "message": "There are no course retrieved"
        }
    ), 500

#view eligible courses
@app.route("/view_eligible_courses", methods=['POST'])
def view_eligible_courses():
    data = request.get_json()
    completed_courses = []
    eligible_courses = []
    non_eligible_courses = []
    all_courses = {}
    final_result = {"eligible":[],"non_eligible":[]}
    try:
        #retrieve all completed course by EID
        completed_courses_retrieved = Academic_record.query.filter_by(EID=data["EID"], status="completed")
        completed_courses = [course.json()['CID'] for course in completed_courses_retrieved]
        all_courses_retrieved = Course.query.all()
        for course in all_courses_retrieved:
            all_courses[course.json()['CID']] = course.list_of_prerequisites()
        
        for key in all_courses.keys():
            fail = False
            if key not in completed_courses:
                for value in all_courses[key]:
                    if value == '':
                        continue
                    if value not in all_courses:
                        fail = True
                if fail == False:
                    eligible_courses.append(key)

        for course in all_courses:
            if course not in eligible_courses:
                non_eligible_courses.append(course)
        
        for course in all_courses_retrieved:
            if course.json()['CID'] in eligible_courses:
                final_result['eligible'].append(course.json())
            else:
                final_result['non_eligible'].append(course.json())

        return jsonify(
            {
                "message": "Eligible and non-eligible courses are retrieved",
                "data": final_result
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "message": "There are no course retrieved"
            }
        ), 500


#create course and add in the prerequisties
@app.route("/create_course", methods=['POST'])
def create_course():
    data = request.get_json()
    if "name" not in data.keys():
        return jsonify(
        {
            "message": "Course name is not inserted successfully into the database",
        }
    ), 500
    try:
        course = Course(CID=data["CID"], name=data["name"], prerequisites=data["prerequisites"])
        db.session.add(course)
        db.session.commit()
        return jsonify(
            {
                "message": f"{data['name']} has been inserted successfully into the database",
                "data": course.to_dict()
            }
        ), 200

    except Exception as e:
        return jsonify(
        {
            "message": f"{data['name']} is not inserted successfully into the database",
        }
    ), 500


# #query specific course detail using CID. Usually used to query the pre-requisties
@app.route("/query_course", methods=['POST'])
def query_course():
    data = request.get_json()
    if "CID" not in data.keys():
        return jsonify(
        {
            "message": "CID is missing",
        }
    ), 500
    try:
        course = Course.query.filter_by(CID=data["CID"]).first()
        return jsonify(
        {
            "message": f"{data['CID']} has been query successfully from the database",
            "data": course.to_dict()
        }
    ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"{data['CID']} cannot be query",
        }
    ), 500


# update course name detail
@app.route("/update_course_name", methods=['POST'])
def update_course_name():
    data = request.get_json()
    if "CID" not in data.keys():
        return jsonify(
        {
            "message": "CID is missing",
        }
        ), 500
    try:
        course = Course.query.filter_by(CID=data["CID"])
        course.update(dict(name=data['name']))
        course = Course.query.filter_by(CID=data["CID"]).first()
        db.session.commit()
        return jsonify(
        {
            "message": f"{data['CID']} name has been updated successfully in the database",
            "data": course.to_dict()
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"{data['CID']} name is not updated",
        }
    ), 500

# update course prequisties
@app.route("/update_course_prerequisites", methods=['POST'])
def update_course_prerequisites():
    data = request.get_json()
    if "CID" not in data.keys():
        return jsonify(
        {
            "message": "CID is missing",
        }
        ), 500
    try:
        course = Course.query.filter_by(CID=data["CID"])
        course.update(dict(prerequisites=data['prerequisites']))
        course = Course.query.filter_by(CID=data["CID"]).first()
        db.session.commit()
        return jsonify(
        {
            "message": f"{data['CID']} prerequisites has been updated successfully in the database",
            "data": course.to_dict()
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"{data['CID']} prerequisites is not updated"
        }
    ), 500


# #delete course by course_name (can be changed)
@app.route("/delete_course", methods=['POST'])
def delete_course():
    data = request.get_json()
    if "CID" not in data.keys():
        return jsonify(
        {
            "message": "CID is missing",
        }
        ), 500
    try:
        course = Course.query.filter_by(CID=data["CID"])
        if course.first()==None:
            return jsonify(
            {
                "message": f"{data['CID']} is not deleted"
            }),500
        course.delete()
        db.session.commit()
        return jsonify(
        {
            "message": f"{data['CID']} has been deleted successfully from the database"
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"{data['CID']} is not deleted"
        }
    ), 500
### End of API points for Course CRUD ###

### Start of API points for Registration functions ###
@app.route("/engineer_signup", methods=['POST'])
def engineer_signup():
    data = request.get_json()
    expected=["EID", "CID", "SID"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Enrollment {not_present} is not present,  engineer is not enrolled"
            }
        ), 500
    try:
        enrollment = Enrollment(EID = data['EID'], SID = data['SID'], CID = data['CID'])
        db.session.add(enrollment)
        db.session.commit()
        return jsonify(
        {
            "message": f"{data['EID']} engineer has been updated successfully in the database",
            "data": enrollment.to_dict()
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"{data['EID']} engineer is not updated",
        }
    ), 500    


@app.route("/hr_view_signup", methods=['GET'])
def hr_view_signup():
    retrieved_signups = Enrollment.query.all()
    enrolls = [enroll.to_dict() for enroll in retrieved_signups]
    if enrolls:
        return jsonify(
            {
                "message": "All enrollments are retrieved",
                "data": enrolls
            }
        ), 200
    return jsonify(
        {
            "message": "There are no enrollment retrieved"
        }
    ), 500



@app.route("/hr_assign_engineer", methods=['POST'])
def hr_assign_engineer():
    data = request.get_json()
    expected=["EID", "CID", "SID", "QID"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"academic record {not_present} is not present,  engineer is not assigned"
            }
        ), 500
    try:
        academic_record = Academic_record(EID = data["EID"], SID = data["SID"], CID = data["CID"], QID = data["QID"], status = "ongoing", quiz_result = 0)
        db.session.add(academic_record)
        db.session.commit()

        return jsonify(
            {
                "message": f"{data['EID']} has been inserted successfully into the course details",
                "data": academic_record.to_dict()
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"{data['EID']} is not inserted successfully into the course details",
        }
    ), 500


@app.route("/hr_withdraw_engineer", methods=['POST'])
def hr_withdraw_engineer():
    data = request.get_json()
    expected=["EID", "CID", "SID"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"academic_record {not_present} is not present, engineer is not withdrawn"
            }
        ), 500
    try:
        exist = (Academic_record.query.filter_by(EID = data["EID"], SID = data["SID"], CID = data["CID"]).first() != None)
        if exist:
            Academic_record.query.filter_by(EID = data["EID"], SID = data["SID"], CID = data["CID"]).delete()
            db.session.commit()
            return jsonify(
                {
                    "message": f"{data['EID']} has been deleted successfully from course details",
                }
            ), 200
        else:
            return jsonify(
                {
                    "message": f"academic_record {data['EID']} is not present in database, engineer is not withdrawn",
                }), 500
    except Exception as e:
        return jsonify(
        {
            "message": f"{data['EID']} is not deleted"
        }
    ), 500    


@app.route("/hr_approve_signup", methods=['POST'])
def hr_approve_signup():
    data = request.get_json()
    expected=["EID", "CID", "SID", "QID"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Academic record {not_present} is not present, engineer is not enrolled"
            }
        ), 500
    try:
        exist = (Enrollment.query.filter_by(EID = data['EID'], SID = data['SID'], CID = data['CID']).first() != None)
        if exist:
            academic_record = Academic_record(EID = data['EID'], SID = data['SID'], CID = data['CID'], QID = data['QID'], status = "ongoing", quiz_result = 0)
            Enrollment.query.filter_by(EID = data['EID'], SID = data['SID'], CID = data['CID']).delete()
            db.session.add(academic_record)
            db.session.commit()
            return jsonify(
                {
                    "message": f"{data['EID']} prerequisites has been moved successfully from Enrollment to academic_record",
                    "data": academic_record.to_dict()
                }
            ), 200
        else:
            return jsonify(
                {
                    "message": f"Academic record {data['EID']} is not present, engineer is not enrolled",
                }), 500

    except Exception as e:
        return jsonify(
        {
            "message": f"{data['EID']} prerequisites is not moved successfully"
        }
    ), 500



@app.route("/hr_reject_signup", methods=['POST'])
def hr_reject_signup():
    data = request.get_json()
    expected=["EID", "CID", "SID"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Academic record {not_present} is not present, signup is not rejected"
            }
        ), 500
    try:
        exist = (Enrollment.query.filter_by(EID = data['EID'], SID = data['SID'], CID = data['CID']).first() != None)
        if exist :
            Enrollment.query.filter_by(EID = data['EID'], SID = data['SID'], CID = data['CID']).delete()
            db.session.commit()
            return jsonify(
            {
                "message": f"{data['EID']} has been deleted successfully from Enrollment"
            }
            ), 200
        else:
            return jsonify(
                {
                    "message": f"Enrollment {data['EID']} is not present in database,  engineer is not rejected",
                }), 500
    except Exception as e:
        return jsonify(
        {
            "message": f"{data['EID']} is not deleted"
        }
    ), 500



@app.route("/hr_assign_trainer", methods=['POST'])
def hr_assign_trainer():
    data = request.get_json()
    expected=["CID", "TID"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Course {not_present} is not present, trainer is not assigned"
            }
        ), 500
    try:
        course = db.session.query(Course).get(data['CID'])
        if len(course.trainers) == 0:
            course.trainers = data['TID']
        else:
            current_trainer = course.trainers.split(',')
            if data['TID'] not in current_trainer:
                course.trainers = course.trainers +','+ data['TID']
            else:
                return jsonify(
                {
                    "message": f"Trainers {data['TID']} is already in database"
                }
            ), 500
            
        db.session.commit()
        return jsonify(
        {
           "message": f"Trainers {data['TID']} has been updated successfully in the database",
           "data": course.to_dict()
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Trainers {data['TID']} are not updated"
        }
    ), 500
    ### End of API points for Registration functions ###
    
    
    ### Start of API points for Section CRUD ###
@app.route("/view_sections", methods=['POST'])
#view all sections by using TID
def view_all_sections():
    data = request.get_json()
    if "TID" not in data.keys():
        return jsonify(
        {
            "message": "TID is not found"
        }
    ), 500
    retrieved_sections = Section.query.filter_by(TID = data['TID'])
    sections = [section.to_dict() for section in retrieved_sections]
    if sections:
        return jsonify(
            {
                "message": f"All sections are retrieved for Trainer's ID {data['TID']}",
                "data": sections
            }
        ), 200
    return jsonify(
        {
            "message": "There are no sections retrieved"
        }
    ), 500

#create section and add in the prerequisties
@app.route("/create_section", methods=['POST'])
def create_section():
    data = request.get_json()
    required_keys = ["CID","SID","start","end","TID"]
    missing_keys = []
    for key in required_keys:
        if key not in data.keys():
            missing_keys.append(key)
    if len(missing_keys) > 0:
        missing_keys_string = ','.join(missing_keys)
        return jsonify(
        {
            "message": f"{missing_keys_string} not found"
        }
        ), 500

    try:
        date_object_start = datetime.strptime(data["start"], "%d/%m/%Y %H:%M:%S")
        date_object_end = datetime.strptime(data["end"], "%d/%m/%Y %H:%M:%S")
        section = Section(SID=data["SID"], CID=data["CID"], start=date_object_start, end=date_object_end, vacancy=data["vacancy"], TID=data["TID"])
        db.session.add(section)
        db.session.commit()
        return jsonify(
            {
                "message": f"Section {data['SID']} has been inserted successfully into the database",
                "data": section.to_dict()
            }
        ), 200

    except Exception as e:
        return jsonify(
        {
            "message": f"Section {data['SID']} is not inserted successfully into the database",
            'error':e
        }
    ), 500


# query specific section detail using CID.
@app.route("/query_section", methods=['POST'])
def query_section():
    data = request.get_json()
    if "CID" not in data.keys():
        return jsonify(
            {
                "message": "Section cannot be query"
            }), 500
    try:
        retrieved_section = Section.query.filter_by(CID=data["CID"])
        sections = [section.to_dict() for section in retrieved_section]
        if len(sections) == 0:
            return jsonify(
            {
                "message": "Section cannot be query"
            }), 500
        return jsonify(
        {
            "message": f"{data['CID']} has been query successfully from the database",
            "data": sections
        }
    ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Section cannot be query",
        }
    ), 500


# update section detail
@app.route("/update_section", methods=['POST'])
def update_section_detail():
    data = request.get_json()
    required_keys = ["SID","CID","start", "end", "vacancy", "TID"]
    missing_keys = []
    for key in required_keys:
        if key not in data.keys():
            missing_keys.append(key)
    if len(missing_keys) > 0:
        missing_keys_string = ','.join(missing_keys)
        return jsonify(
        {
            "message": f"{missing_keys_string} not found"
        }
        ), 500
    try:
        # Convert to datetime format
        data['start'] = datetime.strptime(data['start'], "%d/%m/%Y %H:%M:%S")
        data['end'] = datetime.strptime(data['end'], "%d/%m/%Y %H:%M:%S")

        #Retrieve data and then update it with updated details
        section = Section.query.filter_by(SID=data["SID"], CID=data["CID"], start=data["start"])

        section.update(dict(SID=data['SID'],CID=data['CID'],start=data['start'],end=data['end'],vacancy=data['vacancy'],TID=data['TID']))
        db.session.commit()
        section = Section.query.filter_by(SID=data["SID"], CID=data["CID"], start=data["start"]).first()

        
        return jsonify(
        {
            "message": f"Section {data['SID']}'s details have been updated successfully in the database",
            "data": section.to_dict()
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": "Section is not found"
        }
    ), 500


# #delete section by section_name (can be changed)
@app.route("/delete_section", methods=['POST'])
def delete_section():
    data = request.get_json()
    required_keys = ["SID","CID","start"]
    missing_keys = []
    for key in required_keys:
        if key not in data.keys():
            missing_keys.append(key)
    if len(missing_keys) > 0:
        missing_keys_string = ','.join(missing_keys)
        return jsonify(
        {
            "message": f"{missing_keys_string} not found"
        }
        ), 500
    try:
        data['start'] = datetime.strptime(data['start'], "%d/%m/%Y %H:%M:%S")
        Section.query.filter_by(SID=data["SID"], CID=data["CID"], start=data["start"]).delete()
        db.session.commit()
        return jsonify(
        {
            "message": f"Section {data['SID']} has been deleted successfully from the database"
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Section {data['SID']} is not deleted"
        }
    ), 500
### End of API points for Section CRUD ###

### Start of API point for material CRUD ###
#create section material
@app.route("/create_material", methods=['POST'])
def create_material():
    data = request.get_json()
    expected=["SID", "CID", "QID", "content_name", "content_type", "link"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Section content {not_present} is not present, section content is not inserted successfully into the database"
            }
        ), 500
    try:
        section_content = Section_content(SID=data["SID"], CID=data["CID"], QID=data["QID"], content_name=data["content_name"], content_type=data["content_type"], link=data["link"])
        db.session.add(section_content)
        db.session.commit()
        return jsonify(
            {
                "message": f"Section {data['content_name']} has been inserted successfully into the database",
                "data": section_content.to_dict()
            }
        ), 200

    except Exception as e:
        return jsonify(
        {
            "message": f"Section {data['content_name']} is not inserted successfully into the database"
        }
    ), 500

#read section content
@app.route("/view_section_content", methods=['POST'])
#view all sections by using SID, CID
def view_section_content():
    data = request.get_json()
    expected=["SID", "CID"]
    not_present=list()
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Section content {not_present} is not present, no section content is retrieved from database"
            }
        ), 500
    retrieved_section_content = Section_content.query.filter_by(SID = data['SID'], CID = data['CID'])
    section_contents = [section_content.to_dict() for section_content in retrieved_section_content]
    if section_contents:
        return jsonify(
            {
                "message": f"All sections content are retrieved for section {data['CID'], ' ', data['SID']}",
                "data": section_contents
            }
        ), 200
    return jsonify(
        {
            "message": "There are no section content retrieved"
        }
    ), 500

#update section content
@app.route("/update_section_content", methods=['POST'])
def update_section_content():
    data = request.get_json()
    expected=["old_SID", "old_CID", "old_QID", "old_content_name", "old_content_type", "old_link"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Section content {not_present} is not present, section content is not inserted successfully into the database"
            }
        ), 500
    potential_changes=["SID", "CID", "QID", "content_name", "content_type", "link"]
    for change in potential_changes:
        if change not in data.keys():
            data[change] = data[str('old_'+change)]
    try:
        section_content = Section_content(SID=data["SID"], CID=data["CID"], QID=data["QID"], content_name=data["content_name"], content_type=data["content_type"], link=data["link"])
        db.session.add(section_content)
        db.session.commit()
        Section_content.query.filter_by(SID = data["old_SID"], CID = data["old_CID"], content_name = data["old_content_name"]).delete()
        db.session.commit()
        return jsonify(
        {
            "message": f"Section content {data['old_CID'], data['old_SID'], data['content_name']}'s details have been updated successfully in the database",
            "data": section_content.to_dict()
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Section {data['old_CID'], data['old_SID'], data['content_name']} is not updated"
        }
    ), 500


#delete section content
@app.route("/delete_section_content", methods=['POST'])
def delete_section_content():
    data = request.get_json()
    expected=["SID", "CID", "content_name"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Section content {not_present} is not present, section content is not successfully deleted"
            }
        ), 500
    try:
        Section_content.query.filter_by(SID = data["SID"], CID = data["CID"], content_name = data["content_name"]).delete()
        db.session.commit()
        return jsonify(
        {
            "message": f"Section content { data['CID'], data['SID'], data['content_name']} has been deleted successfully from the database"
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Section {data['CID'], data['SID'], data['content_name']} is not deleted"
        }
    ), 500

### End of API points for Material CRUD ###


### Start of API point for lesson CRUD ###
#view all lessons
@app.route("/view_lessons", methods=['GET'])
def view_all_lessons():
    retrieved_lessons = Lesson.query.all()
    lessons = [lesson.to_dict() for lesson in retrieved_lessons]
    if lessons:
        return jsonify(
            {
                "message": "All lessons are retrieved",
                "data": lessons
            }
        ), 200
    return jsonify(
        {
            "message": "There are no lesson retrieved"
        }
    ), 500

# query specific lessons detail using SID & CID
@app.route("/query_lessons", methods=['POST'])
def query_lessons():
    data = request.get_json()

    try:
        retrieved_lessons = Lesson.query.filter_by(SID=data['SID'] ,CID=data["CID"])

        lessons = [lesson.to_dict() for lesson in retrieved_lessons]

        if len(lessons) == 0:
            return jsonify(
            {
                "message": "Lessons cannot be query"
            }), 500

        return jsonify(
        {
            "message": "Lessons have been query successfully from the database",
            "data": lessons
        }
        ), 200

    except Exception as e:
        return jsonify(
        {
            "message": "Lessons cannot be query"
        }
    ), 500

#create lesson
@app.route("/create_lesson", methods=['POST'])
def create_lesson():
    data = request.get_json()
    try:
        lesson = Lesson(LID=data["LID"], SID=data["SID"], CID=data["CID"])
        db.session.add(lesson)
        db.session.commit()
        return jsonify(
            {
                "message": "Lesson has been inserted successfully into the database",
                "data": lesson.to_dict()
            }
        ), 200

    except Exception as e:
        return jsonify(
        {
            "message": "Lesson is not inserted successfully into the database"
        }
    ), 500


### End of API point for lesson CRUD ###


### Start of API points for Ungraded Quiz CRUD ###
#create ungraded quiz and add it in the ungraded quiz table
@app.route("/create_ungraded_quiz_question", methods=['POST'])
def create_ungraded_quiz():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID', 'question', 'answer', 'options', 'duration']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, ungraded quiz question creation failed",
            }
        ), 500
    try:
        ungraded_quiz = Ungraded_quiz(CID=data["CID"], LID=data["LID"], SID=data["SID"], question=data["question"], 
                                    answer=data["answer"], options=data["options"], duration=data["duration"])
        db.session.add(ungraded_quiz)
        db.session.commit()
        return jsonify(
            {
                "message": f"Ungraded quiz question, {data['question']} ,has been inserted successfully into the database",
                "data": ungraded_quiz.to_dict()
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
    ), 500


#Read/get all the questions from a specific ungraded quiz
@app.route("/read_ungraded_quiz", methods=['POST'])
def read_ungraded_quiz():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, ungraded quiz read failed",
            }
        ), 500
    try:
        quiz_questions = Ungraded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"])
        all_questions = [question.to_dict() for question in quiz_questions]
        if len(all_questions) == 0:
            return jsonify(
            {
                "message": f"Quiz with CID {data['CID']} LID {data['LID']} SID {data['SID']} does not exist in database",
            }
        ), 500
        return jsonify(
            {
                "message": f"Quiz with CID {data['CID']}, LID {data['LID']}, SID {data['SID']} has been retrieved",
                "data": all_questions
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
    ), 500


#Read/get a specific question from a specific ungraded quiz
@app.route("/read_ungraded_quiz_question", methods=['POST'])
def read_ungraded_quiz_question():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID', 'question']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, ungraded quiz question read failed",
            }
        ), 500
    try:
        quiz_question = Ungraded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"], question=data["question"])
        question = quiz_question.first()
        if question == None:
            return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with CID {data['CID']} LID {data['LID']} SID {data['SID']} does not exist in database",
            }
        ), 500
        return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with CID {data['CID']}, LID {data['LID']}, SID {data['SID']} has been retrieved",
                "data": question.to_dict()
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
    ), 500


#Update a question from a specific ungraded quiz
'''primary keys cant be updated, only fields that needs to be updated will be sent over'''
@app.route("/update_ungraded_quiz_question", methods=['POST'])
def update_ungraded_quiz_question():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID', 'question']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, ungraded quiz update failed",
            }
        ), 500
    try:
        question = Ungraded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"], question=data["question"])
        possible_update_columns = ['answer', 'options', 'duration']
        if 'answer' in data.keys():
            question.update(dict(answer=data['answer']))
            db.session.commit()
        if 'options' in data.keys():
            question.update(dict(options=data['options']))
            db.session.commit()
        if 'duration' in data.keys():
            question.update(dict(options=data['duration']))
            db.session.commit()
        question = Ungraded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"], question=data["question"]).first()
        return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' has been updated",
                "data": question.json()
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
    ), 500


#Delete an ungraded quiz from database
@app.route("/delete_ungraded_quiz", methods=['POST'])
def delete_ungraded_quiz():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, ungraded quiz deletion failed",
            }
        ), 500
    try:
        quiz_questions = Ungraded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"])
        all_questions = [question.to_dict() for question in quiz_questions]
        if len(all_questions) == 0:
            return jsonify(
            {
                "message": f"Quiz with the CID {data['CID']} LID {data['LID']} SID {data['SID']} does not exist in the database",
            }
        ), 500
        quiz_questions.delete()
        db.session.commit()
        return jsonify(
            {
                "message": f"Quiz with the CID {data['CID']} LID {data['LID']} SID {data['SID']} has been deleted successfully",
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
        ), 500
    

#Delete an ungraded quiz question from database
@app.route("/delete_ungraded_quiz_question", methods=['POST'])
def delete_ungraded_quiz_question():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID', 'question']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, ungraded quiz question deletion failed",
            }
        ), 500
    try:
        quiz_question = Ungraded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"], question=data["question"])
        question = quiz_question.first()
        if question == None:
            return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with the CID {data['CID']} LID {data['LID']} SID {data['SID']} does not exist in the database",
            }
        ), 500
        quiz_question.delete()
        db.session.commit()
        return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with the CID {data['CID']} LID {data['LID']} SID {data['SID']} has been deleted successfully",
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
        ), 500
### End of API points for Ungraded Quiz CRUD ###

### Start of API points for Graded Quiz CRUD ###
#create graded quiz and add it in the graded quiz table
@app.route("/create_graded_quiz_question", methods=['POST'])
def create_graded_quiz():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID', 'question', 'answer', 'options', 'duration']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, graded quiz question creation failed",
            }
        ), 500
    try:
        graded_quiz = Graded_quiz(CID=data["CID"], LID=data["LID"], SID=data["SID"], question=data["question"], 
                                    answer=data["answer"], options=data["options"], duration=data["duration"])
        db.session.add(graded_quiz)
        db.session.commit()
        return jsonify(
            {
                "message": f"Graded quiz question, {data['question']} ,has been inserted successfully into the database",
                "data": graded_quiz.to_dict()
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
    ), 500


#Read/get all the questions from a specific graded quiz
@app.route("/read_graded_quiz", methods=['POST'])
def read_graded_quiz():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, graded quiz read failed",
            }
        ), 500
    try:
        quiz_questions = Graded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"])
        all_questions = [question.to_dict() for question in quiz_questions]
        if len(all_questions) == 0:
            return jsonify(
            {
                "message": f"Quiz with CID {data['CID']} LID {data['LID']} SID {data['SID']} does not exist in database",
            }
        ), 500
        return jsonify(
            {
                "message": f"Quiz with CID {data['CID']}, LID {data['LID']}, SID {data['SID']} has been retrieved",
                "data": all_questions
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
    ), 500


#Read/get a specific question from a specific graded quiz
@app.route("/read_graded_quiz_question", methods=['POST'])
def read_graded_quiz_question():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID', 'question']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, graded quiz question read failed",
            }
        ), 500
    try:
        quiz_question = Graded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"], question=data["question"])
        question = quiz_question.first()
        if question == None:
            return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with CID {data['CID']} LID {data['LID']} SID {data['SID']} does not exist in database",
            }
        ), 500
        return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with CID {data['CID']}, LID {data['LID']}, SID {data['SID']} has been retrieved",
                "data": question.to_dict()
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
    ), 500


#Update a question from a specific graded quiz
'''primary keys cant be updated, only fields that needs to be updated will be sent over'''
@app.route("/update_graded_quiz_question", methods=['POST'])
def update_graded_quiz_question():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID', 'question']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, graded quiz update failed",
            }
        ), 500
    try:
        question = Graded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"], question=data["question"])
        possible_update_columns = ['answer', 'options', 'duration']
        if 'answer' in data.keys():
            question.update(dict(answer=data['answer']))
            db.session.commit()
        if 'options' in data.keys():
            question.update(dict(options=data['options']))
            db.session.commit()
        if 'duration' in data.keys():
            question.update(dict(duration=data['duration']))
            db.session.commit()
        question = Graded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"], question=data["question"]).first()
        return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' has been updated",
                "data": question.json()
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
    ), 500


#Delete an graded quiz from database
@app.route("/delete_graded_quiz", methods=['POST'])
def delete_graded_quiz():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, graded quiz deletion failed",
            }
        ), 500
    try:
        quiz_questions = Graded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"])
        all_questions = [question.to_dict() for question in quiz_questions]
        if len(all_questions) == 0:
            return jsonify(
            {
                "message": f"Quiz with the CID {data['CID']} LID {data['LID']} SID {data['SID']} does not exist in the database",
            }
        ), 500
        quiz_questions.delete()
        db.session.commit()
        return jsonify(
            {
                "message": f"Quiz with the CID {data['CID']} LID {data['LID']} SID {data['SID']} has been deleted successfully",
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
        ), 500
    

#Delete an graded quiz question from database
@app.route("/delete_graded_quiz_question", methods=['POST'])
def delete_graded_quiz_question():
    data = request.get_json()
    fields = ['CID', 'LID', 'SID', 'question']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, graded quiz question deletion failed",
            }
        ), 500
    try:
        quiz_question = Graded_quiz.query.filter_by(CID=data["CID"], LID=data["LID"], SID=data["SID"], question=data["question"])
        question = quiz_question.first()
        if question == None:
            return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with the CID {data['CID']} LID {data['LID']} SID {data['SID']} does not exist in the database",
            }
        ), 500
        quiz_question.delete()
        db.session.commit()
        return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with the CID {data['CID']} LID {data['LID']} SID {data['SID']} has been deleted successfully",
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
        ), 500
### End of API points for Graded Quiz CRUD ###


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)