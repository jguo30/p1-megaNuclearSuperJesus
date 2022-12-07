

from flask import Flask, render_template, request
import requests

app = app = Flask(__name__)      
@app.route("/", methods = ["POST", "GET"])                   
def display():
    return render_template("main.html")

if __name__ == "__main__": 
    app.debug = True                                                                                                        
    app.run()      

