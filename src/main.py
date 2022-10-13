from click import password_option
from flask import Flask, request, session, flash, redirect, url_for, render_template
import db

app = Flask(__name__)
app.secret_key = 'super secret key'

# Opret tabeller i database
db.db_setup()

@app.get("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("index"))

    if request.method == "POST":
        if session.get("username"):
            return redirect(url_for("index"))

        username = request.form.get("username")
        password = request.form.get("password")
        if db.check_user(username, password):
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("Forkert brugernavn eller kodeord!")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("username"):
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not username or not password:
            flash("Udfyld venligst alle felter!")
        elif password != confirm:
            flash('Kodeordene er ikke ens!')
        elif len(username) < 3:
            flash('Brugernavnet skal være længere end 3 tegn!')
        elif len(username) > 20:
            flash('Brugernavnet skal være kortere end 20 tegn!')
        elif len(password) < 8:
            flash('Kodeordet skal være længere end 8 tegn!')
        elif len(password) > 50:
            flash('Kodeordet skal være kortere end 50 tegn!')
        elif db.get_user(request.form['username']):
            flash('Brugernavn allerede i brug')
        else:
            db.add_user(username, password)
            flash('Bruger oprettet, du kan nu logge ind')
            return redirect(url_for("login"))

    return render_template("register.html")


@app.get("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.get("/download")
def download():
    username = session.get("username")
    if not username:
        flash("Du skal være logget ind for at hente spillet!")
        return redirect(url_for("login"))

    license_ = db.get_license(username)

    return render_template("download.html", license_=license_, username=username)

if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
