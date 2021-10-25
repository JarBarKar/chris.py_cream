
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

print('lesgosaaaaaassaa')
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
        if self.prerequisites.split(',')[0] == '':
            return []
        else:
            return self.prerequisites.split(',')
### Course Class ###


### Academic record Class ###
class Academic_record(db.Model):
    __tablename__ = 'academic_record'
    EID = db.Column(db.Integer(), primary_key=True)
    SID = db.Column(db.String(64), primary_key=True)
    CID = db.Column(db.String(64), primary_key=True)
    start = db.Column(db.DateTime, nullable=False, primary_key=True)
    status = db.Column(db.String(64), nullable=False)


    def __init__(self, EID, SID, CID, start, status):
        self.EID = EID
        self.SID = SID
        self.CID = CID
        self.start = start
        self.status = status

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
        return {"EID": self.EID, "SID": self.SID, "CID": self.CID, "start": self.start, "status": self.status}
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
### Content Class ###
class Content(db.Model):
    __tablename__ = 'content'
    SID = db.Column(db.String(64), primary_key=True)
    CID = db.Column(db.String(64), primary_key=True)
    LID = db.Column(db.String(64), primary_key=True)
    start = db.Column(db.DateTime, nullable=False, primary_key=True)
    content_name = db.Column(db.String(64), primary_key=True)
    content_type = db.Column(db.String(64), nullable=False)
    link = db.Column(db.String(64), nullable=False)

    def __init__(self, SID, CID, LID, start, content_name, content_type, link):
        self.SID = SID
        self.CID = CID
        self.LID = LID
        self.start = start
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
        return {"SID": self.SID, "CID": self.CID, "LID": self.LID, "start": self.start, "content_type": self.content_type ,"content_name": self.content_name, "link": self.link}
### Content Class ###

### Lesson Class ###
class Lesson(db.Model):
    __tablename__ = 'lesson'
    LID = db.Column(db.String(64), primary_key=True)
    SID = db.Column(db.String(64), primary_key=True)
    CID = db.Column(db.String(64), primary_key=True)
    start = db.Column(db.DateTime, nullable=False, primary_key=True)

    
    def __init__(self, LID, SID, CID, start):
        self.LID = LID
        self.SID = SID
        self.CID = CID
        self.start = start


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
        return {"LID": self.LID, "SID": self.SID, "CID": self.CID, "start": self.start}
### Lesson Class ###

### Quiz Questions Class ###
class Quiz_questions(db.Model):
    __tablename__ = 'Quiz_questions'
    LID = db.Column(db.Integer(), primary_key=True)
    SID = db.Column(db.String(64), primary_key=True)
    CID = db.Column(db.String(64), primary_key=True)
    start = db.Column(db.DateTime, nullable=False, primary_key=True)
    question = db.Column(db.String(64), primary_key=True)
    answer = db.Column(db.String(64), nullable=False)
    options = db.Column(db.String(64), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.String(64), nullable=False)

    def __init__(self, LID, SID, CID, start, question, answer, options, duration, type):
        self.LID = LID
        self.SID = SID
        self.CID = CID
        self.start = start
        self.question = question
        self.answer = answer
        self.options = options
        self.duration = duration
        self.type = type


    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            if column == 'start':
                result[column] = str(getattr(self, column))
            else:
                result[column] = getattr(self, column)
        return result

    def json(self):
        return {"LID": self.LID, "SID": self.SID, "CID": self.CID, "start": self.start , "question": self.question,
                "answer":self.answer, "options":self.options, "duration":self.duration, "type": self.type}
### Quiz Questions Class ###


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

