from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

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
    nom = db.Column(db.String, unique=True)
    pastille = db.Column(db.String)
    description = db.Column(db.String)


@app.route("/")
def show_all():
   return render_template('webapp/list_user.html', Webapp=Webapp.query.all())

@app.route("/solistatus")
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


@app.route('/solistatus/<int:id>', methods=['PUT'])
def webapp_update(id):
    webapp = Webapp.query.get(id)
    if request.method == "PUT":
        webapp.nom = request.form["nom"]
        webapp.pastille = request.form["pastille"]
        webapp.description = request.form["description"]
        db.session.commit()
    return redirect(url_for('webapp_list'))


@app.route("/solistatus/<int:id>/delete", methods=["GET", "POST"])
def webapp_delete(id):
    webapps = db.get_or_404(Webapp, id)

    if request.method == "POST":
        db.session.delete(webapps)
        db.session.commit()
        return redirect(url_for("/solistatus"))

    return render_template("webapp/delete.html", webapps=webapps)
