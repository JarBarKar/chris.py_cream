
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@127.0.0.1:3306/spm_lms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

### Course Class ###
class Course(db.Model):
    __tablename__ = 'course'
    CID = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    prerequisites= db.Column(db.String(64), nullable=False)
    trainers = db.Column(db.String(64), nullable=False)


    def __init__(self, CID, name, prerequisites, trainers):
        self.CID = CID
        self.name = name
        self.prerequisites = prerequisites
        self.trainers = trainers

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
        "prerequisites": self.prerequisites,  "trainers": self.trainers}
### Course Class ###

### Course Detail Class ###
class Course_detail(db.Model):
    __tablename__ = 'course_detail'
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
### Course Detail Class ###

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
    
    def to_start_datetime(self):
        return datetime.strptime(self.start, "%d/%m/%Y %H:%M:%S")

    def to_end_datetime(self):
        return datetime.strptime(self.end, "%d/%m/%Y %H:%M:%S")

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


### Start of API points for Course CRUD ###
@app.route("/view_courses", methods=['GET'])
#view all courses
def view_all_courses():
    # data = request.get_json()
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

#create course and add in the prerequisties
@app.route("/create_course", methods=['POST'])
def create_course():
    data = request.get_json()
    try:
        course = Course(CID=data["CID"], name=data["name"], prerequisites=data["prerequisites"], trainers=data["trainers"])
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
    try:
        Course.query.filter_by(CID=data["CID"]).delete()
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
    try:
        course_detail = Course_detail(EID = data["EID"], SID = data["SID"], CID = data["CID"], QID = data["QID"], status = "ongoing", quiz_result = 0)
        db.session.add(course_detail)
        db.session.commit()

        return jsonify(
            {
                "message": f"{data['EID']} has been inserted successfully into the course details",
                "data": course_detail.to_dict()
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
    
    try:
        Course_detail.query.filter_by(EID = data["EID"], SID = data["SID"], CID = data["CID"]).delete()
        db.session.commit()
        return jsonify(
            {
                "message": f"{data['EID']} has been deleted successfully from course details",
            }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"{data['EID']} is not deleted"
        }
    ), 500    


@app.route("/hr_approve_signup", methods=['POST'])
def hr_approve_signup():
    data = request.get_json()
    try:
        course_detail = Course_detail(EID = data['EID'], SID = data['SID'], CID = data['CID'], QID = data['QID'], status = "ongoing", quiz_result = 0)
        Enrollment.query.filter_by(EID = data['EID'], SID = data['SID'], CID = data['CID']).delete()
        db.session.add(course_detail)
        db.session.commit()
        return jsonify(
        {
            "message": f"{data['EID']} prerequisites has been moved successfully from Enrollment to course_detail",
            "data": course_detail.to_dict()
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"{data['EID']} prerequisites is not moved successfully"
        }
    ), 500



@app.route("/hr_reject_signup", methods=['POST'])
def hr_reject_signup():
    data = request.get_json()
    try:
        Enrollment.query.filter_by(EID = data['EID'], SID = data['SID'], CID = data['CID']).delete()
        db.session.commit()
        return jsonify(
        {
            "message": f"{data['EID']} has been deleted successfully from Enrollment"
        }
        ), 200

    except Exception as e:
        return jsonify(
        {
            "message": f"{data['EID']} is not deleted"
        }
    ), 500



@app.route("/hr_assign_trainer", methods=['POST'])
def hr_assign_trainer():
    data = request.get_json()
    try:
        course = Course.query.filter_by(CID = data['CID']).first()
        course.trainer = course.trainer +','+ data['TID']
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
            "message": f"Section {data['SID']} is not inserted successfully into the database"
        }
    ), 500


# # #query specific section detail using CID. Usually used to query the pre-requisties
# @app.route("/query_section", methods=['POST'])
# def query_course():
#     data = request.get_json()
#     try:
#         course = Course.query.filter_by(CID=data["CID"]).first()
#         return jsonify(
#         {
#             "message": f"{data['CID']} has been query successfully from the database",
#             "data": course.to_dict()
#         }
#     ), 200
#     except Exception as e:
#         return jsonify(
#         {
#             "message": f"{data['CID']} cannot be query",
#         }
#     ), 500


# update section detail
@app.route("/update_section", methods=['POST'])
def update_section_detail():
    data = request.get_json()
    old_update_section = {}
    new_update_section = {}
    #split into old and new section
    for section_key, section_value in data.items():
        if section_key.split('_')[0] == 'old':
            old_update_section[section_key.split('_')[1]] = section_value
        else:
            new_update_section[section_key.split('_')[1]] = section_value
    try:
        #loop through the new_update_section, replace blank string with old values. New value will not be touched
        for section_key, section_value in new_update_section.items():
            if section_value == '':
                new_update_section = old_update_section[section_key]

        # Convert to datetime format
        old_update_section['start'] = datetime.strptime(old_update_section['start'], "%d/%m/%Y %H:%M:%S")
        old_update_section['end'] = datetime.strptime(old_update_section['end'], "%d/%m/%Y %H:%M:%S")
        new_update_section['start'] = datetime.strptime(new_update_section['start'], "%d/%m/%Y %H:%M:%S")
        new_update_section['end'] = datetime.strptime(new_update_section['end'], "%d/%m/%Y %H:%M:%S")

        #Retrieve old data and then update it with updated details
        section = Section.query.filter_by(SID=old_update_section["SID"], CID=old_update_section["CID"], start=old_update_section["start"])
        section.update(dict(SID=new_update_section['SID'],CID=new_update_section['CID'],start=new_update_section['start'],end=new_update_section['end'],vacancy=new_update_section['vacancy'],TID=new_update_section['TID']))
        db.session.commit()
        section = Section.query.filter_by(SID=new_update_section["SID"], CID=new_update_section["CID"], start=new_update_section["start"]).first()
        return jsonify(
        {
            "message": f"Section {old_update_section['SID']}'s details have been updated successfully in the database",
            "data": section.to_dict()
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"Section {old_update_section['CID']} is not updated"
        }
    ), 500


# #delete section by section_name (can be changed)
@app.route("/delete_section", methods=['POST'])
def delete_section():
    data = request.get_json()
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
            "message": f"Section {data['SID']} is not deleted",
            "error": e
        }
    ), 500
### End of API points for Section CRUD ###


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)