#view eligible courses by EID
@app.route("/view_eligible_courses", methods=['POST'])
def view_eligible_courses():
    data = request.get_json()
    completed_courses = []
    eligible_courses = []
    non_eligible_courses = []
    all_courses = {}
    final_result = {"eligible":[],"non_eligible":[]}

    if "EID" not in data.keys():
        return jsonify(
            {
                "message": "EID is missing"
            }
        ), 500

    try:
        #retrieve all completed course, ongoing course by EID
        completed_courses_retrieved = Academic_record.query.filter_by(EID=data["EID"], status="completed")
        ongoing_courses_retrieved = Academic_record.query.filter_by(EID=data["EID"], status="ongoing")
        completed_courses = [course.to_dict() for course in completed_courses_retrieved]
        ongoing_courses = [course.to_dict() for course in ongoing_courses_retrieved]

        all_courses_retrieved = Course.query.all()

        for course in all_courses_retrieved:
            all_courses[course.json()['CID']] = course.list_of_prerequisites()

        # If course is not in completed courses and on-going courses and fulfil the re-requisite, it is eligible
        # If course is either on-going or completed, it is not eligible
        for course, prerequisites in all_courses.items():
            if course not in [c_course["CID"] for c_course in completed_courses] and course not in [o_course["CID"] for o_course in ongoing_courses]:
                status = True
                for prereq in prerequisites:
                    if prereq not in [c_course["CID"] for c_course in completed_courses] and course not in [o_course["CID"] for o_course in ongoing_courses]:
                        status = False
                if status == True:
                    eligible_courses.append(course)


        for course in all_courses:
            if course not in eligible_courses:
                non_eligible_courses.append(course)
        
        for course in all_courses_retrieved:
            if course.json()['CID'] in eligible_courses:
                final_result['eligible'].append(course.json())
            else:
                final_result['non_eligible'].append(course.json())

        if final_result['eligible'] or final_result['non_eligible']:
            return jsonify(
                {
                    "message": "Eligible and non-eligible courses are retrieved",
                    "data": final_result
                }
            ), 200
        else:
            return jsonify(
                {
                    "message": "There are no course retrieved"
                }
            ), 500

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



# @app.route("/hr_assign_trainer", methods=['POST'])
# def hr_assign_trainer():
#     data = request.get_json()
#     expected=["CID", "TID"]
#     not_present=list()
#     #check input
#     for expect in expected:
#         if expect not in data.keys():
#             not_present.append(expect)
#     if len(not_present)>0:
#         return jsonify(
#             {
#                 "message": f"Course {not_present} is not present, trainer is not assigned"
#             }
#         ), 500
#     try:
#         course = db.session.query(Course).get(data['CID'])
#         if len(course.trainers) == 0:
#             course.trainers = data['TID']
#         else:
#             current_trainer = course.trainers.split(',')
#             if data['TID'] not in current_trainer:
#                 course.trainers = course.trainers +','+ data['TID']
#             else:
#                 return jsonify(
#                 {
#                     "message": f"Trainers {data['TID']} is already in database"
#                 }
#             ), 500
            
#         db.session.commit()
#         return jsonify(
#         {
#            "message": f"Trainers {data['TID']} has been updated successfully in the database",
#            "data": course.to_dict()
#         }
#         ), 200
#     except Exception as e:
#         return jsonify(
#         {
#             "message": f"Trainers {data['TID']} are not updated"
#         }
#     ), 500
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
    required_keys = ["CID","SID","start","end","TID", "vacancy"]
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
        date_object_start = datetime.fromisoformat(data["start"])
        date_object_end = datetime.fromisoformat(data["end"])
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
        date_object_start = datetime.fromisoformat(data["start"])
        date_object_end = datetime.fromisoformat(data["end"])

        #Retrieve data and then update it with updated details
        section = Section.query.filter_by(SID=data["SID"], CID=data["CID"], start=date_object_start)

        section.update(dict(SID=data['SID'],CID=data['CID'],start=date_object_start,end=date_object_end,vacancy=data['vacancy'],TID=data['TID']))

        db.session.commit()

        section = Section.query.filter_by(SID=data["SID"], CID=data["CID"], start=date_object_start).first()

        if section:
            return jsonify(
            {
                "message": f"Section {data['SID']}'s details have been updated successfully in the database",
                "data": section.to_dict()
            }
            ), 200
        else:
            return jsonify(
            {
                "message": "Section is not found",
            }
            ), 500

    except Exception as e:
        return jsonify(
        {
            "message": "Section is not found",
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
        date_object_start = datetime.fromisoformat(data["start"])
        section_query = Section.query.filter_by(SID=data["SID"], CID=data["CID"], start=date_object_start)
        if section_query.first():
            section_query.delete()
            db.session.commit()
            return jsonify(
            {
                "message": f"Section {data['SID']} has been deleted successfully from the database"
            }
            ), 200
        else:
            return jsonify(
            {
                "message": f"Section {data['SID']} is not deleted"
            }
            ), 500
        

    except Exception as e:
        return jsonify(
        {
            "message": f"Section {data['SID']} is not deleted"
        }
    ), 500
### End of API points for Section CRUD ###

### Start of API point for material CRUD ###
#create section material
@app.route("/create_content", methods=['POST'])
def create_content():
    data = request.get_json()
    expected=["SID", "CID", "LID", "start", "content_name", "content_type", "link"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Content {not_present} is not present, content is not inserted successfully into the database"
            }
        ), 500
    try:
        data['start'] = datetime.strptime(data['start'], "%d/%m/%Y %H:%M:%S")
        content = Content(SID=data["SID"], CID=data["CID"], LID=data["LID"], start=data["start"], content_name=data["content_name"], content_type=data["content_type"], link=data["link"])
        db.session.add(content)
        db.session.commit()
        return jsonify(
            {
                "message": f"Content {data['content_name']} has been inserted successfully into the database",
                "data": content.to_dict()
            }
        ), 200

    except Exception as e:
        return jsonify(
        {
            "message": f"Content {data['content_name']} is not inserted successfully into the database"
        }
    ), 500

#read section content
@app.route("/view_all_section_content", methods=['POST'])
#view all sections by using SID, CID
def view_all_section_content():
    data = request.get_json()
    expected=["SID", "CID", "start"]
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
    data['start'] = datetime.strptime(data['start'], "%d/%m/%Y %H:%M:%S")
    retrieved_section_content = Content.query.filter_by(SID = data['SID'], CID = data['CID'], start = data['start'])
    section_contents = [section_content.to_dict() for section_content in retrieved_section_content]
    if section_contents:
        return jsonify(
            {
                "message": f"All sections content are retrieved for section {data['CID'], data['SID']}",
                "data": section_contents
            }
        ), 200
    return jsonify(
        {
            "message": "There are no section content retrieved"
        }
    ), 500

#read lesson content
@app.route("/view_lesson_content", methods=['POST'])
#view all content by using SID, CID, LID
def view_lesson_content():
    data = request.get_json()
    expected=["SID", "CID", "LID", "start"]
    not_present=list()
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Content {not_present} is not present, no content is retrieved from database"
            }
        ), 500
    data['start'] = datetime.strptime(data['start'], "%d/%m/%Y %H:%M:%S")
    retrieved_content = Content.query.filter_by(SID = data['SID'], CID = data['CID'], LID = data['LID'], start = data['start'])
    contents = [content.to_dict() for content in retrieved_content]
    if contents:
        return jsonify(
            {
                "message": f"All content are retrieved for lesson {data['CID'], data['SID'], data['LID']}",
                "data": contents
            }
        ), 200
    return jsonify(
        {
            "message": "There are no content retrieved"
        }
    ), 500

