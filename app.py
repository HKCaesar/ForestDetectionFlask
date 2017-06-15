#our web app framework!

#you could also generate a skeleton from scratch via
#http://flask-appbuilder.readthedocs.io/en/latest/installation.html

#Generating HTML from within Python is not fun, and actually pretty cumbersome because you have to do the
#HTML escaping on your own to keep the application secure. Because of that Flask configures the Jinja2 template engine 
#for you automatically.
#requests are objects that flask handles (get set post, etc)
from flask import Flask, render_template,request
#for importing our keras model
import keras.models
#for reading operating system data
import os

from load import * 
from predict import * 
#initalize our flask app
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#global vars for easy reusability
global model
#initialize these variables
model = init()

@app.route('/')
def index():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
	target = APP_ROOT
	print(request.files.getlist("file"))
	for upload in request.files.getlist("file"):
		print(upload)
		print("{} is the file name".format(upload.filename))
		filename = upload.filename
		destination = "/".join([target, "temp.jpg"])
		print ("Accept incoming file:", filename)
		print ("Save it to:", destination)
		upload.save("temp.jpg")
	makePrediction(destination, model)
	return render_template("uploaded.html")
	
@app.after_request
def add_header(response):
	"""
	Add headers to both force latest IE rendering engine or Chrome Frame,
	and also to cache the rendered page for 10 minutes.
	"""
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers['Cache-Control'] = 'public, max-age=0'
	return response
	
if __name__ == "__main__":
	#decide what port to run the app in
	port = int(os.environ.get('PORT', 5000))
	#run the app locally on the givn port
	app.run(host='0.0.0.0', port=port)
	#optional if we want to run in debugging mode
	app.run(debug=False)
