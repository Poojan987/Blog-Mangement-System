from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form , StringField, FileField, TextAreaField, PasswordField, BooleanField, RadioField, validators, DateField
from passlib.hash import sha256_crypt
from functools import wraps
import datetime

app = Flask(__name__)
# configuration of Mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Poojan'
app.config['MYSQL_DB'] = 'dbmsblogproject_tp1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

# check if user is logged in 
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('UNAUTHORIZED, PLEASE LOGIN', 'danger')
            return redirect(url_for('login'))
    return wrap

def is_not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('home'))
    return wrap

# user login 
@app.route('/login', methods=['GET', 'POST'])
@is_not_logged_in
def login():
    if request.method=='POST':
        # getting fields of form
        username = request.form['username']
        password_candidate = request.form['password']

        # create cursor
        cur = mysql.connection.cursor()

        # to get user by username
        result = cur.execute("SELECT * FROM login WHERE username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            print(data)
            password = data['user_password']
            
            # if sha256_crypt.verify(password_candidate, password):
            if password_candidate==password or sha256_crypt.verify(password_candidate,password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['admin'] = data['isAdmin']
                session['superuser'] = data['isSuperAdmin']
                print(session)

                flash('YOU ARE LOGGED IN', 'success')
                return redirect(url_for('home'))

            else:
                error = 'INVALID PASSWORD'
                return render_template('login.html', error = error)
            # close connection
            cur.close()
            
        else:
            error = 'USERNAME NOT FOUND'
            return render_template('login.html', error = error)

            

    return render_template('login.html')


# logout
@app.route('/logout')
@is_logged_in   
def logout():
    session.clear()
    flash('YOU ARE NOW LOGGED OUT', 'success')
    return redirect(url_for('login'))

@app.route('/admins_super')
@is_logged_in
def admins_super():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    results = cur.execute("SELECT * from login where isAdmin=true and isSuperAdmin=false")

    admin_users = cur.fetchall()

    if results > 0:
        return render_template('admin_users.html', admin_users = admin_users)
    else:
        msg = 'No Admin Users Found'
        return render_template('admin_users.html', msg=msg)

    # closing the connection
    cur.close()

@app.route('/users')
@is_logged_in
def users():
    cur = mysql.connection.cursor()

    result = cur.execute("select * from user")

    users = cur.fetchall()

    cur.close()

    if result > 0:
        return render_template('all_users.html', users = users)
    else:
        msg = 'No users Found'
        return render_template('all_users.html', msg=msg)

# Article class
class AdminUserForm(Form):
    username = StringField('username', [validators.Length(min=1, max=200)])
    user_password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm',message=' Passwords do not match')
    ])
    confirm=PasswordField('Confirm Password')
    # is_Admin = BooleanField('is_Admin', [validators.DataRequired()])

# Article route
@app.route('/add_admin_user', methods=['GET', 'POST'])
@is_logged_in
def add_admin_user():
    form = AdminUserForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        user_password = sha256_crypt.encrypt(str(form.user_password.data))

        # create cursors
        cur = mysql.connection.cursor()

        result = cur.execute("select username from login")
        
        result1 = list(cur.fetchall())
        tkp = []
        for i in result1:
            tkp.append(i['username'])
        if username in tkp:
            error = 'USERNAME ALREADY EXISTS'
            return render_template('add_admin_user.html', form = form, error=error)
        else:

            # print(123456, True)
            # print(1111, result1, tkp, type(result1))
            # execute
            cur.execute("INSERT INTO login(username, user_password, isAdmin) VALUES( %s, %s, 1)", (username, user_password))
            
            cur.execute("INSERT INTO admin(username) values(%s)", [username])
            # commit to DB
            mysql.connection.commit()

            # close connection
            cur.close()

            flash('Admin User created successfully', 'success')

            return redirect(url_for('admins_super'))
    
    return render_template('add_admin_user.html', form = form)

