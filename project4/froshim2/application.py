from flask import Flask, render_template, request, redirect
import os
import smtplib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("try1_index.html")


@app.route('/register', methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    email = 'scpl.singhal@gmail.com'
    dorm = request.form.get("dorm")
    if not name or not dorm or not email:
        return render_template("failure.html")
    message = "you're registered"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('sgi.singhal@gmail.com', os.getenv("PASSWORD"))
    server.sendmail('sgi.singhal@gmail.com', email, message)
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)