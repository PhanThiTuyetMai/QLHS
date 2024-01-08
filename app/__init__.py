from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '*(*dsg45654154+-+*/475698273!#$$$%)))'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:%s@localhost/qlhs?charset=utf8mb4" % quote(
    'Maiphan13082003')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 2

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name="duz2xltvs",
    api_key="557735761715113",
    api_secret="fgDAPEDmfeWUbA6Xk7kRK-0jajE"
)

login = LoginManager(app=app)