@app.route('/add_user', methods=['GET', 'POST'])
@is_logged_in
def add_user():
    form = AdminUserForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        user_password = sha256_crypt.encrypt(str(form.user_password.data))

        # create cursors
        cur = mysql.connection.cursor()

        result = cur.execute("select username from login")
        
        result1 = list(cur.fetchall())
        tkp = []
        for i in result1:
            tkp.append(i['username'])
        if username in tkp:
            error = 'USERNAME ALREADY EXISTS'
            return render_template('add_user.html', form = form, error=error)
        else:

            # print(123456, True)
            # print(1111, result1, tkp, type(result1))
            # execute
            cur.execute("INSERT INTO login(username, user_password, isAdmin) VALUES( %s, %s, 0)", (username, user_password))
            
            cur.execute("INSERT INTO user(username) values(%s)", [username])
            # commit to DB
            mysql.connection.commit()

            # close connection
            cur.close()

            flash('User created successfully', 'success')

            return redirect(url_for('users'))
    
    return render_template('add_user.html', form = form)


# delete article
@app.route('/delete_admin_user/<string:username>', methods=['GET', 'POST'])
@is_logged_in
def delete_admin_user(username):
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM admin WHERE username = %s", [username])
    cur.execute("DELETE FROM login WHERE username = %s", [username])

    mysql.connection.commit()

    cur.close()

    flash('Admin User Deleted', 'success')

    return redirect(url_for('admins_super'))

@app.route('/delete_user/<string:username>', methods=['GET', 'POST'])
@is_logged_in
def delete_user(username):
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM user WHERE username = %s", [username])
    cur.execute("DELETE FROM login WHERE username = %s", [username])

    mysql.connection.commit()

    cur.close()

    flash('User Deleted', 'success')

    return redirect(url_for('users'))

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
    # print("hello")
    if request.method=='POST' and form.validate():
        
        username = form.username.data
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        username = form.username.data
        dob=form.dob.data
        gender=form.gender.data
        password = sha256_crypt.encrypt(str(form.password.data))
        profile = 'male.png'
        if gender=='Female':
            profile='female.png'

        cur = mysql.connection.cursor()

        # Execute query
        
        try:
            try:
                cur.execute("INSERT INTO login(username, user_password, isAdmin, isSuperAdmin) VALUES(%s, %s, %s, %s)", (username, password, False, False))
                cur.execute("INSERT INTO user(username, firstName, lastName, birth_date,userEmail,gender) VALUES(%s, %s, %s, %s, %s, %s)", (username, fname, lname,dob, email,gender))
                cur.close()
                mysql.connection.commit()
                # return redirect(url_for('index'))
                return redirect(url_for('login'))
                # NB : you won't get an IntegrityError when reading
            except (mysql.connection.Error) as e:
                e=str(e).split(',')
                e=e[1].split('\'')
                e=e[1]
                # print(e)
                # msg=e.msg
                cur.close()
                flash(e,'danger')
                # return render_template('Register_2.html',form=form)
                return redirect(url_for('register'))

        finally:
            print("tp")
        











        record=cur.execute("SELECT * from login where username=%s",[username])
        # print('123',username)        
        if record<=0:
            cur.execute("INSERT INTO login(username, user_password, isAdmin, isSuperAdmin) VALUES(%s, %s, %s, %s)", (username, password, False, False))
            cur.execute("INSERT INTO user(username, firstName, lastName, birth_date,userEmail,gender, profile) VALUES(%s, %s, %s, %s, %s, %s, %s)", (username, fname, lname,dob, email,gender, profile))
            mysql.connection.commit()
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exist. select unique Username','danger')
            return redirect(url_for('register'))
        # Close connection
        cur.close()
    return render_template('register2.html',form=form)


class EditForm(Form):
    fname=StringField('First Name ',[validators.Length(max=45)])
    lname=StringField('Last Name ',[validators.Length(max=45)])
    email=StringField('Email ',[validators.Length(max=50)])
    dob=DateField('Birth Date ', format='%Y/%m/%d')
    gender=RadioField('Gender ',choices=[('Male','Male'),('Female','Female')])
