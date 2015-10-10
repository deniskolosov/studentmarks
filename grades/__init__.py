from flask import Flask, url_for, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.db'
app.secret_key = "mysecret"
db = SQLAlchemy(app)

import grades.views
import grades.models

from grades.models import Discipline

# Init database
db.drop_all()
db.create_all()
math = Discipline(name="Математика")
physics = Discipline(name="Физика")
lit = Discipline(name="Литература")
inf = Discipline(name="Информатика")
db.session.add_all([math,physics,lit,inf])
db.session.commit()
