from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector


Crt_acc = Blueprint('createAcc', __name__)

conn = mysql.connector.connect(
    host='localhost',
    database='form',
    user='Tomal',
    password='Tomal@01764'
)


@Crt_acc.route('/createAcc.html')
def create_account():
    return render_template('createAcc.html')


@Crt_acc.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    cursor = conn.cursor()
    query = "SELECT * FROM user WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return render_template('createAcc.html', error='Email already exists')

    if password != confirm_password:
        return render_template('createAcc.html', error='Passwords do not match')

    cursor = conn.cursor()
    query = "INSERT INTO user (name, email, phone, passwod) VALUES (%s, %s, %s, %s)"
    values = (name, email, phone, password)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()

    return redirect('/login.html')


@Crt_acc.route('/submit', methods=['POST'])
def submit():
    emails = request.form.get('email')
    message = request.form.get('message')

    if conn.is_connected():
        myco = conn.cursor()

        sql = "INSERT INTO comments (email, message) VALUES (%s, %s)"
        val = (emails, message)

        myco.execute(sql, val)

        conn.commit()

        myco.close()

    conn.close()

    return redirect('/success')