@app.route('/profile/<string:username>', methods=['GET', 'POST'])
@is_logged_in
def profile(username):
    cur = mysql.connection.cursor()

    rs = cur.execute("SELECT * FROM login WHERE username = %s", [username])

    dt1 = cur.fetchone()
    
    cur.close()

    print(session)
    if dt1['isAdmin']==0:
        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM user WHERE username = %s", [username])

        dt = cur.fetchone()
        
        cur.close()

        form = EditForm(request.form)

        if dt['firstName']==None:
            dt['firstName']=''
        if dt['lastName']==None:
            dt['lastName']=''
        if dt['userEmail']==None:
            dt['userEmail']=''
        if dt['gender']==None:
            dt['gender']='Male'
        if dt['birth_date']==None:
            tt = datetime.datetime.now()
            dt['birth_date']=datetime.date(tt.year, tt.month, tt.day)

        form.fname.data = dt['firstName']
        form.lname.data = dt['lastName']
        form.dob.data = dt['birth_date']
        form.email.data = dt['userEmail']
        form.gender.data = dt['gender']
        print(dt, 12)
        # print(request.form, request.form['fname'], request.method, request.form['dob'])
        print(form.validate())

        if request.method == 'POST' and form.validate():
            fname = request.form['fname']
            lname = request.form['lname']
            dob = request.form['dob']
            email = request.form['email']
            gender = request.form['gender']

            cur = mysql.connection.cursor()
            print(fname, lname, dob, email, gender)
            kp = 'male.jpg'
            if gender=='Female':
                kp = 'female.jpg'
            print(gender, kp)
            # execute
            cur.execute("UPDATE user SET firstname = %s, lastname = %s, birth_date = %s, userEmail = %s, gender = %s, profile=%s WHERE username = %s", (fname, lname, dob, email, gender, kp, username))

            # commit to DB
            mysql.connection.commit()

            # close connection
            cur.close()

            flash('Information Updated', 'success')

            return redirect(url_for('home'))
        
        return render_template('edit_profile.html', form = form)


    else:
        print(123)
        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM admin WHERE username = %s", [username])

        dt = cur.fetchone()
        
        cur.close()

        form = EditForm(request.form)

        if dt['firstName']==None:
            dt['firstName']=''
        if dt['lastName']==None:
            dt['lastName']=''
        if dt['adminEmail']==None:
            dt['adminEmail']=''
        if dt['gender']==None:
            dt['gender']='Male'
        if dt['birth_date']==None:
            tt = datetime.datetime.now()
            dt['birth_date']=datetime.date(tt.year, tt.month, tt.day)

        form.fname.data = dt['firstName']
        form.lname.data = dt['lastName']
        form.dob.data = dt['birth_date']
        form.email.data = dt['adminEmail']
        form.gender.data = dt['gender']
        print(dt)
        # print(request.form, request.form['fname'], request.method, request.form['dob'])
        print(form.validate())
        if request.method == 'POST' and form.validate():
            fname = request.form['fname']
            lname = request.form['lname']
            dob = request.form['dob']
            email = request.form['email']
            gender = request.form['gender']

            cur = mysql.connection.cursor()
            print(fname, lname, dob, email, gender)
            # execute
            cur.execute("UPDATE admin SET firstname = %s, lastname = %s, birth_date = %s, adminEmail = %s, gender = %s WHERE username = %s", (fname, lname, dob, email, gender, username))

            # commit to DB
            mysql.connection.commit()

            # close connection
            cur.close()

            flash('Information Updated', 'success')

            return redirect(url_for('home'))
        
        return render_template('edit_profile.html', form = form)




@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()

    # Get articles
    results = cur.execute("SELECT * from post where username=%s",[session['username']])

    posts = cur.fetchall()

    if results > 0:
        return render_template('dashboard.html', posts = posts)
    else:
        msg = 'No posts Found'
        return render_template('dashboard.html', msg=msg)

    # closing the connection
    cur.close()

class Post(Form):
    title=StringField('Title ',[validators.Length(min=3,max=95)])
    brief=StringField('Brief Description',[validators.Length(min=3,max=150)])
    body=TextAreaField('Body ',[validators.Length(min=1)])

