from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import time

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///web_solinest.db"
# initialize the app with the extension
db.init_app(app)


class Webapp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String)
    pastille = db.Column(db.String)
    description = db.Column(db.String)
    update_time = db.Column(
        db.String, default=time.strftime("%m-%d-%Y %H:%M"))


with app.app_context():
    db.create_all()


@app.route("/solistatus")
def show_all():
    webapps = db.session.execute(
        db.select(Webapp).order_by(Webapp.nom)).scalars()
    return render_template("webapp/list_user.html", webapps=webapps)


@app.route("/admin")
def webapp_list():
    webapps = db.session.execute(
        db.select(Webapp).order_by(Webapp.nom)).scalars()
    return render_template("webapp/list.html", webapps=webapps)


@app.route("/solistatus/create", methods=["GET", "POST"])
def webapp_create():
    if request.method == "POST":
        webapps = Webapp(
            nom=request.form["nom"],
            pastille=request.form["pastille"],
            description=request.form["description"]
        )
        db.session.add(webapps)
        db.session.commit()
    return render_template("webapp/create.html")


@app.route("/solistatus/update/<int:id>", methods=["GET", "POST"])
def webapp_update(id):
    webapp = Webapp.query.get(id)
    if request.method == "POST":
        webapp.nom = request.form["nom"]
        webapp.pastille = request.form["pastille"]
        webapp.description = request.form["description"]
        webapp.update_time = time.strftime("%m-%d-%Y %H:%M")
        db.session.commit()
    return render_template("webapp/update.html", webapp=webapp)



@app.route("/solistatus/<int:id>/delete", methods=["GET"])
def webapp_delete(id):
    webapps = Webapp.query.get(id)
    db.session.delete(webapps)
    db.session.commit()
    return redirect(url_for('webapp_list'))
