from flask import Flask, url_for, request, redirect
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from wtforms import Form, StringField, SelectField, validators


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.db'
app.secret_key = "mysecret"
db = SQLAlchemy(app)
db.create_all()


# MODELS
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return 'Student {}'.format(self.name)


class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return self.name


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.Integer, db.ForeignKey('student.id'))
    discipline = db.Column(db.Integer, db.ForeignKey('discipline.id'))
    discipline_related = db.relationship('Discipline',
                                         backref=db.backref('grades',
                                                            lazy='dynamic'))
    student_related = db.relationship('Student',
                                      backref=db.backref('grades',
                                                         lazy='dynamic'))
    grade = db.Column(db.Integer)

    def __repr__(self):
        return "Student {} got {} at {}".format(self.student_related.name,
                                                self.grade,
                                                self.discipline_related.name)


# VIEWS
class StudentForm(Form):
    name = StringField('Name', [validators.Length(max=120)])
    discipline = SelectField('Discipline', coerce=int)
    grade = SelectField('Grade', choices=[(1, '1'), (2, '2'), (3, '3'),
                                          (4, '4'), (5, '5')], coerce=int)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentForm(request.form)
    form.discipline.choices = [(d.id, d.name) for d in Discipline.query.all()]
    grades = Grade.query.all()
    print(grades)
    if request.method == 'POST' and form.validate():
        s = Student(name=form.name.data)
        db.session.add(s)
        db.session.commit()
        g = Grade(student=s.id,
                  discipline=form.discipline.data,
                  grade=form.grade.data)
        db.session.add(g)
        db.session.commit()
        return redirect(url_for('index'))

    # Avg grades for all
    avg_grades = db.session.query(func.avg(Grade.grade)).all()
    # Avg grade by subj
    all_grades = [d.grades.all() for d in Discipline.query.all()]
    avg_for_discipline = [
        (sum([gr.grade for gr in d])/len(d), d[0].discipline_related.name)
        for d in all_grades]
    # Avg by student
    students = Student.query.all()
    student_avg = [(sum([mark.grade
                         for mark in st.grades.all()])/len(st.grades.all()),
                    st.name) for st in students if len(st.grades.all()) > 0]

    return render_template('index.html',
                           form=form,
                           grades=grades,
                           avg_grades=avg_grades,
                           avg_for_discipline=avg_for_discipline,
                           student_avg=student_avg)

if __name__ == "__main__":
    app.run(debug=True)
