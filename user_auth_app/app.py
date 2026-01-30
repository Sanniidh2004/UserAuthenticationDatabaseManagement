from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "sanni123"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sanni123'
app.config['MYSQL_DB'] = 'user_auth_db'


mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/dashboard')
        else:
            return "Invalid username or password"

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        roll = request.form['roll']
        address = request.form['address']

        if password != confirm:
            return "Passwords do not match"

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO users
            (username, password, name, email, phone, roll_no, address)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (username, hashed_password, name, email, phone, roll, address))
        mysql.connection.commit()
        cur.close()

        return redirect('/')

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT name, email, phone, roll_no, address
        FROM users
        WHERE id = %s
    """, (session['user_id'],))
    user = cur.fetchone()

    cur.execute("""
        SELECT subject, marks, grade
        FROM grades
        WHERE user_id = %s
    """, (session['user_id'],))
    grades = cur.fetchall()

    cur.close()

    return render_template(
        'dashboard.html',
        username=session['username'],
        user=user,
        grades=grades
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)


