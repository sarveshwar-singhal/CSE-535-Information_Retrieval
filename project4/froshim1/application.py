from flask import Flask, render_template, request, redirect

app = Flask(__name__)

students=[]

@app.route('/')
def index():
    return render_template("try1_index.html")

@app.route('/registrants')
def registrants():
    return render_template("register.html", students=students)

@app.route('/register', methods=["POST"])
def register():
    name = request.form.get("name")
    dorm = request.form.get("dorm")
    if not name or not dorm:
        pass
    else:
        students.append(f'{name} from {dorm}')
        return redirect('/registrants')


if __name__ == '__main__':
    app.run(debug=True)