from pathlib import Path

import pandas as pd
from flask import Flask, redirect, render_template, url_for
from loguru import logger

from dash_app import create_dash_app
from src.load_sql import load_database

app = Flask(__name__)

# Load the dataset
df = load_database()
logger.info(f"Column names: {df.columns}")
 
# Serve the Dash app
dash_app = create_dash_app(app)


# Define Flask routes
@app.route("/")
def welcome_redirect():
    return redirect(url_for("welcome"))


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/barchart")
def show_barchart():
    filtered_df = df[df["Total"].notnull()]
    countries = filtered_df["Country"].tolist()
    ratings = filtered_df["Total"].tolist()
    return render_template("barchart.html", countries=countries, ratings=ratings)



@app.route("/FAQ")
def faq_page():
    return render_template("FAQ.html")

@app.route("/data")
def data_page():
    return render_template("data.html")



@app.route("/dash")
def render_dash():
    return redirect("/dash/")

@app.route("/charts")
def charts_page():
    return render_template("charts.html")

if __name__ == "__main__":
    app.run(debug=True)
