from flask import Flask, render_template, request, redirect, Blueprint
import mysql.connector

from CreateAc import Crt_acc
from login import login_bp

app = Flask(__name__)

# Create a connection
conn = mysql.connector.connect(
    host='localhost',
    database='form',
    user='Tomal',
    password='Tomal@01764'
)


# Check if the connection was successful


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
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


app.register_blueprint(login_bp)


@app.route('/home.html')
def home():
    return render_template('home.html')


@app.route('/success')
def success():
    return render_template('success.html')


app.register_blueprint(Crt_acc)


if __name__ == '__main__':
    app.run()
