from flaskext.mysql import MySQL
import calendar
import datetime

class Database():

    def __init__(self, app):
        self.mysql = MySQL()
        app.config['MYSQL_DATABASE_USER'] = 'project-web'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'web@project'
        app.config['MYSQL_DATABASE_DB'] = 'project'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        self.mysql.init_app(app)
        conn = self.mysql.connect()
        self.cursor = conn.cursor

    def get_data(self, sql, params=None):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        # print("getting data")
        try:
            # print(sql)
            cursor.execute(sql, params)
        except Exception as e:
            print(e)
            return False

        result = cursor.fetchall()
        data = []
        for row in result:
            data.append(list(row))
        cursor.close()
        conn.close()

        return data

    def set_data(self, sql, params=None):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            conn.commit()
        except Exception as e:
            print(e)
            return False

        cursor.close()
        conn.close()

    def get_dates(self):
        days = []
        data = self.get_data(
            "SELECT cast(A.measurementTime as date) FROM feeder as F left join amount A on A.amountID=F.amountID;")
        for i in range(0, len(data)):
            date = data[i][0]
            if (date != None):
                dayOfWeek = calendar.day_name[date.weekday()]
                monthOfYear = calendar.month_name[date.month]
                day = ("{0},&nbsp{1}&nbsp{2}&nbsp{3}".format(dayOfWeek, date.day, monthOfYear, date.year))
                if (day not in days):
                    days.append(day)
        return days

    def get_hours(self,params = None):
        hours = []
        sql = "SELECT TIME(A.measurementTime) FROM feeder as F left join amount A on A.amountID=F.amountID WHERE cast(A.measurementTime as date) like %(date)s;"
        data = self.get_data(sql, {'date':params})
        for i in range(0, len(data)):
            if (data[i][0] != None):
                time = self.timedelta2hour(data[i][0])
                hours.append(str(datetime.time(time[0], time[1]))[0:5])
        return hours

    def timedelta2hour(self,timedelta):
        hours, min_sec = divmod(timedelta.seconds, 3600)
        minutes, seconds = divmod(min_sec, 60)
        return [hours, minutes]

    def get_weights(self,params = None):
        weights = []
        sql = "SELECT A.foodAmount FROM feeder as F left join amount A on A.amountID=F.amountID WHERE cast(A.measurementTime as date) like %(date)s;"
        data = self.get_data(sql, {'date': params})
        for i in range(0, len(data)):
            if (data[i][0] != None):
                weights.append(str(data[i][0]))
        return weights