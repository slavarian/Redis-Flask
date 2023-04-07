from flask import Flask, render_template, request, redirect, url_for, session
import redis

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        r.set('users', username)
        r.set('pass', password)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if r.get('users') == username and r.get('pass') == password:
            session['users'] = username
            return redirect(url_for('profile'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')


@app.route('/profile')
def profile():
    if 'users' in session:
        username = session['users']
        password = r.get('pass')
        return render_template('profile.html', username=username, password=password)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('users', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host="localhost", port=8080,
            debug=True)
