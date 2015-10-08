from flask import Flask
from flask import render_template
from sqlalchemy import create_engine
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, IntegerField, validators


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marks.db'
db = SQLAlchemy(app)
db.create_all()

student_to_discipline = db.Table('s_t_d',
        db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
        db.Column('disipline_id', db.Integer, db.ForeignKey('discipline.id'))
        )

# MODELS
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    studying = db.relationship('Discipline',
            secondary=student_to_discipline,
            backref=db.backref('studying', lazy='dynamic'))
    mark = db.Column(db.Integer)

    def __repr__(self):
        return 'Student {}'.format(self.name)

class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return self.name

# VIEWS
class StudentForm(Form):
    name = StringField('Name', [validators.Length(max=120)])
    discipline = StringField('Discipline', [validators.Length(max=80)])
    mark = IntegerField('Mark', [validators.NumberRange(min=1, max=5)]) 


@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentForm()
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
