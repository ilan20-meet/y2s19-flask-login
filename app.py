from databases import *
from flask import Flask, request, redirect, render_template
from flask import session as login_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/')
def home():

    if 'logged_in' in login_session and login_session['logged_in'] == True:
        return render_template('home.html', fav_food=get_user(login_session['name']).fav_food)
    else:
        return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    user = get_user(request.form['username'])
    if user != None and user.verify_password(request.form["password"]):
        login_session['name'] = user.username
        login_session['logged_in'] = True
        return render_template("logged.html", fav_food=get_user(login_session['name']).fav_food)
    else:
        return home()


@app.route('/signup', methods=['POST'])
def signup():
    #check that username isn't already taken
    user = get_user(request.form['username'])
    if user == None: 
        add_user(request.form['username'],request.form['password'])
    return home()


@app.route('/logged-in', methods=["GET", "POST"])
def logged_in():
    if request.method == 'POST':
        update_food(login_session['name'], request.form['fav_food'])
    return render_template('logged.html', fav_food=get_user(login_session['name']).fav_food)


@app.route('/logout')
def logout():
    login_session.clear()
    return home()



if __name__ == '__main__':
    app.run(debug=True)
