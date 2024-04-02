from flask import Flask,request,render_template,redirect,url_for,flash,abort
import mysql.connector
from flask_session import Session
from flask_bcrypt import Bcrypt
from dmail import sendmail
from Stoken import token
from itsdangerous import URLSafeTimedSerializer
from key import secret_key,salt1,salt2
#kzxw bjoj lapa zjev

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = secret_key
app.config['SESSION_TYPE']='filesystem'

mydb = mysql.connector.connect(host='localhost',user='root',password='root',database='user')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        Name = request.form['name']
        Mail = request.form['email']
        Pwd = request.form['password']
        pwd = bcrypt.generate_password_hash(Pwd)
        Phone = request.form['phone']
        Place = request.form['place']
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select Email from user where Email=%s',[Mail])
        count = cursor.fetchone()
        #print(count)
        cursor.close()
        if count == 1:
            flash('Email Already In use')
            return render_template('register.html')
        userinfo = {'name':Name,'mail':Mail,'pwd':Pwd,'ph':Phone,'place':Place}
        subject='Email Authentication'        
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('confirm',token=token(userinfo,salt=salt1),_external=True)}"
        sendmail(to=Mail,subject=subject,body=body)
        flash('Confirmation link sent to ur registred mail')
        return render_template('register.html')
    return render_template('register.html')

@app.route('/confirm/<token>')
def confirm(token):
    try :
        datta = URLSafeTimedSerializer(secret_key)
        userinfo = datta.loads(token,salt=salt1,max_age=200)
    except Exception as e:
        #print(e)
        return 'sorry this link expiredddd plz register after somettime Have a Good Day'
    else:
        cursor = mydb.cursor(buffered=True)
        cursor.execute('insert into user(Name,Email,pwd,phno,place) values(%s,%s,%s,%s,%s)',[userinfo['name'],userinfo['mail'],userinfo['pwd'],userinfo['ph'],userinfo['place']])
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['D@TT@']
        pwd = request.form['pwd']
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select email,pwd from user where email=%s',[Email])
        e_mail,passwrd = cursor.fetchone()
        cursor.close()
        if email == e_mail and pwd == password:
            #return [e_mail,pwd]
            return redirect(url_for('Dashboard'))
        else:
            flash('Invalide Username & password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/Dashboard')
def Dashboard():
    return render_template('Dashboard.html')

@app.route('/reset',methods=['GET','POST'])
def reset():
    if request.method == 'POST':
        mail = request.form['email']
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select count(*) from user where Email=%s',[mail])
        count = cursor.fetchone()[0]
        # print('----------',count)
        cursor.close()
        if count == 1:
            subject='Reset password link'        
            body=f"your reset password link\n\nfollow this link takes for next step-{url_for('forgot',token=token(mail,salt=salt2),_external=True)}"
            sendmail(to=mail,subject=subject,body=body)
            flash('Reset link sended to ur Mail')
            return redirect(url_for('reset'))
    return render_template('reset.html')

@app.route('/forgot/<token>',methods=['GET','POST'])
def forgot(token):
    try :
        ram = URLSafeTimedSerializer(secret_key)
        user = ram.loads(token,salt=salt2,max_age=200)
    except Exception as e:
        # print(e)
        abort(404, 'This link expiredddd.....!')
    else:
        if request.method == 'POST':
            newpwd = request.form['npwd']
            confirmpwd = request.form['cpwd']
            if newpwd == confirmpwd:
                cursor = mydb.cursor(buffered=True)
                cursor.execute('update user set pwd=%s where Email=%s',[newpwd,user])
                mydb.commit()
                cursor.close()
                flash('Password successfully updated...!' )
                return redirect(url_for('login'))
            else:
                flash('Password mismatched....!')
                return render_template('forgot.html')
    return render_template('forgot.html')


app.run(use_reloader=True,debug=True)