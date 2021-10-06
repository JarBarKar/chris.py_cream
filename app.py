
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

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
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)