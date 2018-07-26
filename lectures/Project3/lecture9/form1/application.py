from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/form", methods=["POST"])
def form():
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("user.html", u = username)

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
