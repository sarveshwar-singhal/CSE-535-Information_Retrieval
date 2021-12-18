from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    # return "Hello World"
    name = request.args.get("name", "world")
    return render_template("try1_index.html", name=name)

@app.route("/register", methods=["POST"])
def register():
    #name = request.args.get("name") #forms sends through get are fetched using .args
    #dorm = request.args.get("dorm") #forms send through post are fetched using .forms.get
    name = request.form.get("name")
    dorm = request.form.get('dorm')
    if not name or not dorm:
        return render_template("failure.html")
    else:
        return render_template("success.html")

if __name__ == '__main__':
    app.run(debug=True)