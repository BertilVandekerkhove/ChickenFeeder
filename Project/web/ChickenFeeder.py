from flask import Flask, render_template, request
from Classes.Database import Database
from Classes.DRV8825 import DRV8825
from Classes.HX711 import HX711
from threading import Thread
from time import sleep
import datetime
import calendar
import socket
import time

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

checkFeedTimes = True

stepper = DRV8825(21,20)

app = Flask(__name__,template_folder='./templates')
db = Database(app)

ip_address = "0"

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    print(ip_address)
except:
    print("IP + PORT :5000", 0)
    print("169.254.10.11", 1)

def measure_food():
    global hx
    hx = HX711(23, 24)
    hx.set_reading_format("LSB", "MSB")
    hx.set_reference_unit(327)
    hx.reset()
    hx.tare()
    while True:
        total = 0
        val = hx.get_weight(5)
        hx.power_down()
        hx.power_up()
        sleep(0.5)
        if(val>0):
            ID = db.get_data("SELECT feederID FROM feeder ORDER BY feederID DESC LIMIT 1")
            sql = "INSERT INTO feeder VALUES((%(ID)s+1),NULL,NULL,(%(ID)s+1))"
            db.set_data(sql, {'ID':ID[0][0]})
            sql = "INSERT INTO amount VALUES((%(ID)s+1),now(),%(amount)s);"
            db.set_data(sql, {'ID': ID[0][0], 'amount': val})
        sleep(1800)

thread_foodmeasure = Thread(target=measure_food)
thread_foodmeasure.daemon = True
thread_foodmeasure.start()

def check_feedtime():
    global checkFeedTimes
    while checkFeedTimes:
        count = 0
        times = []
        time_data = db.get_data("SELECT FT.feedingTime FROM feeder as F left join feedingtimes FT on FT.feedingTimeID = F.feedingTimeID;")
        data = db.get_data("SELECT FT.feedingTime, FT.dayID FROM feeder as F left join feedingtimes FT on FT.feedingTimeID = F.feedingTimeID;")
        for i in range(0, len(data)):
            if (data[i][0] != None):
                time_data = db.timedelta2hour(data[i][0])
                time = (str(datetime.time(time_data[0], time_data[1]))[0:5])
                day = days[data[i][1]-1]
                if((time == str(datetime.datetime.now().time())[0:5]) and (day == calendar.day_name[datetime.date.today().weekday()])):
                    while(count!=1000):
                        stepper.on()
                        count += 1
                    ID = db.get_data("SELECT feederID FROM feeder ORDER BY feederID DESC LIMIT 1")
                    sql = "INSERT INTO feeder VALUES((%(ID)s+1),NULL,NULL,(%(ID)s+1))"
                    db.set_data(sql, {'ID': ID[0][0]})
                    sql = "INSERT INTO deposit VALUES((%(ID)s+1),now(),1);"
                    db.set_data(sql, {'ID': ID[0][0]})
                    sleep(60)

thread_feedtimes = Thread(target=check_feedtime)
thread_feedtimes.daemon = True
thread_feedtimes.start()

def getMonth(monthName):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return months.index(monthName) + 1

@app.route('/', methods=['GET','POST'])
def home():
    day = "None"
    list_days = db.get_dates()
    if request.method == 'POST':
        data = str(request.form["select"]).rsplit('&nbsp')
        date = datetime.datetime(int(data[3]),getMonth(data[2]),int(data[1])).date()
        list_times = db.get_hours(date)
        list_weights = db.get_weights(date)
        dayOfWeek = calendar.day_name[date.weekday()]
        monthOfYear = calendar.month_name[date.month]
        day = ("{0},&nbsp{1}&nbsp{2}&nbsp{3}".format(dayOfWeek, date.day, monthOfYear, date.year))
    else:
        data = list_days[len(list_days)-1].rsplit('&nbsp')
        date = datetime.datetime(int(data[3]), getMonth(data[2]), int(data[1])).date()
        list_times = db.get_hours(date)
        list_weights = db.get_weights(date)
    return render_template('home.html', days=(list(reversed(list_days))), time=list_times, weight=list_weights, dayselect = day)

@app.route('/feedingtimes', methods=['GET','POST'])
def feeding_times():
    global days
    items_count = 0
    if request.method == 'POST':
        for i in range(1,8):
            day = request.form.get(days[i - 1])
            time = datetime.time(int(day[0:2]),int(day[3:]))
            sql = "call project.create_or_update_first_rows(%(ID)s,%(time)s,%(dayID)s);"
            db.set_data(sql, {'ID':i, 'time':time, 'dayID':i})
            items_count += 1
        try:
            for i in range(1,8):
                day = request.form.getlist("{0}1".format(days[i - 1]))
                for item in range(1,len(day)+1):
                    time = datetime.time(int(day[item-1][0:2]),int(day[item-1][3:]))
                    id = ((i+7)*item)
                    sql = "call project.insert_or_update_time(%(ID)s,%(time)s,%(dayID)s);"
                    db.set_data(sql, {'ID':id, 'time':time, 'dayID':i})
                    items_count += 1
        except:
            print(Exception)
        count_after = db.get_data("SELECT COUNT(*) from feedingtimes;")
        count = (count_after[0][0] - items_count)
        if count > 0:
            sql = "call project.delete_rows(%(count)s);"
            db.set_data(sql, {'count':count})
    return render_template('feedingtimes.html')

@app.route('/history')
def history():
    idlist = []
    momentlist = []
    iddata = db.get_data("SELECT depositID from deposit ")
    momentdata = db.get_data("SELECT depositMoment from deposit ")
    for i in range(0,len(iddata)):
        if(iddata[i][0]!=None):
            idlist.append(int(iddata[i][0]))
            dayOfWeek = calendar.day_name[momentdata[i][0].weekday()]
            monthOfYear = calendar.month_name[momentdata[i][0].month]
            time = datetime.time(momentdata[i][0].hour,momentdata[i][0].minute)
            moment = ("{0}, {1} {2} {3} - {4}".format(dayOfWeek, momentdata[i][0].day, monthOfYear, momentdata[i][0].year, str(time)[0:5]))
            momentlist.append(moment)
    return render_template('deposit_history.html', idlist = idlist, momentlist = momentlist)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
