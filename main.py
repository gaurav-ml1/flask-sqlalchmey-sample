import os
from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/demodb'

db = SQLAlchemy(app)
db.init_app(app)

class UserMixin:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(12), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

class Teacher(db.Model, UserMixin):
    subject = db.Column(db.String(250), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    department = db.Column(db.String(150), nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Student(db.Model, UserMixin):
    department = db.Column(db.String(150), nullable=True)
    address = db.Column(db.String(250), nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

class TeacherStudentMapModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

@app.route('/teacher', methods=['GET', 'POST', 'DELETE'])
def teacher():
    if request.method == "POST":
        requested_data = json.loads(request.data)
        teacher = Teacher(name=requested_data.get("name"), mobile=requested_data.get("mobile"), subject=requested_data.get("subject"))
        teacher.save()
        return jsonify({"status": True, "message": "Record has been created successfully"}), 201
    elif request.method == "GET":
        teachers = Teacher.query.all()
        output = []
        # we can make serializer also in seperate file
        for teacher in teachers:
            output.append({"teacher_id": teacher.id, "name": teacher.name, "mobile": teacher.mobile})
        return jsonify({"status": True, "result": output}), 200
    elif request.method == "DELETE":
        requested_data = json.loads(request.data)
        teacher = Teacher.query.get(requested_data.get("teacher_id"))
        # Hard delete but should soft delete
        # we can move inside model
        db.session.delete(teacher)
        db.session.commit()
        return jsonify({"status": True, "message": "Deleted"}), 200


@app.route('/student', methods=['GET', 'POST', 'DELETE'])
def stduent():
    if request.method == "POST":
        requested_data = json.loads(request.data)
        student = Student(name=requested_data.get("name"), mobile=requested_data.get("mobile"), department=requested_data.get("subject"))
        student.save()
        return jsonify({"status": True, "message": "Record has been created successfully"}), 201
    elif request.method == "GET":
        students = Student.query.all()
        output = []
        # we can make serializer also in seperate file
        for student in students:
            output.append({"student_id": student.id, "name": student.name, "mobile": student.mobile})
        return jsonify({"status": True, "result": output}), 200
    elif request.method == "DELETE":
        requested_data = json.loads(request.data)
        stduent = Student.query.get(requested_data.get("student_id"))
        # Hard delete but should soft delete
        # we can move inside model
        db.session.delete(stduent)
        db.session.commit()
        return jsonify({"status": True, "message": "Record Deleted"}), 200


@app.route('/assign', methods=['GET', 'POST', 'DELETE'])
def stduent_teacher_map():
    if request.method == "POST":
        requested_data = json.loads(request.data)
        student_teacher_obj = TeacherStudentMapModel(student=requested_data.get("student_id"), teacher=requested_data.get("teacher_id"))
        student_teacher_obj.save()
        return jsonify({"status": True, "message": "Record has been created successfully"}), 201
    else:
        teacher_id = request.args.get("teacher_id")
        print(teacher_id)
        students = TeacherStudentMapModel.query.filter_by(teacher=teacher_id)
        results = []
        for stduent in students:
            student_obj = Student.query.get(stduent.student)
            results.append({"name": student_obj.name})
        return jsonify(results)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8000", debug=True)
