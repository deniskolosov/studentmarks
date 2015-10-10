from flask import url_for, request, redirect, render_template
from sqlalchemy.sql import func
from wtforms import Form, StringField, SelectField, validators
from flask.ext.sqlalchemy import SQLAlchemy

from grades.models import Discipline, Student, Grade
from grades import app
from grades import db


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
        if Student.query.filter_by(name=form.name.data).first() is not None:
            s = Student.query.filter_by(name=form.name.data).first()
        else:
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
        for d in all_grades if len(d) > 0]
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