@app.route('/add_Post',methods=['GET','POST'])
@is_logged_in
def add_Post():
    form=Post(request.form)
    if(request.method=='POST' and form.validate()):
        title=form.title.data
        brief=form.brief.data
        body=form.body.data
        cur =mysql.connection.cursor()

        try:
            try:
                cur.execute('insert into post(username,title,blogcontent,brief_desc) values(%s,%s,%s,%s)',(session['username'],title,body,brief))
                cur.close()
                mysql.connection.commit()
                flash('Post added:)','success')
                return redirect(url_for('dashboard'))
            except (mysql.connection.Error) as e:
                e=str(e).split(',')
                e=e[1].split('\'')
                e=e[1]
                # print(e)
                # msg=e.msg
                cur.close()
                flash(e,'danger')
                # return render_template('Register_2.html',form=form)
                return redirect(url_for('add_Post'))

        finally:
            print("tp")
        




        # cur.execute('insert into post(username,title,blogcontent,brief_desc) values(%s,%s,%s,%s)',(session['username'],title,body,brief))
        # cur.close()
        # mysql.connection.commit()
        # flash('Post added:)','success')
        # return redirect(url_for('dashboard'))
    return render_template('add_Post.html',form=form)


@app.route('/all_posts')
def all_posts():
    cur = mysql.connection.cursor()

    # Get articles
    results = cur.execute("SELECT * from post")

    posts = list(cur.fetchall())

    rec = cur.execute("select accepted_posts()")

    rec1 = cur.fetchone()
    tp = list(rec1.values())[0]
    print(tp)
    tkp=[]
    if len(tp)>0:
        tkp = list(map(int,tp[1:].split(';')))
    
    dp = []
    for i in posts:
        if i['post_id'] not in tkp:
            dp.append(i)
    
    if results > 0:
        return render_template('all_posts.html', posts = tuple(dp))
    else:
        msg = 'No Posts Found'
        return render_template('all_posts.html', msg=msg)

    # closing the connection
    cur.close()

@app.route('/all_posts/<string:postid>')
def post(postid):
    cur = mysql.connection.cursor()
    cur.execute("call check_views(%s)", [postid])
    mysql.connection.commit()

    result = cur.execute("SELECT * FROM post WHERE post_id=%s", [postid])
    post = cur.fetchone()

    if len(session)!=0:
        result1 = cur.execute("SELECT liked(%s, %s)", (session['username'], postid))
        flag = cur.fetchone()
        post['flag'] = list(flag.values())[0]
    cur.close()
    return render_template('post.html', post = post)


@app.route('/edit_post/<string:postid>', methods=['GET', 'POST'])
@is_logged_in
def edit_post(postid):
    # create cursor
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM post WHERE post_id = %s", [postid])

    post = cur.fetchone()
    
    cur.close()


    form = Post(request.form)

    form.title.data = post['title']
    form.brief.data = post['brief_desc']
    form.body.data = post['blogcontent']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        brief = request.form['brief']
        body = request.form['body']

        # create cursors
        cur = mysql.connection.cursor()

        # execute

        try:
            try:
                cur.execute("UPDATE post SET title = %s, brief_desc=%s, blogcontent = %s WHERE post_id = %s", (title, brief, body, postid))
                mysql.connection.commit()
                cur.close()
                flash('Post Edited successfully', 'success')
                return redirect(url_for('dashboard'))
            except (mysql.connection.Error) as e:
                e=str(e).split(',')
                e=e[1].split('\'')
                e=e[1]
                # print(e)
                # msg=e.msg
                cur.close()
                flash(e,'danger')
                # return render_template('Register_2.html',form=form)
                return redirect(url_for('dashboard'))

        finally:
            print("tp")
        
        # cur.execute("UPDATE post SET title = %s, brief_desc=%s, blogcontent = %s WHERE post_id = %s", (title, brief, body, postid))

        # # commit to DB
        # mysql.connection.commit()

        # close connection
        

        # flash('Post Edited successfully', 'success')

        return redirect(url_for('dashboard'))
    
    return render_template('edit_post.html', form = form)


