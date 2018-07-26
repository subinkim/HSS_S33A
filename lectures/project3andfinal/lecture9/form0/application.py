from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/form", methods=["POST"])
def form():
    username = request.form.get("username")
    return render_template("user.html", u = username)

if __name__ == "__main__":
    with app.app_context():
        app.run()
