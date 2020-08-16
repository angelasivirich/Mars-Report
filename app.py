from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_tomars

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mars_info = mongo.db.mars.find_one()
    return render_template("index.html", mars_info = mars_info)


@app.route("/scrape")
def scrape():
    mars_data = mission_tomars.scrape()
    mongo.db.mars.update({}, mars_data, upsert = True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)