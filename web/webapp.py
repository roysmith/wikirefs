import secrets

from bs4 import BeautifulSoup
import flask
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from pywikibot import Site, Page
from wtforms import StringField
from wtforms.validators import DataRequired

import wikirefs

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex()


@app.route("/", methods=["GET", "POST"])
def index():
    form = PageForm(request.form)
    if request.method == "POST" and form.validate():
        page_title = form.page_title.data
        return redirect(url_for("show", page_title=page_title))
    return render_template("page_form.html", form=form)


@app.route("/show")
def show():
    site = Site("en")
    page = Page(site, request.args.get("page_title"))
    soup = BeautifulSoup(page.get_parsed_page(), features="lxml")
    statements = wikirefs.get_statements(soup)
    return render_template("show.html", statements=statements)


class PageForm(FlaskForm):
    page_title = StringField("page_title", validators=[DataRequired()])
