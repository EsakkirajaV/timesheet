from flask import Flask,render_template,request,session,redirect
from flask_migrate import Migrate
from models import db, Users,Projects,UserProjectMapper,Timesheet
from sqlalchemy.orm import sessionmaker
import datetime,json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/profile'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db.init_app(app)
#migrate = Migrate(app, db)
app.app_context().push()

app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

app.debug = True

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
@app.route('/login', methods = ["GET","POST"])
def login():
    msg = ''
    if request.method == "POST":
        if request.form.get('username')!='' and request.form.get('password') !='':
            user = Users.query.filter_by(username=request.form.get('username'),password=request.form.get('password')).first()
            if user:
                session['loggedin']=True
                session['username']=user.username
                session['userid'] = user.userid
                return redirect('index')
            else:
                msg = 'Username & Password is incorrect! '
                return render_template('login.html',msg=msg) 

        else:
            msg = 'Please fill username & password! '   

            return render_template('login.html',msg=msg) 

    else:    
        return render_template('login.html')

@app.route('/insertdata',methods=["POST"])
def insertdata():
    if request.form['final_data']:
        for data in json.loads(request.form['final_data']):
            up_mapping_id = data['mappingid']
            no_of_hours = data['no_of_hours']
            date_of_entry = data['date_of_entry']
            project = data['project']

            insert_data = Timesheet(up_mapping_id=up_mapping_id,date_of_entry=date_of_entry,no_of_hours=no_of_hours)
            db.session.add(insert_data)
            db.session.commit()
        msg = 'Success'    
    else:
        msg = 'Failure'
    return msg   

@app.route('/viewtimesheet')
def viewtimesheet():
    if 'loggedin' in session:

        now = datetime.datetime.now()
        now_day_1 = now - datetime.timedelta(days=now.weekday())
        dates = [(now_day_1 + datetime.timedelta(days=d+0*7)).strftime("%d-%b-%Y") for d in range(7)]
        projectdetails =   UserProjectMapper.query\
            .add_columns(Projects.projectname)\
            .join(Projects,UserProjectMapper.project_id==Projects.projectid)\
            .filter(UserProjectMapper.user_id==int(session['userid']))\
            .all()
            
        timesheetdetails = db.session.query(Timesheet.date_of_entry,Timesheet.up_mapping_id,Timesheet.no_of_hours,UserProjectMapper.up_mapping_id,UserProjectMapper.project_id) .\
            filter(UserProjectMapper.user_id==int(session['userid'])).\
            all()    
        #timedetails = db.session.query(Projects.projectname,Timesheet.date_of_entry,Timesheet.no_of_hours)\
            #.join(Timesheet,UserProjectMapper.up_mapping_id==Timesheet.up_mapping_id)\
            #.outerjoin(Timesheet,UserProjectMapper.up_mapping_id==Timesheet.up_mapping_id)\
            #.filter(UserProjectMapper.user_id==int(session['userid'])).all()  
        print(timesheetdetails)
        #exit()
        context = {
            'dates'     :   dates,
            'finaldata' :   projectdetails,
            'timesheetdata' : timesheetdetails
        }
        return render_template('viewtimesheet.html',dates=dates,data = context)
    else:
        return redirect('login')    

@app.route('/entertimesheet')
def entertimesheet():
    if 'loggedin' in session:
        now = datetime.datetime.now()
        now_day_1 = now - datetime.timedelta(days=now.weekday())
        dates = [(now_day_1 + datetime.timedelta(days=d+0*7)).strftime("%d-%b-%Y") for d in range(7)]
        #project_details = Projects.query.all()
        #project_details = UserProjectMapper.query\
         #   .add_columns(Projects.projectname,UserProjectMapper.up_mapping_id)\
          #  .join(Projects,UserProjectMapper.project_id==Projects.projectid)\
           # .filter(UserProjectMapper.user_id == int(session['userid']))\
            #.all()
        project_details = db.session.query(Projects.projectname,UserProjectMapper.up_mapping_id)\
            .join(Projects,UserProjectMapper.project_id==Projects.projectid)\
            .filter(UserProjectMapper.user_id == int(session['userid'])).all()
        print(project_details)
        context = {
            'dates' : dates,
            'project_data' : project_details
        }
        return render_template('addtimeentry.html',data = context)


@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username', None)
    session.pop('userid',None)
    return redirect('login')


if __name__ == "__main__":
    db.create_all()
    app.run(host='localhost',port='5003')