#update content
@app.route("/update_content", methods=['POST'])
def update_content():
    data = request.get_json()
    expected=["old_SID", "old_CID", "old_LID", "old_start", "old_content_name", "old_content_type", "old_link"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Content {not_present} is not present, content is not inserted successfully into the database"
            }
        ), 500
    potential_changes=["SID", "CID", "LID", "start", "content_name", "content_type", "link"]
    for change in potential_changes:
        if change not in data.keys():
            data[change] = data[str('old_'+change)]
    data['start'] = datetime.strptime(data['start'], "%d/%m/%Y %H:%M:%S")
    data['old_start'] = datetime.strptime(data['old_start'], "%d/%m/%Y %H:%M:%S")
    exist = (Content.query.filter_by(SID = data["old_SID"], CID = data["old_CID"], LID = data["old_LID"], start = data["old_start"], content_name = data["old_content_name"]).first() != None)
    if exist:
        try:
            Content.query.filter_by(SID = data["old_SID"], CID = data["old_CID"], LID = data["old_LID"], start = data["old_start"], content_name = data["old_content_name"]).delete()
            content = Content(SID=data["SID"], CID=data["CID"], LID=data["LID"], start=data["start"], content_name=data["content_name"], content_type=data["content_type"], link=data["link"])
            db.session.add(content)
            db.session.commit()
            return jsonify(
            {
                "message": f"Content {data['old_CID'], data['old_SID'], data['old_LID'], data['content_name']}'s details have been updated successfully in the database",
                "data": content.to_dict()
            }
            ), 200

        except Exception as e:
            return jsonify(
            {
                "message": f"Content{data['old_CID'], data['old_SID'], data['old_LID'], data['old_content_name']} is not updated"
            }
        ), 500
    else:
        return jsonify(
        {
            "message": f"Content {data['old_CID'], data['old_SID'], data['old_LID'], data['old_content_name']} do not exist"
        }), 500



