from flask import Flask,request,render_template,redirect,url_for,session
from flask_socketio import SocketIO,emit
import secrets
# real time , server to client 

from werkzeug.security import generate_password_hash,check_password_hash

# x = generate_password_hash("mmdrezaw")
# print(check_password_hash(x,'mmdrezaw'))

app = Flask(__name__)
socketio = SocketIO(app)

users = {}
@app.route('/register',methods = ['POST','GET']) 
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if username in users:
            error = 'نام کاربری قبلا ثبت شده است!'
        elif password != confirm_password:
            error = 'رمز عبور مطابقت ندارد'
        else:
            users[username] = {
                'username': username,
                'password': generate_password_hash(password),
            }
            return redirect(url_for('login'))
        return render_template('register.html',error=error)

    return render_template('register.html')


@app.route('/login',methods = ['POST','GET']) 
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'] ,password):
            session['username'] = username
            print('success')
            return redirect(url_for('index'))
        error = "نام کاربری یا رمز عبور اشتباه است"
        print('error')
        return render_template('login.html',error = error)

    return render_template('login.html')

@app.route('/logout',) 
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/',) 
def index():
    if 'username' in session:
        return render_template('index.html',username = session['username'])
    return redirect(url_for('login'))

# def controlgar event message in html
@socketio.on('message')
def handle_message(message):
    emit('message',{'username':session['username'],'message':message},broadcast=True)
    
if __name__ == '__main__':
    app.secret_key = secrets.token_urlsafe(16)
    socketio.run(app,debug=True)