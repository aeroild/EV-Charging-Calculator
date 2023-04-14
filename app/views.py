from app import app

from flask import render_template, request, redirect, session

from datetime import datetime, timedelta   #brukes for å vise cutom filter 

import math

import time

import json

from json import dumps

#global batteryneed

app.config["SECRET_KEY"] = "k0I30Da2pRnJbbNBqzVuuA"

@app.template_filter("clean_date")  #lager custom filter som vi gir navn clean_date
def clean_date(dt):
    return dt.strftime("%d %m %Y")

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/setup")
def setup():
       
        return render_template("setup.html")
    
@app.route("/saved", methods=["GET", "POST"])
def saved():
    
    if request.method == "POST":   #Denne koden kjøres bare når metoden er POST
         
            req = request.form   #Lagrer i variablen req data som request lager en fin diconary av
    
            #Lager en variabel av hvert felt
            chargingcurrent = int(req["chargingcurrent"])
            batteryusable = int(req["batteryusable"])
            consumption = int(req["consumption"])
            chargingloss = float(req["chargingloss"])
            voltage = int(req["voltage"])
            phases = int(req["phases"])
            
            #Beregninger
            chargingspeed = round((chargingcurrent*voltage*math.sqrt(phases)/1000), 1)
            
            #printer ut hver variabel
            print(req)
            print(chargingcurrent, batteryusable, consumption, chargingloss, phases, voltage)
            print(chargingspeed)

            session["chargingcurrent"] = chargingcurrent
            session["chargingspeed"] = chargingspeed
            session["batteryusable"] = batteryusable
            session["consumption"] = consumption
            session["chargingloss"] = chargingloss            
            session["voltage"] = voltage
            session["phases"] = phases

            return redirect(request.url)
        
    return render_template("saved.html", chargingspeed=session.get("chargingspeed"), chargingcurrent=session.get("chargingcurrent"), batteryusable=session.get("batteryusable"), consumption=session.get("consumption"), chargingloss=session.get("chargingloss"), voltage=session.get("voltage"), phases=session.get("phases"))    

@app.route("/starte", methods=["GET", "POST"])
def starte():

        return render_template("starte.html")

@app.route("/result", methods=["GET", "POST"])
def result():
            
        if request.method == "POST":   #Denne koden kjøres bare når metoden er POST
         
            req = request.form   #Lagrer i variablen req data som request lager en fin diconary av
    
            #Lager en variabel av hvert felt
            batterynow = req.get("batterynow")
            batterytarget = req.get("batterytarget")
            departure = req.get("departure")
            
            #Fjerner T fra dato og tid string
            departure=departure.replace('T', ' ')
            
            #Gjør om til datetime
            departure = datetime.strptime(departure, "%Y-%m-%d %H:%M")
                        
            print(batterynow, batterytarget, departure)
            
            batteryusable=session.get("batteryusable")
            consumption=session.get("consumption")
            
            #Beregninger
            batteryneedpct = int(batterytarget) - int(batterynow)
            batteryneedkwh = ((batteryneedpct/100)*session.get("batteryusable"))/((100-session.get("chargingloss"))/100)
            hourscharging = batteryneedkwh/session.get("chargingspeed")
            chargingtime = timedelta(hours=hourscharging)
            chargingstart = departure - chargingtime
            
            chargingtime = json.dumps(chargingtime, indent=4, sort_keys=True, default=str)
            chargingtime = chargingtime[1:5]
            #chargingtime = datetime.strptime(chargingtime, "%H:%M")
            rangeestimate = round((((int(batterytarget)/100) * batteryusable)/consumption) * 100)
            
            #chargingstart=datetime.strptime(chargingstart, "%Y-%m-%d %H:%M")
            
            session["chargingtime"] = chargingtime
            session["chargingstart"] = chargingstart
            session["rangeestimate"] = rangeestimate
                
            #printer ut hver variabel
            print(batteryneedpct, batteryneedkwh, hourscharging, chargingstart, chargingtime)

            return redirect(request.url)  #Etter at Sign up knappen trykkes sendes brukeren til url-en sign-up    
   
    
        return render_template("result.html", chargingtime=session.get("chargingtime"), chargingstart=session.get("chargingstart"), rangeestimate=session.get("rangeestimate"))    
   

    
@app.route("/power", methods=["GET", "POST"])
def power():
    
        if request.method == "POST":   #Denne koden kjøres bare når metoden er POST
         
            req = request.form   #Lagrer i variablen req data som request lager en fin diconary av
    
            #Lager en variabel av hvert felt
            ladestrom = int(req["ladestrom"])
            batteri = int(req["batteri"])
            forbruk = int(req["forbruk"])
            ladetap = float(req["ladetap"])
            spenning = int(req["spenning"])
            faser = int(req["faser"])
            
            #Beregninger
            ladehastighet = (ladestrom*spenning*math.sqrt(faser)/1000)
            
            #printer ut hver variabel
            print(req)
            print(ladestrom, batteri, forbruk, ladetap, faser, spenning)
            print(ladehastighet)
                             
            session["ladehastighet"] = ladehastighet
            session["batteri"] = batteri
            session["forbruk"] = forbruk
            session["ladetap"] = ladetap            

            return redirect(request.url)  #Etter at Sign up knappen trykkes sendes brukeren til url-en sign-up
        
        return render_template("starte.html")
    
    