@app.route('/delete_post/<string:postid>', methods=['GET', 'POST'])
@is_logged_in
def delete_post(postid):
    cur = mysql.connection.cursor()

    # execute

    cur.execute("DELETE FROM post WHERE post_id = %s", [postid])

    mysql.connection.commit()

    cur.close()

    flash('Post Deleted', 'success')

    return redirect(url_for('dashboard'))

@app.route('/profile_user/<string:username>')
def profile_user(username):
    user = {}
    if username!='style.css':
        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM user WHERE username = %s", [username])
        user = cur.fetchone()

        result1 = cur.execute("SELECT * from post")
        posts = cur.fetchall()

        res = cur.execute("call valid_post(%s)", [username])
        all_stats = cur.fetchone()

        tp = all_stats['finalStats']
        kp = list(tp.split(':'))
        kp.pop(0)
        for i in range(len(kp)):
            kp[i]=list(kp[i].split(';'))
        # print(user)
        dp = kp.pop()
        user['likes']=dp[0]
        user['views']=dp[1]
        user['posts']=dp[2]
        tsp = []
        for i in range(len(kp)):
            tsp.append(kp[i][0])
        print(tsp)
        ans = []
        for i in posts:
            if str(i['post_id']) in tsp:
                ans.append(i)
                lk = cur.execute("select likesOfParticularPost(%s)", [i['post_id']])
                lks = cur.fetchone()
                ans[-1]['likes']=list(lks.values())[0]
                vw = cur.execute("select viewsOfParticularPost(%s)", [i['post_id']])
                vws = cur.fetchone()
                ans[-1]['views']=list(vws.values())[0]
        # profile = {'ans':ans,'user':user}
        cur.close()
        for i in ans:
            print(i['likes'], i['views'])

    return render_template('profile_user.html', profile={'ans':tuple(ans),'user':user}, pic = user['profile']) 



@app.route('/post_permission')
@is_logged_in
def post_permission():
    cur = mysql.connection.cursor()

    results = cur.execute("SELECT post.post_id, post.username, post.dt, post.title, post.isDeleted, post.brief_desc, post.blogcontent, post.bool_repost, post.repost_user_name FROM post, to_be_accepted where post.post_id=to_be_accepted.post_id and to_be_accepted.appr=0")

    posts = cur.fetchall()

    if results > 0:
        return render_template('post_permission.html', posts = posts)
    else:
        msg = 'No Posts Found'
        return render_template('post_permission.html', msg=msg)
    
    cur.close()

@app.route('/approved/<string:postid>', methods=['GET', 'POST'])
@is_logged_in
def approved(postid):
    cur = mysql.connection.cursor()

    # execute
    cur.execute("INSERT INTO permission_bridge_temp(admin_user, post_id, status) values(%s, %s, 'Approved')", (session['username'], postid))
    cur.execute("DELETE FROM to_be_accepted WHERE post_id = %s", [postid])

    mysql.connection.commit()

    cur.close()

    flash('Post Approved', 'success')

    return redirect(url_for('post_permission'))

@app.route('/rejected/<string:postid>', methods=['GET', 'POST'])
@is_logged_in
def rejected(postid):
    cur = mysql.connection.cursor()

    # execute
    cur.execute("INSERT INTO permission_bridge_temp(admin_user, post_id, status) values(%s, %s, 'Rejected')", (session['username'], postid))
    cur.execute("UPDATE to_be_accepted SET appr=1 WHERE post_id = %s", [postid])

    mysql.connection.commit()

    cur.close()

    flash('Post Rejected', 'danger')

    return redirect(url_for('post_permission'))

@app.route('/like_post/<string:postid>/<string:username>')
@is_logged_in
def like_post(postid, username):
    cur = mysql.connection.cursor()

    results = cur.execute("select * from likes")
    all_us = list(cur.fetchall())
    
    f=0
    for i in all_us:
        if i['username']==username and str(i['post_id'])==postid:
            f=1
            break
    if f==0:
        cur.execute("INSERT INTO likes values(%s, %s)", (username, postid))
    else:
        cur.execute("delete from likes where username=%s and post_id=%s", (username, postid))

    mysql.connection.commit()

    cur.close()

    return redirect(request.referrer)



if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)







    