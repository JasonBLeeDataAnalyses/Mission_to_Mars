# Flask application
# Create a route called /scrape that will import your scrape_mars.py script and call your  scrape function

# Dependencies
from scrape_mars import scrape
from flask_pymongo import PyMongo
from flask import Flask, render_template, jsonify, redirect

# Create flask app
app = Flask(__name__)

# Connect to MongoDB
# conn = "mongodb://localhost:27017"
mongo = PyMongo(app)

# # Use database and create it
# db = mongo.marsdataDB
# collection = db.marsdata

# marsdata = list(db.marsdata.find())
# print(marsdata)

# Create root/index route to query mongoDB and pass mars data to HTML template to display data
@app.route('/')
def index():
    marsdata = mongo.db.mars.find_one()
    # print(marsdata)
    return render_template('index.html', marsdata=marsdata)

# Create route called /scrape
@app.route('/scrape')
def scrape_mars_data():
    marsdata = scrape()
    mars_db = mongo.db.mars
    mars_db.update(
        {},
        marsdata,
        upsert=True
    )
    return redirect('http://localhost:5000/', code=302)

if __name__ == '__main__':
    app.run(debug=True)