#delete content
@app.route("/delete_content", methods=['POST'])
def delete_content():
    data = request.get_json()
    expected=["SID", "CID", "LID", "start", "content_name"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Content {not_present} is not present, content is not successfully deleted"
            }
        ), 500
    data['start'] = datetime.strptime(data['start'], "%d/%m/%Y %H:%M:%S")
    exist = (Content.query.filter_by(SID = data["SID"], CID = data["CID"], LID = data["LID"], start = data["start"], content_name = data["content_name"]).first() != None)
    if exist:
        try:
            Content.query.filter_by(SID = data["SID"], CID = data["CID"], LID = data["LID"], start = data["start"], content_name = data["content_name"]).delete()
            db.session.commit()
            return jsonify(
            {
                "message": f"Content { data['CID'], data['SID'], data['LID'], data['content_name']} has been deleted successfully from the database"
            }
            ), 200
        except Exception as e:
            return jsonify(
            {
                "message": f"Content {data['CID'], data['SID'], data['LID'], data['content_name']} is not deleted"
            }
    ), 500
    else:
        return jsonify(
        {
            "message": f"Content {data['CID'], data['SID'], data['LID'], data['content_name']} do not exist"
        }), 500
    

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
    missing_input = []
    expected_input = ["LID","SID","CID","start"]
    for key in expected_input:
        if key not in data.keys():
            missing_input.append(key)
    if len(missing_input)>0:
        return jsonify(
            {
                "message": f"{','.join(missing_input)} is missing"
            }
        ), 500
    try:
        date_object_start = datetime.fromisoformat(data["start"])
        lesson = Lesson(LID=data["LID"], SID=data["SID"], CID=data["CID"], start=date_object_start)
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
            "message": "Lesson is not inserted successfully into the database",
            "e" : e
        }
    ), 500


#delete lesson
@app.route("/delete_lesson", methods=['POST'])
def delete_lesson():
    data = request.get_json()
    date_object_start = datetime.fromisoformat(data["start"])
    expected=["SID", "CID", "LID","start"]
    not_present=list()
    #check input
    for expect in expected:
        if expect not in data.keys():
            not_present.append(expect)
    if len(not_present)>0:
        return jsonify(
            {
                "message": f"Lesson {not_present} is not present, lesson is not successfully deleted"
            }
        ), 500
    exist = (Lesson.query.filter_by(SID = data["SID"], CID = data["CID"], LID = data["LID"], start=date_object_start).first() != None)
    if exist:
        try:
            Lesson.query.filter_by(SID = data["SID"], CID = data["CID"], LID = data["LID"], start=date_object_start).delete()
            db.session.commit()
            return jsonify(
            {
                "message": f"Lesson { data['CID'], data['SID'], data['LID'], data['start']} has been deleted successfully from the database"
            }
            ), 200
        except Exception as e:
            return jsonify(
            {
                "message": f"Lesson {data['CID'], data['SID'], data['LID'], data['start']} is not deleted"
            }
    ), 500
    else:
        return jsonify(
        {
            "message": f"Lesson {data['CID'], data['SID'], data['LID'], data['start']} do not exist"
        }), 500

### End of API point for lesson CRUD ###


