from flask import Flask, render_template, request, Response, session, redirect
from db import add_to_db, in_table, correct_passwd, pw_confirm
import requests
import calendar
import random
import os
code = 7997
app = Flask(__name__)
app.secret_key = "6gBvzKwE8RWOt6amHzNz"

month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './js/home.js')


@app.route("/", methods = ["POST", "GET"])
def display():
    return render_template("main.html")

@app.route("/results", methods = ["POST", "GET"])
def results():
    wd = os.path.dirname(os.path.realpath(__file__))
    file = open(wd + "/keys/key_bing.txt", "r")
    bingKey = file.read()
    print(bingKey)
    file.close()
    file = open(wd + "/keys/key_college.txt", "r")
    collegeKey = file.read()
    print(collegeKey)
    file.close()

    collegeBase = "https://api.data.gov/ed/collegescorecard/v1/schools.json?"
    schoolAddon = collegeBase + "school.name="
    schoolAddon += request.args["College"]
    schoolAddon += "&school.main_campus=1"
    fields0 = "&fields=school.name,location.lat,location.lon,2020.student.size,school.degree_urbanization,student.demographics.female_share"
    #apiKey = "&api_key=U5nqzYuypTfafBJkGiHwhNU10dXdtO36S8isJeUi"
    finalURL = schoolAddon + fields0+ "&api_key=" + collegeKey
    print(finalURL)
    r = requests.get(finalURL)
    data = r.json()
    college_name = data["results"][0]["school.name"]
    #Bing maps stuff
    lat = float(data["results"][0]["location.lat"])
    lon = float(data["results"][0]["location.lon"])
    dist = 50
    code = 7997
    #code = int(request.form["Code"])
    num = 5
    if (lon > -74.8 and lon < -73.3 and lat < 41.5209 and lat > 40.3209):
        maxTime = 15
    else:
        maxTime = 60

    url = f'http://dev.virtualearth.net/REST/v1/Routes/LocalInsights?waypoint={lat},{lon}&maxTime={maxTime}&timeUnit=minute&type=Restaurants,Museums,Attractions,Parks,Bookstores&key={bingKey}'
    #url = f'http://spatial.virtualearth.net/REST/v1/data/Microsoft/PointsOfInterest?spatialFilter=nearby({lat},{lon},{dist})&$filter=EntityTypeID%20eq%20%27{code}%27&$select=EntityID,DisplayName,Latitude,Longitude,__Distance&$top={num}&$format=json&key=Aq5RfNwj-YFePBBwOI4Dz18rk5AcP_hJ9BcR8g91kQUZNzWY_eNYJT3f79zkfHU0'

    print(url)
    r = requests.get(url)
    print("Bing maps printing...")
    print(r.text)
    data = r.json()
    results = []
    print("_____________________________")
    #for i in data["d"]["results"]:
    for i in data["resourceSets"][0]["resources"][0]["categoryTypeResults"]:#[0]["entities"]:
        count = 0
        #print(i)
        if i["entities"] != []:
            for j in i["entities"]:
                count += 1
            rand = random.randint(1,count)
            print(rand)
            results.append(i["entities"][rand-1]["entityName"])
            #print(i["DisplayName"])
    #weather stuff
    weatherUrl = f'https://archive-api.open-meteo.com/v1/era5?latitude={lat}&longitude={lon}&start_date=2021-01-01&end_date=2021-12-31&daily=temperature_2m_max,temperature_2m_min,rain_sum,snowfall_sum&timezone=America%2FNew_York&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
    r = requests.get(weatherUrl)
    data = r.json()
    weather_results = [[] for i in range(12)]
    months = []
    for i in range(365):
        max = float(data["daily"]["temperature_2m_max"][i])
        min = float(data["daily"]["temperature_2m_min"][i])
        rain = float(data["daily"]["rain_sum"][i])
        snow = float(data["daily"]["snowfall_sum"][i])
        date = data["daily"]["time"][i]
        #print(date)
        mon = int(date[5:7])
        #print(mon)
        mid = (max + min) / 2
        weather_results[mon-1].append((mid,rain,snow))
    #print(weather_results)
    for i in range(12):
        le = len(weather_results[i])
        print(le)
        average = 0
        average2 = 0
        average3 = 0
        for j in range(le):
            #print(weather_results[i])
            #print(weather_results[i][j][0])
            average += weather_results[i][j][0]
            average2 += weather_results[i][j][1]
            average3 += weather_results[i][j][2]
        #average = sum(weather_results[i][0]) / le
        #average2 = sum(weather_results[i][1])
        #average3 = sum(weather_results[i][2])
        average /= le
        months.append((round(average,1),round(average2,1),round(average3,1)))
    print(months)
    #Route info
    url = f'http://dev.virtualearth.net/REST/v1/Routes/Driving?wayPoint.1=40.7178,-74.0138&wayPoint.2={lat},{lon}&optimize=time&avoid=borderCrossing&routeAttributes=transitStops&timeType=departure&dateTime=08/24/2023%2009:42:00&distanceUnit=mi&key={bingKey}'
    print(url)
    r = requests.get(url)
    data = r.json()
    #things = data["resourceSets"][0]["resources"]
    dur = data["resourceSets"][0]["resources"][0]["travelDurationTraffic"]
    dur /= 3600
    dist = data["resourceSets"][0]["resources"][0]["travelDistance"]
    tup = (round(dist,2), round(dur,2))
    gas0 = f'https://www.gasbuddy.com/gaspricemap/county?lat=40.7178&lng=-74.0138&usa=true'
    gas1 = f'https://www.gasbuddy.com/gaspricemap/county?lat={lat}&lng={lon}&usa=true'
    r = requests.post(gas0)
    data = r.json()
    price0 = data[0]["Price"]
    print(data[0]["Price"])
    r = requests.post(gas1)
    data = r.json()
    price1 = data[0]["Price"]
    print(data[0]["Price"])
    gasAv = (float(price0) + float(price1)) / 2.0
    totalGas = round((float(dist) / 24.2) * gasAv,2)
    iUrl = f'https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerialwithlabels/Routes/Driving?wayPoint.1=40.7178,-74.0138&waypoint.2={lat},{lon}&dateTime=08/24/2023%2009:42&maxSolutions=1&key={bingKey}'
    return render_template("results.html", la = lat, lo = lon, key = bingKey, gas = totalGas, poi = results, weath = months, mons = month_list, route = tup, name = college_name, image = iUrl)

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
        if(pw_confirm(request.form['register_pswd'],request.form['pswd_confirm'])):
            if add_to_db(request.form['register_username'],request.form['register_pswd']):
                return redirect("/home")
            else:
                return render_template('register.html',message="Username already exists")
        else:
            return render_template('register.html',message="Passwords do not match")
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
                return redirect("/home")
            else:
                return render_template("login.html",message="Password is incorrect")
        else:
            return render_template("login.html",message="Username not found")

@app.route("/home", methods = ["POST","GET"])
def home():
    wd = os.path.dirname(os.path.realpath(__file__))
    f = open(wd +"/collegeList.txt", "r")
    colleges = f.readlines()
    return render_template('home.html', collection=colleges)

# @app.route("/like",methods = ["POST","GET"])
# def like():
#     if request.method == "POST":
        

if __name__ == "__main__":
    app.debug = True
    app.run()

