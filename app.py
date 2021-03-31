from flask import Flask,render_template,flash,redirect,url_for,session,request,logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,DateField,RadioField
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
app=Flask(__name__)

#config mySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Poojan'
app.config['MYSQL_DB']='dbmsblogproject_tp1'
app.config['MYSQL_CURSORCLASS']='DictCursor'
#init mysql
mysql=MySQL(app)



articles=Articles()

@app.route('/')

def index():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def article():
    return render_template('article.html',articlePar=articles)

@app.route('/articles/<string:id>/')
def articleID(id):
    return render_template('articleID.html',ID=id)

class RegisterForm(Form):
    username=StringField('User Name ',[validators.Length(min=5,max=25)])
    fname=StringField('First Name ',[validators.Length(min=1,max=45)])
    lname=StringField('Last Name ',[validators.Length(min=1,max=45)])
    email=StringField('Email ',[validators.Length(min=5,max=50)])
    password=PasswordField('Password ',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message=' Passwords do not match')
    ])
    confirm=PasswordField('Confirm Password')
    dob=DateField('Birth Date ', format='%Y/%m/%d')
    gender=RadioField('Gender ',choices=[('Male','Male'),('Female','Female')])
    
@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm(request.form)
    
    if request.method=='POST' and form.validate():
        
        username = form.username.data
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        username = form.username.data
        dob=form.dob.data
        gender=form.gender.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        cur = mysql.connection.cursor()

        # Execute query
        
        record=cur.execute("SELECT * from login where username=%s",[username])
        
        if record==0:
            cur.execute("INSERT INTO login(username, user_password, isAdmin, isSuperAdmin) VALUES(%s, %s, %s, %s)", (username, password, False, False))
            cur.execute("INSERT INTO user(username, firstName, lastName, birth_date,userEmail,gender) VALUES(%s, %s, %s, %s, %s, %s)", (username, fname, lname,dob, email,gender))
            mysql.connection.commit()
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username already exist. select unique Username','danger')
            return redirect(url_for('register'))
        # Close connection
        cur.close()
    return render_template('Register_2.html',form=form)

# decorator 
def isLoggedIn(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Please login first','danger')
            return redirect(url_for('login'))
    return wrap



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        # get values from requested form
        username=request.form['username']
        password_candidate=request.form['password']
        # make cursor
        cur=mysql.connection.cursor()

        # get user from database
        result=cur.execute("SELECT * from login where username=%s",[username])
        
        
        if(result>0):
            data=cur.fetchone()
            password=data['user_password']
            if(sha256_crypt.verify(password_candidate,password)):
                session['logged_in']=True
                session['username']=username
                flash('You are successfully logged in','success')
                return redirect(url_for('dashboard'))

            else:
                error='Invalid Password'
                app.logger.info('WRONG PASSWORD MATCHED')
                return render_template('login.html',error=error)
            cur.close
        else:
            error='Username not found'
            app.logger.info('NO USER FOUND')
            return render_template('login.html',error=error)

    return render_template('login.html')




@app.route('/dashboard')
@isLoggedIn
def dashboard():
    username=session['username']

    cursor=mysql.connection.cursor()

    records=cursor.execute("SELECT * from post where username=%s",[username])
    if(records>0):
        posts=cursor.fetchall()
        return render_template('dashboard.html',posts=posts)
    else:
        msg='There are 0 post. Please click add_post to post something.'
        return render_template('dashboard.html',msg=msg)
    cursor.close()


    return render_template('dashboard.html')

class Post(p):
    title=StringField('Title ',validators.Length(min=3,max=95))
@app.route('/add_Post')
@isLoggedIn
def add_Post:

@app.route('/logout')
@isLoggedIn
def logout():
    session.clear()
    flash('Logged out','success')
    return render_template('login.html')


if __name__=='__main__':
    app.secret_key='secret123'
    app.run(debug=True)
