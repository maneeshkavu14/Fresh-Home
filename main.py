# from crypt import methods
from functools import wraps
from traceback import print_tb
from flask import Flask, flash, current_app, render_template, send_from_directory, request, session, redirect, url_for
from flaskext.mysql import MySQL
import os
from werkzeug.utils import secure_filename
from datetime import datetime
# auto-generate password
import string
import random
# e-mail
from flask_mail import Mail, Message
import smtplib
from flask_cors import CORS
app = Flask(__name__)

app.secret_key = '56tf645fg6f676hg66'

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'

app.config['MYSQL_DATABASE_PASSWORD'] = 'root'

app.config['MYSQL_DATABASE_DB'] = 'freshhome'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


app.config['PATH'] = 'C:/Users/sande/OneDrive/Desktop/freshhome/server/static/fileupload'

# mail
mail = Mail(app)
# congiguration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'webfarmstpius@gmail.com'
app.config['MAIL_PASSWORD'] = 'uauyhavmlkcjvjla'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

mysql.init_app(app)

ALLOWED_EXTENSIONS = {'txt', 'png', 'pdf', 'jpeg', 'jpg', 'gif'}

# =======================login Validator=======================================


def allow_for_loggined_users_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.endpoint))
        return f(*args, **kwargs)
    return wrapper


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

# Password Generator


def password(size=8, characters=string.ascii_letters + string.digits):
    return ''.join(random.choice(characters) for _ in range(size))


def Mailer(sender, recipient, Subject, body):
    try:
        msg = Message(Subject, sender=sender, recipients=[recipient])
        msg.body = body
        mail.send(msg)

        return "sended successfully"
    except:
        return "A Error occurred while perform mailing !"

# ----------------------------------------------------------------------------


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from pro_registration"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template("index.html", row=data)


@app.route('/customer_registration', methods=['GET', 'POST'])
def customer_registration():
    if request.method == 'POST':
        try:
            data = request.form
            today = datetime.today()
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "insert into login(username,password,type) values (%s,%s,%s)"
            cursor.execute(
                query, (data['username'], data['password'], 'customer'))
            conn.commit()
            username = [data['username'], data['password']]

            query = "insert into registration(fname,lname,email,phone,gender,adrs,district,city,pin,created_on,lid,type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query, (data['fname'], data['lname'], data['email'], data['phone'], data['gender'],
                           data['adrs'], data['district'], data['city'], data['pin'], today, cursor.lastrowid, 'customer'))
            response = Mailer("webfarmstpius@gmail.com",
                              data['email'], " You have been successfully Registered from this email and your login username and password is  ", ":is username and password is:".join(username))
            print(response)
            conn.commit()
            conn.close()
            flash('You have been successfully Registered and the username, password has been sended to your Email !!!')
            return redirect(url_for('customer_registration'))
        except Exception as e:
            flash('Something went wrong Check details you provided is Correct or not !!!')
            return redirect(url_for('customer_registration'))
    if request.method == 'GET':
        return render_template('customer_registration.html')
# ------------------------------------------------------------------------------------


@app.route('/farmer_registration', methods=['GET', 'POST'])
def farmer_registration():
    if request.method == 'POST':

        try:
            data = request.form
            today = datetime.today()
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "insert into login(username,password,type) values (%s,%s,%s)"
            cursor.execute(
                query, (data['username'], data['password'], 'farmer'))
            conn.commit()
            username = [data['username'], data['password']]
            query = "insert into registration(fname,lname,email,phone,gender,adrs,district,city,pin,society_regno,adhaarno,created_on,lid,type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query, (data['fname'], data['lname'], data['email'], data['phone'], data['gender'], data['adrs'],
                           data['district'], data['city'], data['pin'], data['society_regno'], data['adhaarno'], today, cursor.lastrowid, 'farmer'))
            response = Mailer("webfarmstpius@gmail.com",
                              data['email'], " You have been successfully Registered from this email and your login username and password is  ", ":is username and password is:".join(username))
            print(response)
            conn.commit()
            conn.close()
            flash('You have been successfully Registered and the username, password has been sended to your Email !!!')
            return redirect(url_for('farmer_registration'))
        except Exception as e:
            flash('Something went wrong Check details you provided is Correct or not !!!')
            return render_template('farmer_registration.html')
    if request.method == 'GET':
        return render_template('farmer_registration.html')


