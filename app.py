from flask import Flask, render_template, url_for, request
import sqlite3
from datetime import datetime
import json
from db import Database


app = Flask(__name__)
db = Database("dbdb")


def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        escort = request.form['escort']
        dateraw = request.form['date']
        duration = int(request.form['hours'])
        time = request.form['time']
        name = request.form['name']
        hours = []
        hoursf = ""

        datef = dateraw[8:10] + "." + dateraw[5:7] + "." + dateraw[:4]
        dateasdt = datetime(int(datef[6:11]), int(datef[3:5]), int(datef[0:2]))
        if (dateasdt.weekday() <= 3):
            weektimes = ['18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
            index = weektimes.index(time)
            for x in range(duration):
                hours.append(weektimes[index])
                index += 1
            hoursf = ', '.join(hours).rstrip(', ')
        else:
            weekendtimes = ['15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
            index = weekendtimes.index(time)
            for x in range(duration):
                hours.append(weekendtimes[index])
                index += 1
            hoursf = ', '.join(hours).rstrip(', ')

        bookingid = db.reservereturnid(name, datef, hoursf, escort)
        return render_template('success.html', type = "reserve", bookingid = bookingid)
        
    else:
        escortslist = db.fetchescortslist()
        today = str(datetime.today())[:10]
        
        return render_template('reserve.html', escortslist=escortslist, today=today)

@app.route('/change', methods=['GET', 'POST'])
def changenext():
        if (request.method == 'POST'):
            reqtype = request.form['reqtype']
            if reqtype == 'next':
                name = request.form['name']
                bookingid = request.form['id']
                result = db.getreservationsecure(name, bookingid)
                if ( len(result) == 0 ):
                    return render_template('change.html', type="noescort")
                else:
                    date = result[0][1]
                    date = date[6:10] + "-" + date[3:5] + "-" + date[0:2] 
                    time = result[0][2]
                    time = time[0:5]
                    escort = result[0][3]
                    escortslist = db.fetchescortslist()
                    today = str(datetime.today())[:10]
                    print("today: " + today)
                    print("time: " + time)
                    return render_template('change.html', type="posted", name=name, today=today, bookingId=bookingid, date=date, time=time, escort=escort, escortslist=escortslist)
            elif reqtype == 'change':
                bookingId = request.form['bookingId']
                escort = request.form['escort']
                dateraw = request.form['date']
                duration = int(request.form['hours'])
                time = request.form['time']
                name = request.form['name']
                hours = []
                hoursf = ""
                datef = dateraw[8:10] + "." + dateraw[5:7] + "." + dateraw[:4]
                dateasdt = datetime(int(datef[6:11]), int(datef[3:5]), int(datef[0:2]))
                if (dateasdt.weekday() <= 3):
                    weektimes = ['18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
                    index = weektimes.index(time)
                    for x in range(duration):
                        hours.append(weektimes[index])
                        index += 1
                    hoursf = ', '.join(hours).rstrip(', ')
                else:
                    weekendtimes = ['15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
                    index = weekendtimes.index(time)
                    for x in range(duration):
                        hours.append(weekendtimes[index])
                        index += 1
                    hoursf = ', '.join(hours).rstrip(', ')
                db.changereservation(name, datef, hoursf, escort, bookingId)
                return render_template('success.html', type = "change", bookingid = bookingId)


        else: 
            return render_template('change.html', type="opened")
        

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        name = request.form['name']
        bookingid = request.form['id']
        result = db.getreservationsecure(name, bookingid)
        if ( len(result) == 0 ):
            return render_template('delete.html', type = "invalid")
        else:
            print("DELETING: " + str(result))    
            db.deletereservation(bookingid)
            return render_template('success.html', type = "delete")
    else:
        return render_template('delete.html')

@app.route('/gettimes', methods=['POST', 'GET'])
def returntimes():
    reqtype = str(request.args['type'])
    if (request.args.get('type') == None or request.args.get("escort") == None or request.args.get("date") == None):
        return "no args"
    
    elif (reqtype != "change" and reqtype != "reserve"):
        return "wrong type"

    if (request.args.get('type') == "reserve"):
        escort = request.args['escort']
        dateraw = request.args['date']
        datef = dateraw[8:10] + "." + dateraw[5:7] + "." + dateraw[:4]
        dateasdt = datetime(int(datef[6:11]), int(datef[3:5]), int(datef[0:2]))
        reservedtimelist = db.getreservedlist(datef, escort)
        if (dateasdt.weekday() <= 3):
            weektimes = ['18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
            availabletimes = sorted(Diff(reservedtimelist, weektimes), key=lambda x: x[:2])
            return json.dumps(availabletimes[1:])
        else:
            weekendtimes = ['15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
            availabletimes = sorted(Diff(reservedtimelist, weekendtimes), key=lambda x: x[:2])
            return json.dumps(availabletimes[1:])

    elif (request.args.get('type') == 'change'):
        escort = request.args['escort']
        dateraw = request.args['date']
        bookingId = request.args['bookingId']
        datef = dateraw[8:10] + "." + dateraw[5:7] + "." + dateraw[:4]
        dateasdt = datetime(int(datef[6:11]), int(datef[3:5]), int(datef[0:2]))
        reservedtimelistfor = db.getreservedlistfor(bookingId)
        reservedtimelist = db.getreservedlist(datef, escort)
        print(bookingId)
        print(reservedtimelist)
        print(db.getescortfor(bookingId))
        print("reservedtimelistfor:" + str(reservedtimelistfor))
        
        if (dateasdt.weekday() <= 3):
            weektimes = ['18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
            availabletimes = sorted(Diff(reservedtimelist, weektimes), key=lambda x: x[:2])
            print("booked date:" + str(db.getdateforbooking(bookingId)))
            if escort == db.getescortfor(bookingId) and db.getdateforbooking(bookingId) == datef:
                availabletimes.extend(reservedtimelistfor)
                availabletimes = sorted(availabletimes, key=lambda x: x[:2])
                if availabletimes[0] == "":
                    del availabletimes[0]
                return json.dumps(availabletimes)
            return json.dumps(availabletimes[1:])
        else:
            weekendtimes = ['15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
            availabletimes = sorted(Diff(reservedtimelist, weekendtimes), key=lambda x: x[:2])
            if escort == db.getescortfor(bookingId) and db.getdateforbooking(bookingId) == datef:
                availabletimes.extend(reservedtimelistfor)
                if availabletimes[0] == "":
                    del availabletimes[0]
                return json.dumps(availabletimes)
            return json.dumps(availabletimes[1:])

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        if password == "abcdef":
            reservationslist = db.getallreservations()
            return render_template('admin.html', type="admin", reservationslist=reservationslist)
        else: 
            return render_template('admin.html', type="wrongp")
    else:    
        return render_template('admin.html', type = "login")
        

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = "1234")

