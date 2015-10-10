from grades import db

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

