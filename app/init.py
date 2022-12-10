from flask import Flask, render_template, request
import requests
code = 7997
app = app = Flask(__name__)      
@app.route("/", methods = ["POST", "GET"])                   
def display():
    return render_template("main.html")

@app.route("/results", methods = ["POST", "GET"])
def results():
    lat = float(request.form["Lat"])
    lon = float(request.form["Long"])
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

    # weatherUrl = f'https://archive-api.open-meteo.com/v1/era5?latitude={lat}&longitude={lon}&start_date=2021-01-01&end_date=2021-12-31&daily=temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York&temperature_unit=fahrenheit&windspeed_unit=mph'
    # r = requests.get(weatherUrl)
    # data = r.json()
    # weather_results = [[] for i in range(12)]
    # months = []
    # for i in range(365):
    #     max = float(data["daily"]["temperature_2m_max"][i])
    #     min = float(data["daily"]["temperature_2m_min"][i])
    #     date = data["daily"]["time"][i]
    #     print(date)
    #     mon = int(date[5:7])
    #     #print(mon)
    #     mid = (max + min) / 2
    #     weather_results[mon].append(mid)
    # print(weather_results)
    # for i in range(12):
    #     average = sum(weather_results[i]) / len(weather_results[i])
    #     months.append(average)

    return render_template("results.html", poi = results)
    
@app.route("/code", methods = ["POST", "GET"])                   
def code():
    code = int(request.form["Code"])
    return redirect("/")

@app.route("/register", methods = ["POST","GET"])
def reg():
    if request.method == "GET":
        return render_template("register.html")
    elif request.methid == "POST":
        

if __name__ == "__main__": 
    app.debug = True                                                                                                        
    app.run()      