# --------------------------------------------------------------------------------------

@app.route('/admin_add_delivery_agent', methods=['GET', 'POST'])
def admin_add_delivery_agent():
    if request.method == 'GET':
        return render_template('admin_add_delivery_agent.html')
    if request.method == 'POST':
     try:
        data = request.form
        password = randomString(8)
        print(password)
        today = datetime.today()
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "insert into login(username,password,type) values (%s,%s,%s)"
        cursor.execute(query, (data['email'], password, 'agent'))
        conn.commit()
        query = "insert into registration(fname,lname,email,phone,gender,adrs,district,city,pin,created_on,lid,type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['fname'], data['lname'], data['email'], data['phone'], data['gender'],
                       data['adrs'], data['district'], data['city'], data['pin'], today, cursor.lastrowid, 'agent'))
        response = Mailer("webfarmstpius@gmail.com",
                          data['email'], " You are become an agent of Webfarm Delivery System ,And your login password is  ",(password))
        print(response)
        conn.commit()
        conn.close()
        flash('Delivery Agent Added Successfully !!!')
        return redirect(url_for('admin_add_delivery_agent'))
     except Exception as e:
        flash('Something went wrong Check details you provided is Correct or not !!!')
        return render_template('admin_add_delivery_agent.html')
    if request.method == 'GET':
        return render_template('admin_add_delivery_agent.html')

# ------------------------------------------------------------------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        conn = mysql.connect()
        curser = conn.cursor()
        query = "select * from login where username=%s and password=%s"
        curser.execute(
            query, (request.form['username'], request.form['password']))
        conn.commit()
        account = curser.fetchone()
        if account:
            print(account)
            session['loggedin'] = True
            session['lid'] = account[0]

            session['username'] = account[1]
            if account[3] == 'admin':
                return redirect(url_for('admin_home'))
            elif account[3] == 'farmer':
                conn = mysql.connect()
                curser = conn.cursor()
                query = ("select * from registration where lid=%s")
                curser.execute(query, account[0])
                row = curser.fetchone()
                session['pin'] = row[7]
                print(session['pin'])
                print(account[0])

                return redirect(url_for('farmer_home'))
            elif account[3] == 'agent':
                conn = mysql.connect()
                curser = conn.cursor()
                query = ("select * from registration where lid=%s")
                curser.execute(query, account[0])
                row = curser.fetchone()
                session['pin'] = row[7]
                print(session['pin'])
                print(account[0])
                return redirect(url_for('agent_home'))
            elif account[3] == 'customer':
                conn = mysql.connect()
                curser = conn.cursor()
                query = ("select * from registration where lid=%s")
                curser.execute(query, account[0])
                row = curser.fetchone()
                session['district'] = row[5]
                print(session['district'])
                print(account[0])
                return redirect(url_for('customer_home'))
            else:
                flash('please Register')
        else:
            flash('Incorrect username or password supplied')
            return render_template("login.html")

# ------------------------------------------------------------------------------------


@app.route('/logout', methods=['GET'])
@allow_for_loggined_users_only
def logout():
    if session['loggedin']:
        session['loggedin'] = False
        session.pop('lid', None)
        session.pop('username', None)
        return redirect(url_for('login'))
    else:
        print("login first")

# ------------------------------------------------------------------------------------


