from flask import Flask, render_template, request, Response, session
from db import add_to_db, in_table, correct_passwd
import requests
code = 7997
app = app = Flask(__name__)      
app.secret_key = "6gBvzKwE8RWOt6amHzNz"


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
        



if __name__ == "__main__": 
    app.debug = True                                                                                                        
    app.run()      

