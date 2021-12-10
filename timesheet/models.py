from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"

    userid      = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username    = db.Column(db.String(50))
    password    = db.Column(db.String(100)) 
    useractive  = db.Column(db.Integer())

    mapping_user = db.relationship('UserProjectMapper', backref='users')

    def __init__(self,username,password,useractive):
        self.username = username
        self.password = password
        self.useractive = useractive


    def __repr__(self):
        return f"{self.userid}:{self.username}:{self.useractive}"

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
        
class Projects(db.Model):
    __tablename__ = "projects"

    projectid           =   db.Column(db.Integer,primary_key=True, autoincrement=True)
    projectname         =   db.Column(db.String(50))
    project_start_date  =   db.Column(db.DateTime())
    project_end_date    =   db.Column(db.DateTime())

    mapping_project       = db.relationship('UserProjectMapper', backref='projects')

    def __init__(self,projectname,project_start_date,project_end_date):
        self.projectname        =   projectname
        self.project_start_date =   project_start_date
        self.project_end_date   =   project_end_date

    def __repr__(self):
        return f"{self.projectname}:{self.project_start_date}:{self.project_end_date}"


class UserProjectMapper(db.Model):
        __tablename__   =   'userprojectmapper'

        up_mapping_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)   
        user_id         = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable = False)
        project_id      = db.Column(db.Integer, db.ForeignKey('projects.projectid'), nullable = False)

        #timesheet       = db.relationship('Timesheet', backref='UserProjectMapper')

        def __init__(self,up_mapping_id,user_id,project_id):
            self.up_mapping_id  = up_mapping_id
            self.user_id        = user_id
            self.project_id     = project_id

        def __repr__(self):
            return f"{self.up_mapping_id}:{self.user_id},{self.project_id}"


class Timesheet(db.Model):
    __tablename__ = "timesheet"

    time_entryid    =   db.Column(db.Integer, primary_key=True)
    up_mapping_id   =   db.Column(db.Integer, db.ForeignKey('userprojectmapper.up_mapping_id'), nullable = False)
    date_of_entry   =   db.Column(db.Date, nullable = False)
    no_of_hours     =   db.Column(db.String(50), default='00:00', nullable = False)

    def __init__(self,up_mapping_id,date_of_entry,no_of_hours):

        self.up_mapping_id = up_mapping_id
        self.date_of_entry = date_of_entry
        self.no_of_hours   = no_of_hours

    def __repr__(self):

        return f"{self.time_entryid}:{self.up_mapping_id}:{self.date_of_entry}:{self.no_of_hours}"
    