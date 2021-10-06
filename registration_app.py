
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@127.0.0.1:3306/spm_lms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

# DB_declare

class Course(db.Model):
    __tablename__ = 'course'
    CID = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    prerequisites= db.Column(db.Integer(), nullable=True)
    trainer= db.Column(db.String(64), nullable=True)


    def __init__(self, CID, name, prerequisites, trainer):
        self.CID = CID
        self.name = name
        self.prerequisites = prerequisites
        self.trainer = trainer

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
        return {"CID": self.CID, "name": self.name, "prerequisites": self.prerequisites, "trainer": self.trainer}


class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    EID = db.Column(db.Integer(), nullable=False)
    SID = db.Column(db.String(64), nullable=False)
    CID = db.Column(db.String(64), nullable=False)


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



class Course_detail(db.Model):
    __tablename__ = 'course_detail'
    EID = db.Column(db.Integer(), nullable=False)
    SID = db.Column(db.String(64), nullable=False)
    CID = db.Column(db.String(64), nullable=False)
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


@app.route("/engineer_signup", methods=['POST'])
def engineer_signup():
    data = request.get_json()
    try:
        enrollment = Enrollment(EID = data.EID, SID = data.SID, CID = data.CID)
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
                "message": "All enrollment are retrieved",
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
        course_detail = Course_detail(EID = data.EID, SID = data.SID, CID = data.CID, status = "ongoing", quiz_result = 0)
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
        Course_detail.query.filter_by(EID = data.EID, SID = data.SID, CID = data.CID).delete()
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
        course_detail = Course_detail(EID = data.EID, SID = data.SID, CID = data.CID, status = "ongoing", quiz_result = 0)
        Enrollment.query.filter_by(EID = data.EID, SID = data.SID, CID = data.CID).delete()
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
        Enrollment.query.filter_by(EID = data.EID, SID = data.SID, CID = data.CID).delete()
        db.session.commit()
        return jsonify(
        {
            "message": f"{data['EID']} has been deleted successfully from Enrollment"
        }
        ), 200
    except Exception as e:
        return jsonify(e), 500

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
        course = Course.query.filter_by(CID = data.CID).first()
        course.trainer = course.trainer +','+ data.TID
        db.session.commit()
        return jsonify(
        {
            "message": f"{data['TID']} course trainer has been updated successfully in the database",
            "data": course.to_dict()
        }
        ), 200
    except Exception as e:
        return jsonify(
        {
            "message": f"{data['TID']} course trainer is not updated"
        }
    ), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)