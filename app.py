from flask import Flask
from sqlalchemy import create_engine
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marks.db'
db = SQLAlchemy(app)
db.create_all()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    marks = db.relationship('Mark', backref='student', lazy='dynamic')

    def __repr__(self):
        return 'Student {}'.format(self.name)


class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discipline = db.Column(db.String(80))
    mark = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return 'Student {} got {} in {}'.format(self.student_id, self.mark,
                                                self.discipline)