### Start of API points for Quiz CRUD ###
#create quiz question and add it in the quiz questions table
@app.route("/create_quiz_question", methods=['POST'])
def create_quiz_question():
    data = request.get_json()
    fields = ['LID', 'SID', 'CID', 'start', 'question', 'answer', 'options', 'duration', 'type']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, quiz question creation failed",
            }
        ), 500
    data["start"] = datetime.fromisoformat(data["start"])
    try:
        quiz_question= Quiz_questions(LID=data["LID"], SID=data["SID"], CID=data["CID"], start=data["start"], question=data["question"], 
                                    answer=data["answer"], options=data["options"], duration=data["duration"], type=data["type"])
        db.session.add(quiz_question)
        db.session.commit()
        return jsonify(
            {
                "message": f"Quiz question, {data['question']} ,has been inserted successfully into the database",
                "data": quiz_question.to_dict()
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
    ), 500


#Read/get all the questions from a specific quiz
@app.route("/read_quiz", methods=['POST'])
def read_quiz():
    data = request.get_json()
    fields = ['LID', 'SID', 'CID', 'start']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, quiz read failed",
            }
        ), 500
    data["start"] = datetime.fromisoformat(data["start"])
    try:
        quiz_questions = Quiz_questions.query.filter_by(LID=data["LID"], SID=data["SID"], CID=data["CID"], start=data["start"])
        all_questions = [question.to_dict() for question in quiz_questions]
        if len(all_questions) == 0:
            return jsonify(
            {
                "message": f"Quiz with LID: {data['LID']}, SID: {data['SID']}, CID: {data['CID']}, start: {data['start']} does not exist in database",
            }
        ), 500
        return jsonify(
            {
                "message": f"Quiz with LID: {data['LID']}, SID: {data['SID']}, CID: {data['CID']}, start: {data['start']} has been retrieved",
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
@app.route("/read_quiz_question", methods=['POST'])
def read_quiz_question():
    data = request.get_json()
    fields = ['LID', 'SID', 'CID', 'start', 'question']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, quiz question read failed",
            }
        ), 500
    data["start"] = datetime.fromisoformat(data["start"])
    try:
        quiz_question = Quiz_questions.query.filter_by(LID=data["LID"], SID=data["SID"], CID=data["CID"], start=data["start"], question=data["question"])
        question = quiz_question.first()
        if question == None:
            return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with LID {data['LID']}, SID {data['SID']}, CID {data['CID']}, start {data['start']} does not exist in database",
            }
        ), 500
        return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with LID {data['LID']}, SID {data['SID']}, CID {data['CID']}, start {data['start']} has been retrieved",
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
@app.route("/update_quiz_question", methods=['POST'])
def update_quiz_question():
    data = request.get_json()
    fields = ['LID', 'SID', 'CID', 'start', 'question']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, quiz update failed",
            }
        ), 500
    data["start"] = datetime.fromisoformat(data["start"])
    try:
        question = Quiz_questions.query.filter_by(LID=data["LID"], SID=data["SID"], CID=data["CID"], start=data["start"], question=data["question"])
        if question.first() == None:
            return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with LID {data['LID']}, SID {data['SID']}, CID {data['CID']}, start {data['start']} does not exist in database",
            }
        ), 500
        # possible_update_columns = ['answer', 'options', 'duration', 'type']
        if 'answer' in data.keys():
            question.update(dict(answer=data['answer']))
            
        if 'options' in data.keys():
            question.update(dict(options=data['options']))
           
        if 'duration' in data.keys():
            question.update(dict(duration=data['duration']))
            
        if 'type' in data.keys():
            question.update(dict(type=data['type']))

        db.session.commit()
        question = Quiz_questions.query.filter_by(LID=data["LID"], SID=data["SID"], CID=data["CID"], start=data["start"], question=data["question"]).first()
        return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' has been updated",
                "data": question.to_dict()
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
    ), 500


#Delete a quiz from database
@app.route("/delete_quiz", methods=['POST'])
def delete_quiz():
    data = request.get_json()
    fields = ['LID', 'SID', 'CID', 'start']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, quiz deletion failed",
            }
        ), 500
    data["start"] = datetime.fromisoformat(data["start"])
    try:
        quiz_questions = Quiz_questions.query.filter_by(LID=data["LID"], SID=data["SID"], CID=data["CID"], start=data["start"])
        all_questions = [question.to_dict() for question in quiz_questions]
        if len(all_questions) == 0:
            return jsonify(
            {
                "message": f"Quiz with LID: {data['LID']}, SID: {data['SID']}, CID: {data['CID']}, start: {data['start']} does not exist in the database",
            }
        ), 500
        quiz_questions.delete()
        db.session.commit()
        return jsonify(
            {
                "message": f"Quiz with LID: {data['LID']}, SID: {data['SID']}, CID: {data['CID']}, start: {data['start']} has been deleted successfully",
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
        ), 500
    

#Delete a quiz question from database
@app.route("/delete_quiz_question", methods=['POST'])
def delete_quiz_question():
    data = request.get_json()
    fields = ['LID', 'SID', 'CID', 'start', 'question']
    for key in fields:
        if key not in data.keys():
            return jsonify(
            {
                "message": f"{key} is missing from request body, quiz question deletion failed",
            }
        ), 500
    data["start"] = datetime.fromisoformat(data["start"])
    try:
        quiz_question = Quiz_questions.query.filter_by(LID=data["LID"], SID=data["SID"],CID=data["CID"], start=data["start"], question=data["question"])
        question = quiz_question.first()
        if question == None:
            return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with LID: {data['LID']}, SID: {data['SID']}, CID: {data['CID']}, start: {data['start']} does not exist in the database",
            }
        ), 500
        quiz_question.delete()
        db.session.commit()
        return jsonify(
            {
                "message": f"Quiz question \'{data['question']}\' with LID: {data['LID']}, SID: {data['SID']}, CID: {data['CID']}, start: {data['start']} has been deleted successfully",
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Error! {e}",
        }
        ), 500
### End of API points for Quiz CRUD ###



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)