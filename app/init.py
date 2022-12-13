from flask import Flask, render_template, request, Response, session
from db import add_to_db, in_table, correct_passwd
import requests
import calendar
code = 7997
app = app = Flask(__name__)      
app.secret_key = "6gBvzKwE8RWOt6amHzNz"

month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

@app.route("/", methods = ["POST", "GET"])                   
def display():
    return render_template("main.html")

@app.route("/results", methods = ["POST", "GET"])
def results():

    collegeBase = "https://api.data.gov/ed/collegescorecard/v1/schools.json?"
    schoolAddon = collegeBase + "school.name="
    schoolAddon += request.form["College"]
    schoolAddon += "&school.main_campus=1"
    fields0 = "&fields=school.name,location.lat,location.lon,2020.student.size"
    apiKey = "&api_key=U5nqzYuypTfafBJkGiHwhNU10dXdtO36S8isJeUi"
    finalURL = schoolAddon + fields0+apiKey
    print(finalURL)
    r = requests.get(finalURL)
    data = r.json()
    #Bing maps stuff
    lat = float(data["results"][0]["location.lat"])
    lon = float(data["results"][0]["location.lon"])
    dist = 50
    code = 7997
    #code = int(request.form["Code"])
    num = 5

    url = f'http://dev.virtualearth.net/REST/v1/Routes/LocalInsights?waypoint={lat},{lon}&maxTime=60&timeUnit=minute&type=SeeDo&key=Aq5RfNwj-YFePBBwOI4Dz18rk5AcP_hJ9BcR8g91kQUZNzWY_eNYJT3f79zkfHU0'
    #url = f'http://spatial.virtualearth.net/REST/v1/data/Microsoft/PointsOfInterest?spatialFilter=nearby({lat},{lon},{dist})&$filter=EntityTypeID%20eq%20%27{code}%27&$select=EntityID,DisplayName,Latitude,Longitude,__Distance&$top={num}&$format=json&key=Aq5RfNwj-YFePBBwOI4Dz18rk5AcP_hJ9BcR8g91kQUZNzWY_eNYJT3f79zkfHU0'

    print(url)
    r = requests.get(url)
    print("Bing maps printing...")
    print(r.text)
    data = r.json()
    results = []
    print("_____________________________")
    #for i in data["d"]["results"]:
    for i in data["resourceSets"][0]["resources"][0]["categoryTypeResults"][0]["entities"]:
        #print(i)
        results.append(i["entityName"])
        #print(i["DisplayName"])
    #weather stuff
    weatherUrl = f'https://archive-api.open-meteo.com/v1/era5?latitude={lat}&longitude={lon}&start_date=2021-01-01&end_date=2021-12-31&daily=temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York&temperature_unit=fahrenheit&windspeed_unit=mph'
    r = requests.get(weatherUrl)
    data = r.json()
    weather_results = [[] for i in range(12)]
    months = []
    for i in range(365):
        max = float(data["daily"]["temperature_2m_max"][i])
        min = float(data["daily"]["temperature_2m_min"][i])
        date = data["daily"]["time"][i]
        #print(date)
        mon = int(date[5:7])
        #print(mon)
        mid = (max + min) / 2
        weather_results[mon-1].append(mid)
    #print(weather_results)
    for i in range(12):
        average = sum(weather_results[i]) / len(weather_results[i])
        months.append(round(average,1))
    print(months)
    return render_template("results.html", poi = results, weath = months, mons = month_list)
    
@app.route("/code", methods = ["POST", "GET"])                   
def code():
    code = int(request.form["Code"])
    return redirect("/")

@app.route("/register", methods = ["POST","GET"])
def reg():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        print("\n\n\n")
        print("***DIAG: this Flask obj ***")
        print(app)
        print("***DIAG: request obj ***")
        print(request)
        print("***DIAG: request.args ***")
        print(request.form)
        print("***DIAG: request.args['username']  ***")
        print(request.form['register_username'])
        print("***DIAG: request.headers ***")
        if add_to_db(request.form['register_username'],request.form['register_pswd']):
            return render_template('home.html')
        else:
            return render_template('register.html',message="Username already exists")
    return Response(status=405)

@app.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        print("\n\n\n")
        print("***DIAG: this Flask obj ***")
        print(app)
        print("***DIAG: request obj ***")
        print(request)
        print("***DIAG: request.args ***")
        print(request.form)  # displays entered info as dict
        print("***DIAG: request.args['username']  ***")
        print(request.form['user_name'])
        print("***DIAG: request.headers ***")
        username = request.form['user_name']
        passwd = request.form['pass_word']
        if(in_table(username)):
            if correct_passwd(username,passwd):
                session[username] = username
                return render_template("home.html")
            else:
                return render_template("login.html",message="Password is incorrect")
        else:
            return render_template("login.html",message="Username not found")
        
@app.route("/home", methods = ["POST","GET"])
def home():

    return render_template('home.html')

if __name__ == "__main__": 
    app.debug = True                                                                                                        
    app.run()      

