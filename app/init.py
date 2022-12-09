from flask import Flask, render_template, request
import requests
code = 7997
app = app = Flask(__name__)      
@app.route("/", methods = ["POST", "GET"])                   
def display():
    return render_template("main.html")
@app.route("/results", methods = ["POST", "GET"])
def results():
    lat = 40
    lon = -74
    dist = 50
    code = int(request.form["Code"])
    num = 5

    url = f'http://spatial.virtualearth.net/REST/v1/data/Microsoft/PointsOfInterest?spatialFilter=nearby({lat},{lon},{dist})&$filter=EntityTypeID%20eq%20%27{code}%27&$select=EntityID,DisplayName,Latitude,Longitude,__Distance&$top={num}&$format=json&key=Aq5RfNwj-YFePBBwOI4Dz18rk5AcP_hJ9BcR8g91kQUZNzWY_eNYJT3f79zkfHU0'
    print(url)
    r = requests.get(url)
    print(r.headers)
    print(r.text)
    data = r.json()
    results = []
    print("_____________________________")
    for i in data["d"]["results"]:
        #print(i)
        results.append(i["DisplayName"])
        #print(i["DisplayName"])
    return render_template("results.html", poi = results)
@app.route("/code", methods = ["POST", "GET"])                   
def code():
    code = int(request.form["Code"])
    return redirect("/")

if __name__ == "__main__": 
    app.debug = True                                                                                                        
    app.run()      

