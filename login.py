import mysql.connector
from flask import Blueprint, render_template, request, redirect, url_for

login_bp = Blueprint('login', __name__)

conn = mysql.connector.connect(
    host='localhost',
    database='form',
    user='Tomal',
    password='Tomal@01764'
)


@login_bp.route('/login.html')
def login():
    return render_template('/login.html')


@login_bp.route('/login.html', methods=['post'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')
    #admin = 'admin' in request.form.get()

    # Perform authentication and authorization
    if conn.is_connected():
        cursor = conn.cursor()
        query = "SELECT * FROM user WHERE email = %s AND passwod = %s"
        values = (username, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        cursor.close()

        if user:
            # If authentication is successful, redirect to the home page
            return render_template('/index.html')
        else:
            # Authentication failed, display an error message
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@login_bp.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    message = request.form.get('message')

    if conn.is_connected():
        myco = conn.cursor()

        sql = "INSERT INTO comments (email, message) VALUES (%s, %s)"
        val = (email, message)

        myco.execute(sql, val)

        conn.commit()

        # Close the cursor
        myco.close()

    # Close the connection
    conn.close()

    return redirect('/success')