@app.route('/admin_add_announcement', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def admin_add_announcement():
    if request.method == 'GET':
        return render_template('admin_add_announcement.html')
    if request.method == 'POST':

        try:
            data = request.form
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "insert into announcement(subject,content,date,type) values(%s,%s,%s,%s)"
            cursor.execute(
                query, (data['subject'], data['content'], datetime.now(), 'admin'))
            conn.commit()
            conn.close()
            flash("Announcement added Successfully ")
            return redirect(url_for('admin_add_announcement'))
        except Exception as e:
            flash("Something went Wrong !!!")
            return redirect(url_for('admin_add_announcement'))

# --------------------------------------------------------------------------------------------


@app.route('/farmer_add_announcement', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def farmer_add_announcement():
    if request.method == 'GET':
        return render_template('farmer_add_announcement.html')
    if request.method == 'POST':
        try:
            data = request.form
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "insert into announcement(subject,content,date,type) values(%s,%s,%s,%s)"
            cursor.execute(
                query, (data['subject'], data['content'], datetime.now(), 'farmer'))
            conn.commit()
            conn.close()
            flash("Announcement added Successfully ")
            return redirect(url_for('farmer_add_announcement'))
        except Exception as e:
            flash("Something went Wrong !!!")
            return redirect(url_for('farmer_add_announcement'))

# ------------------------------------------------------------------------------------


@app.route('/admin_add_application', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def admin_add_application():
    if request.method == 'GET':
        return render_template('admin_add_application.html')
    if request.method == 'POST':
        try:
            data = request.form
            image = request.files['image']
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['PATH']+filename))
            today = datetime.today()
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "insert into application(app_name,image,description,created_on) values(%s,%s,%s,%s)"
            cursor.execute(
                query, (data['app_name'], filename, data['description'], today))
            conn.commit()
            conn.close()

            flash("Application added Successfully ")
            return redirect(url_for('admin_add_application'))
        except Exception as e:
            flash("Something went Wrong !!!")
            return redirect(url_for('admin_add_application'))


# ------------------------------------------------------------------------------------

@app.route('/view_application', methods=['GET'])
@allow_for_loggined_users_only
def view_application():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from application")
        row = cursor.fetchall()
        # print(row)
        conn.commit()
        conn.close()
        return render_template('view_application.html', result=row)


@app.route('/admin_view_application', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def admin_view_application():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from application")
        row = cursor.fetchall()
        # print(row)
        conn.commit()
        conn.close()
        return render_template('admin_view_application.html', result=row)
    if request.method == 'POST':
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "delete from application where app_id=%s"
            cursor.execute(query, request.form.get('delete_by_id'))
            conn.commit()
            conn.close()
            flash("Application has been deleted Successfully ")
            return redirect(url_for('admin_view_application'))
        except Exception as e:
            flash("Something went Wrong !!!")
            return redirect(url_for('admin_view_application'))

# ---------------------------pdf dwnld----------------------------------------------------


@app.route('/return-files/<file_name>')
@allow_for_loggined_users_only
def returnfiles(file_name):
    print(file_name)
    uploads = os.path.join(current_app.root_path, app.config['PATH'])
    return send_from_directory(directory=uploads, path=file_name)

# ------------------------------------------------------------------------------------


@app.route('/feedback', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def feedback():
    if request.method == 'GET':
        return render_template('feedback.html')
    if request.method == 'POST':
        try:
            data = request.form
            print(session['lid'])
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "insert into feedback(subject,feedback,lid,created_on) values(%s,%s,%s,%s)"
            cursor.execute(
                query, (data['subject'], data['feedback'], session['lid'], datetime.now()))
            print(query)
            conn.commit()
            conn.close()
            flash(" Your feedback has been added Successfully ")
            return render_template('feedback.html')
        except Exception as e:
            flash("Something went Wrong !!!")
            return render_template('feedback.html')


# ------------------------------------------------------------------------------------

@app.route('/add_pro_category', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def add_pro_category():
    if request.method == 'GET':
        return render_template("add_pro_category.html")
    if request.method == 'POST':
        try:
            data = request.form
            image = request.files['image']
            filename = secure_filename(image.filename)
            print(os.path.join(app.config['PATH'], filename))
            image.save(os.path.join(app.config['PATH'], filename))
            conn = mysql.connect()
            cursor = conn.cursor()
            print(filename)
            print(datetime.now())
            conn.commit()
            query = "INSERT INTO product_category(categoryname, image, createdon) values(%s,%s,%s)"
            cursor.execute(
                query, (data['categoryname'], filename, datetime.now()))
            print(query)
            conn.commit()
            conn.close()
            flash("Product category added Successfully ")
            return redirect(url_for('add_pro_category'))
        except Exception as e:
            flash("Something went Wrong !!!")
            return redirect(url_for('add_pro_category'))
            # return redirect(url_for('add_pro_category'))

# ----------------------------------------------------------------------------


@app.route('/admin_view_product', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def admin_view_product():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from pro_registration"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_product.html', result=data)
    if request.method == 'POST':
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "delete from pro_registration where pid=%s"
            cursor.execute(query, request.form.get('delete_by_id'))
            conn.commit()
            conn.close()
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "select * from pro_registration"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            flash(" Product has been Removed Successfully ")
            return render_template('admin_view_product.html', result=data)
        except Exception as e:
            flash("Something went Wrong !!!")
            return render_template('admin_view_product.html', result=data)



@app.route('/farmer_view_product', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def farmer_view_product():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from pro_registration where logid=%s"
        cursor.execute(query,session['lid'])
        data = cursor.fetchall()
        conn.close()
        return render_template('farmer_view_product.html', result=data)
    if request.method == 'POST':
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            query= "UPDATE pro_registration SET stock=%s where  pid=%s"
            cursor.execute(query,(request.form.get("stock"),request.form.get("pid")))
            conn.commit()
            query = "select * from pro_registration where logid=%s"
            cursor.execute(query,session['lid'])
            data = cursor.fetchall()
            conn.close()
            flash(" Your Stock has been Edited Successfully ")
            return render_template('farmer_view_product.html', result=data)
        except Exception as e:
            flash("Something went Wrong !!!")
            return render_template('farmer_view_product.html', result=data)

# ---------------------------------------------------------------------------


@app.route('/farmer_pro_reg', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def farmer_pro_reg():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_category")
        row = cursor.fetchall()
        print(row)
        conn.commit()
        conn.close()
        return render_template('farmer_pro_reg.html', row=row)
    if request.method == 'POST':
        try:
            data = request.form
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['PATH'], filename))
                conn = mysql.connect()
                cursor = conn.cursor()
                s = session['lid']
                path = os.path.join(app.config['PATH'], filename)
                print(path)
                d1 = data['desc']
                query = "INSERT INTO pro_registration(`pname`,`image`,`desc`,`price`,`stock`,`pcid`,`logid`) values (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(
                    query, (data['pname'], filename, d1, data['price'], data['stock'], data['pcid'], s))
                conn.commit()
                conn.close()
                flash(" Your Product added Successfully ")
            return redirect(url_for('farmer_pro_reg'))
        except Exception as e:
            flash("Something went Wrong !!!")
            return redirect(url_for('farmer_pro_reg'))
            # return render_template('farmer_home.html')

# ------------------------------------------------------------------------------------


@app.route('/customer_home', methods=['GET'])
@allow_for_loggined_users_only
def customer_home():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select  pro_registration.* ,registration.* from pro_registration ,registration where registration.lid=pro_registration.logid and registration.district=%s"
        cursor.execute(query, session['district'])
        data = cursor.fetchall()

        conn.close()
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select sum(qnty) from cart where usr_id=%s "
        cursor.execute(query, (session['lid']))
        qnty = cursor.fetchall()
        return render_template('customer_home.html', row=data, qnty=qnty)


# ------------------------------------------------------------------------------------

@app.route('/farmer_home')
@allow_for_loggined_users_only
def farmer_home():
    return render_template("farmer_home.html")


@app.route('/agent_home')
@allow_for_loggined_users_only
def agent_home():

    return render_template("agent_home.html")

# ------------------------------------------------------------------------------------


@app.route('/admin_home')
@allow_for_loggined_users_only
def admin_home():
    return render_template("admin_home.html")

# --------------------------------------------------------------------------


@app.route('/farmer_view_announcement', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def farmer_view_announcement():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from announcement where type='admin'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('farmer_view_announcement.html', result=data)

# ------------------------------------------------------------------------------------


@app.route('/agent_view_admin_announcement', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def agent_view_admin_announcement():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from announcement where type='admin'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('agent_view_admin_announcement.html', result=data)

# --------------------------------------------------------------------------


@app.route('/customer_view_announcement', methods=['GET'])
@allow_for_loggined_users_only
def customer_view_announcement():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from announcement where type='admin'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('customer_view_announcement.html', result=data)


@app.route('/customer_view_farmer_announcement', methods=['GET'])
@allow_for_loggined_users_only
def customer_view_farmer_announcement():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from announcement where type='farmer'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('customer_view_farmer_announcement.html', result=data)

# -----------------------------------------------------------------------------


@app.route('/admin_view_farmer', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def admin_view_farmer():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from registration where type='farmer'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_farmer.html', result=data)
    if request.method == 'POST':
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "delete from registration where lid=%s"
            query = "delete from login where lid=%s"
            cursor.execute(query, request.form.get('delete_by_id'))
            conn.commit()
            conn.close()
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "select * from registration where type='farmer'"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            flash(" Farmer removed Successfully ")
            return render_template('admin_view_farmer.html', result=data)
        except Exception as e:
            flash("Something went Wrong !!!")
            return render_template('admin_view_farmer.html', result=data)


# -----------------------------------------------------------------------

@app.route('/admin_view_customer', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def admin_view_customer():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from registration where type='customer'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_customer.html', result=data)
    if request.method == 'POST':
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "delete from registration where lid=%s"
            query = "delete from login where lid=%s"
            cursor.execute(query, request.form.get('delete_by_id'))
            conn.commit()
            conn.close()
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "select * from registration where type='customer'"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            flash(" Customer removed Successfully ")
            return render_template('admin_view_customer.html', result=data)
        except Exception as e:
            flash("Something went Wrong !!!")
            return render_template('admin_view_customer.html', result=data)

# ------------------------------------------------------------------------------


@app.route('/admin_view_delivery_agent', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def admin_view_delivery_agent():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select * from registration where type='agent'"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_view_delivery_agent.html', result=data)
    if request.method == 'POST':
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "delete from registration where lid=%s"
            query = "delete from login where lid=%s"
            cursor.execute(query, request.form.get('delete_by_id'))
            conn.commit()
            conn.close()
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "select * from registration where type='agent'"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            flash(" Delivery agent removed Successfully ")
            return render_template('admin_view_delivery_agent.html', result=data)
        except Exception as e:
            flash("Something went Wrong !!!")
            return render_template('admin_view_delivery_agent.html', result=data)

# ------------------------------------------------------------------------


@app.route('/customer_add_complaints', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def customer_add_complaints():
    if request.method == 'GET':
        return render_template('customer_add_complaints.html')
    if request.method == 'POST':
        try:
            data = request.form
            print(session['lid'])
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "insert into complaint (complaint,lid,complaint_date) values (%s,%s,%s)"
            cursor.execute(
                query, (data['complaint'], session['lid'], datetime.now()))
            print(query)
            conn.commit()
            conn.close()
            flash(" Your complaint has been added  Successfully ")
            return render_template('customer_add_complaints.html')
        except Exception as e:
            flash("Something went Wrong !!!")
            return render_template('customer_add_complaints.html')


# -------------------------------------------------------------------------------

@app.route('/admin_reply_complaints', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def admin_reply_complaints():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from complaint")
        row = cursor.fetchall()
        print(row)
        conn.commit()
        conn.close()
        return render_template('admin_reply_complaints.html', result=row)
    
    if request.method == 'POST':
        if request.json is not None:
            print(request.json)
            data = request.json
            print(datetime.now())
            conn =mysql.connect()
            cursor = conn.cursor()
            q=" UPDATE complaint SET reply ='{}',reply_date ='{}' WHERE cmp_id='{}'"
            query= q.format(data['reply'], datetime.now(),data['cmp_id'])                    
            print(query)
            cursor.execute(query)
            conn.commit()
            conn.close()
            flash('Reply sended succesfully')
            return redirect(url_for('admin_reply_complaints'))
        else:
            flash('Reply sended succesfully')
            return redirect(url_for('admin_reply_complaints'))
    


# --------------------------------------------------------------------------------------------

@app.route('/view_complaint_reply', methods=['GET'])
@allow_for_loggined_users_only
def view_complaint_reply():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        # cursor.execute("SELECT complaint , reply ,reply_date FROM complaint")
        cursor.execute("select * from complaint where lid=%s", session['lid'])
        row = cursor.fetchall()
        # print(row)
        conn.commit()
        conn.close()
        return render_template('view_complaint_reply.html', result=row)

# ------------------------------------------------------------------------------------


@app.route('/admin_view_feedback', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def admin_view_feedback():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from feedback")
        row = cursor.fetchall()
        # print(row)
        conn.commit()
        conn.close()
        return render_template('admin_view_feedback.html', result=row)

# --------------------------------------addtocart----------------------------------------


@app.route('/addtocart', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def addtocart():
    if request.method == 'POST':
        data = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('select * from cart where pro_id=%s and usr_id=%s',
                       (data['pid'], session['lid']))
        dt = cursor.fetchone()
        subtotal = float(data['qnty'])*float(data['price'])
        shipping=(subtotal*0.35)
        print(shipping)
        total= shipping+subtotal
        
        if dt is None:
            # insert query
            query = "insert into cart (pro_id,qnty,shipping,subtotal,total,usr_id) values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(
                query, (data['pid'], data['qnty'], shipping, subtotal, total, session['lid']))
            conn.commit()
        else:
            qty = float(data['qnty'])+float(dt[2])
            total = qty*float(data['price'])
            cursor.execute("update cart set qnty=%s,total=%s where pro_id=%s and usr_id=%s",
                           (qty, total, data['pid'], session['lid']))
            conn.commit()
            print(qty, total)
            print(dt)
            conn.close()
        return redirect(url_for('customer_home'))

# -----------------------------------viewcart-------------------------------------------------


@app.route('/cart', methods=['GET', 'POST'])
@allow_for_loggined_users_only
def cart():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = " select login.lid,registration.*,pro_registration.*,cart.* from login , registration, pro_registration ,cart where login.lid=registration.lid and pro_registration.pid=cart.pro_id and registration.lid=cart.usr_id and registration.lid=%s"
        cursor.execute(query, (session['lid']))
        row = cursor.fetchall()
        conn = mysql.connect()
        cursor = conn.cursor()
        
        query = "select sum(shipping),sum(subtotal),sum(total) from cart where usr_id=%s"
        cursor.execute(query, (session['lid']))
        sum = cursor.fetchall()
        print(row)
        conn.close()
        return render_template('cart.html', row=row, sum=sum)
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from cart where crt_id=%s"
        cursor.execute(query, request.form.get('delete_by_id'))
        conn.commit()
        conn.close()

        return redirect(url_for('cart'))

# ------------------------payment-------------------------------------------


@app.route('/payment', methods=['POST', 'GET'])
@allow_for_loggined_users_only
def payment():
    if request.method == 'GET':
        return render_template("payment.html")

    if request.method == 'POST':
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "insert into payment(oid,amount,uid,card_holder_name,card_number,exp,payment_date)values(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query, (
                session['oid'],
                session['amnt'],
                session['lid'],
                request.form['card_holder_name'],
                request.form['card_number'],
                request.form['expiry'],
                datetime.now()
            ))
            conn.commit()
            cursor.execute(
                "update orders set pay_status='paid' where oid=%s", session['oid'])
            conn.commit()


            cursor.execute("select * from orderitem where oid=%s", session['oid'])
            data = cursor.fetchall()
            stock = 0
            total = 0
            for item in data:
                total += int(item[3])
                print(total)
                cursor.execute(
                    "select stock from pro_registration where pid=%s", item[1])
                dt = cursor.fetchone()
                print(dt)
                stock = int(dt[0])-int(item[3])
                print(stock)
                cursor.execute(
                    "update pro_registration set stock=%s where pid=%s", (stock, item[1]))
                conn.commit()
                cursor.execute("delete from cart where usr_id=%s", session['lid'])
                conn.commit()
                conn.close()

            return redirect(url_for('customer_view_current_order'))
        except Exception as e:
            flash(
            'Something went wrong, Check your card details is correct, then try again !!!')
        return redirect(url_for('payment'))


@app.route('/customer_view_current_order')
@allow_for_loggined_users_only
def customer_view_current_order():

    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        # query = " SELECT  registration.*, orderitem.*, orders.* from registration,orderitem ,orders where registration.lid=orders.l_id and orderitem.oid=%s"
        # query= " select * from orders where l_id=%s"
        # query = "SELECT  r.* ,o.*, i.qnty,i.total, p.pname ,p.price from orders o,orderitem i,pro_registration p,registration r where  i.oid=o.oid and o.l_id=r.lid and i.pid=p.pid and o.l_id=%s"
        query = "select p.pname,p.image,p.price,o.total,o.order_status from orderitem i,orders  o, pro_registration p where i.oid=o.oid and i.pid= p.pid and o.l_id=%s"
        cursor.execute(query, (session['lid']))
        row = cursor.fetchall()
        # flash('Payment Successfull !!!')
    return render_template("customer_view_current_order.html", row=row)

# ------------------------------------------------------------------------------------------------------


@app.route('/customer_view_order_item')
@allow_for_loggined_users_only
def customer_view_order_item():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select p.pname,p.image,p.price,o.total,o.order_status from orderitem i,orders  o, pro_registration p where i.oid=o.oid and o.order_status='delivered' and i.pid= p.pid and o.l_id=%s"
        cursor.execute(query, (session['lid']))
        row = cursor.fetchall()
    return render_template("customer_view_order_item.html", row=row)

# ------------------------------------------------------------------------------------------------------


@app.route('/packed', methods=['POST', 'GET'])
@allow_for_loggined_users_only
def packed():
    if request.method == 'GET':
        return render_template("farmer_view_customer_order.html")
    if request.method == 'POST':
        
            conn = mysql.connect()
            cursor = conn.cursor()
            # query="update orders set order_status='dispatched'where l_id=%s"
            # cursor.execute(query,session['lid'])
            cursor.execute(
                "update orders set order_status='packed' where oid=%s", request.form['oid'])
            conn.commit()
            conn.close()
            # flash(" Product Packed Successfully ")
            return redirect(url_for('farmer_view_customer_order'))
        


# ---------------------------------------------------------------------------------------------

@app.route('/dispatched', methods=['POST', 'GET'])
@allow_for_loggined_users_only
def dispatched():
    if request.method == 'GET':
        return render_template("agent_view_customer_orders.html")
    if request.method == 'POST':
        
            conn = mysql.connect()
            cursor = conn.cursor()
            # query="update orders set order_status='dispatched'where l_id=%s"
            # cursor.execute(query,session['lid'])
            cursor.execute(
                "update orders set order_status='dispatched' where oid=%s", request.form['oid'])
            conn.commit()
            conn.close()
            # flash(" Product Dispatched Successfully ")
            return redirect(url_for('agent_view_customer_orders'))


# ------------------------------------------------------------------------------------------------------------

@app.route('/delivered', methods=['POST', 'GET'])
@allow_for_loggined_users_only
def delivered():
    if request.method == 'GET':
        return render_template("agent_view_customer_orders.html")
    if request.method == 'POST':
        
            conn = mysql.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                "update orders set order_status='delivered' where oid=%s", request.form['oid'])
            # cursor.execute("update orders set status='dispatced' where oid=%s",session['oid'])
            conn.commit()
            conn.close()
            return redirect(url_for('agent_view_customer_orders'))
        


# ---------------order placing ---------->


@app.route('/create_order', methods=['POST'])
@allow_for_loggined_users_only
def create_order():

    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("select * from cart where usr_id=%s", session['lid'])
        data = cursor.fetchall()
        stock = 0
        total = 0
        for item in data:
            total += int(item[5])
            print(total)
            cursor.execute(
                "select stock from pro_registration where pid=%s", item[1])
            dt = cursor.fetchone()
            print(dt)
            stock = int(dt[0])-int(item[3])
            print(stock)
            # cursor.execute(
            #     "update pro_registration set stock=%s where pid=%s", (stock, item[1]))
            # conn.commit()

        cursor.execute("insert into orders (l_id,total,pay_status,date,order_status) values(%s,%s,%s,%s,%s)",
                    (session['lid'], total, 'pending', datetime.now(), 'Waiting for updates'))
        conn.commit()

        session['oid'] = cursor.lastrowid
        session['amnt'] = total

        for sub in data:
            cursor.execute("insert into orderitem(pid,oid,qnty,total)values(%s,%s,%s,%s)",
                        (sub[1], cursor.lastrowid, sub[2], sub[5]))
            conn.commit()

        # cursor.execute("delete from cart where usr_id=%s", session['lid'])
        # conn.commit()

        return redirect(url_for('payment'))


# -----------------------------------------------------------------------------

@app.route('/agent_view_customer_orders')
@allow_for_loggined_users_only
def agent_view_customer_orders():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT registration.*, orders.* from registration, orders where registration.lid=orders.l_id and orders.pay_status='paid' and orders.order_status='packed' and registration.pin=%s"
        cursor.execute(query, session['pin'])
        print(session)
        data = cursor.fetchall()
        conn.close()
        return render_template("agent_view_customer_orders.html", result=data)


@app.route('/agent_view_dispatched_orders')
@allow_for_loggined_users_only
def agent_view_dispatched_orders():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT registration.*, orders.* from registration, orders where registration.lid=orders.l_id and orders.pay_status='paid' and orders.order_status='dispatched' and registration.pin=%s"
        cursor.execute(query, session['pin'])
        data = cursor.fetchall()
        conn.close()
        return render_template("agent_view_dispatched_orders.html", result=data)


@app.route('/agent_view_delivered_orders')
@allow_for_loggined_users_only
def agent_view_delivered_orders():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT registration.*, orders.* from registration, orders where registration.lid=orders.l_id and orders.pay_status='paid' and orders.order_status='delivered' and registration.pin=%s"
        cursor.execute(query, session['pin'])
        data = cursor.fetchall()
        conn.close()
        return render_template("agent_view_delivered_orders.html", result=data)


@app.route('/farmer_view_customer_order', methods=['GET'])
@allow_for_loggined_users_only
def farmer_view_customer_order():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT  r.* ,o.*, i.qnty,i.total, p.pname ,p.price from orders o,orderitem i,pro_registration p,registration r where  o.pay_status='paid' and o.order_status='Waiting for updates' and i.oid=o.oid and o.l_id=r.lid and i.pid=p.pid and p.logid=%s"
        cursor.execute(query, session['lid'])
        row = cursor.fetchall()
        conn.close()
        return render_template("farmer_view_customer_order.html", result=row)


@app.route('/farmer_view_packed_items',methods=['GET'])
@allow_for_loggined_users_only
def farmer_view_packed_items():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        query="SELECT registration.*, pro_registration.*, orderitem.*, orders.* from registration, orders ,pro_registration,orderitem where orders.oid=orderitem.oid and orderitem.pid=pro_registration.pid and registration.lid=orders.l_id and orders.pay_status='paid' and orders.order_status='packed' and registration.pin=%s"
        # query= "SELECT registration.*, orders.* from registration, orders where registration.lid=orders.l_id and orders.pay_status='paid' and orders.order_status='packed' and registration.pin=%s"
        cursor.execute(query, session['pin'])
        row = cursor.fetchall()
        conn.close()
        return render_template("farmer_view_packed_items.html",result=row)


if __name__ == '__main__':
    app.run(debug=True)
