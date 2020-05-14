from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseServerError, HttpResponseRedirect
from requests import Response
from rest_framework import viewsets
# from .serializers import LoginSerializer
from django.views.decorators import gzip

from .models import login
from .models import footcount
from .models import VisitLog
from .models import Visitors
from django.db.models import Q
import cv2
from django.views.decorators.csrf import csrf_exempt

from django.views.generic.edit import FormView
from .forms import Employee_form, Visitors_form

# Headers for forecasting
import numpy as np
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt
from matplotlib import pyplot
from PIL import Image
import io
from io import BytesIO
import urllib, base64
from pandas.tseries.offsets import DateOffset
from statsmodels.tsa.stattools import adfuller

from django.views import View

# header for Congestion Hours
from datetime import datetime, date, time as datetime_time, timedelta
from itertools import *
# from background_task import background
import time
from collections import OrderedDict

# Sherry Ki Dependencies
from datetime import date
from django.contrib import messages
########################################################
# Global Declarations
uri2 = ""
past_6_days = {}


class IndexClass(View):
    def get(self, request):
        return render(request, 'footcount/login.html')


def get_frame():
    camera =cv2.VideoCapture(0)
    while True:
        _, img = camera.read()
        imgencode=cv2.imencode('.jpg',img)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
    del(camera)


def indexscreen(request):
    try:
        template = "footcount/live.html"
        return render(request,template)
    except:
        print("error")


@gzip.gzip_page
def live(request, stream_path = "video"):
    try :
        return StreamingHttpResponse(get_frame(),content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        return "error"


def live1(request):
        return render(request, 'footcount/live.html')


class CongestionHoursClass(View):
    def get(self, request):
        x = VisitLog.objects.values('log_time_in')
        str(x)
        y = VisitLog.objects.values('log_time_out')
        str(y)
        logout_time = []  # Exit Time
        login_time  = []  # Entry Time
        for i in x:
            login_time.append(i['log_time_in'])
        for i in y:
            logout_time.append(i['log_time_out'])
        login_time.sort()
        logout_time.sort()
        #########################################
        # Testing Part Date
        in_date = []
        out_date = []
        for i in login_time:
            in_date.append(i.date())
        for i in logout_time:
            out_date.append(i.date())
        in_date = list(dict.fromkeys(in_date))
        out_date = list(dict.fromkeys(out_date))
        date = zip(in_date, out_date)

        #########################################
        # Assuming shop is open from 09:00 to 18:00
        # count 1 (9 - 12)
        # count 2 (12 - 15)
        # count 3 (15 - 18)
        c1 = "09:00:00"
        c2 = "12:00:00"
        c3 = "15:00:00"
        c4 = "18:00:00"
        t1 = datetime.strptime(c1, '%H:%M:%S').time()
        t2 = datetime.strptime(c2, '%H:%M:%S').time()
        t3 = datetime.strptime(c3, '%H:%M:%S').time()
        t4 = datetime.strptime(c4, '%H:%M:%S').time()

        weekly = {}
        record = {}
        day_send = []
        result_list = []
        date_send = []

        for it1, it2 in date:  # uniform date
            check_1 = 0
            check_2 = 0
            check_3 = 0
            for (i, j) in zip(login_time, logout_time):
                if i.time() >= t1 and j.time() <= t2 and j.date() == it2 and i.date() == it1:
                    check_1 = check_1 + 1
                elif i.time() >= t1 and j.time() <= t3 and j.date() == it2 and i.date() == it1:
                    check_2 = check_2 + 1
                elif i.time() >= t1 and j.time() <= t4 and j.date() == it2 and i.date() == it1:
                    check_3 = check_3 + 1
            maximum = max(check_1, check_2, check_3)
            record.update({it1: maximum})
            result = ""
            if maximum == check_1:
                result = "09:00:00 to 12:00:00"
                weekly.update({it1: result})
            elif maximum == check_2:
                result = "12:00:00 to 15:00:00"
                weekly.update({it1: result})
            elif maximum == check_3:
                result = "15:00:00 to 18:00:00"
                weekly.update({it1: result})

            result_list.append(result)
            date_send.append(it1)
            day_send.append(str(it1.strftime("%A")))

            result_to_templates = zip(result_list, date_send, day_send)
        temp_dict = {}
        v = []
        dy = []
        count = 0
        maximum_value_send = []
        maximum_date_send = []
        for i, j in record.items():
            temp_dict.update({i: j})
            count += 1

            if count % 2 == 0:
                maxim_value = max(temp_dict.values())
                max_date = max(temp_dict, key=temp_dict.get)
                maximum_value_send.append(maxim_value)
                maximum_date_send.append(max_date)
                v.append(weekly[max_date])
                dy.append(max_date.strftime("%A"))
                temp_dict.clear()

        maximum_ultra_data = zip(maximum_value_send, maximum_date_send, dy, v)

        # Past 6 days
        x = OrderedDict(sorted(record.items(), reverse=True))
        x = dict(x)
        last_week_congestion_data = {}
        count = 0
        for i, j in x.items():
            if count <= 5:
                last_week_congestion_data[i] = j
                count += 1
        a = []
        b = []
        for i in last_week_congestion_data.keys():
            a.append(i)
        for i in last_week_congestion_data.values():
            b.append(i)
        ultra_congestion_data = zip(a, b)

        global past_6_days
        past_6_days = ultra_congestion_data

        object_list = Visitors.objects.values('vis_id', 'vis_type', 'vis_feature_vector', 'vis_photo_path')
        object_list_two = VisitLog.objects.values('log_visitor_id', 'log_time_in', 'log_time_out')
        visits = []
        visitor = []
        for i in object_list:
            visitor.append(i)
        for i in object_list_two:
            visits.append(i)

        merged = {}
        for i in visits:
            x = str(i['log_time_in'])
            y = str(i['log_time_out'])
            i['log_time_in'] = x
            i['log_time_out'] = y

        for i in visits:
            for j in visitor:
                if i['log_visitor_id'] == j['vis_id']:
                    i['vis_type'] = j['vis_type']
                    i['vis_feature_vector'] = j['vis_feature_vector']
                    i['vis_photo_path'] = j['vis_photo_path']

        prams = {
            'result': result_to_templates,
            'maximum': maximum_ultra_data,
            'object_list': visits,
        }
        return render(request, 'footcount/congestion_hrs.html', prams)


class ForecastClass(View):
    # uri = ""
    def get(self, request):
        # x = footcount.objects.values('count')
        # month_data = []                         # Month date
        # for i in x:
        #     month_data.append(i['count'])

        # y = footcount.objects.values('month')
        # value_data = []                         # Count
        # for i in y:
        #     value_data.append(i['month'])

        # # converting to proper format
        # df = pd.DataFrame(list(zip(month_data, value_data)), columns=['Month', 'count'])
        # df['Month'] = pd.to_datetime(df['Month'])

        # df.set_index('Month', inplace=True)
        # df = df.astype(float)

        # df['Seasonal First Difference'] = df['count'] - df['count'].shift(12)
        # # self.adfuller_test(df['Seasonal First Difference'].dropna())
        # # df['Seasonal First Difference'].plot()

        # model = sm.tsa.statespace.SARIMAX(df['count'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        # results = model.fit()

        # # df['forecast'] = results.predict(start=90, end=108, dynamic=True)
        # # df[['count', 'forecast']].plot(figsize=(12, 8))

        # future_dates = [df.index[-1] + DateOffset(months=x) for x in range(0, 12)]
        # future_datest_df = pd.DataFrame(index=future_dates[1:], columns=df.columns)
        # f_d = []
        # for i in future_dates:
        #     f_d.append(i.date())

        # future_df = pd.concat([df, future_datest_df])

        # future_df['forecast'] = results.predict(start=len(month_data)-1, end=len(month_data)+12, dynamic=True)
        # future_df[['count', 'forecast']].plot(figsize=(12, 8))

        # ls = future_df['forecast'][-12:].tolist()
        # ls1 = []
        # for i in ls:
        #     ls1.append(int(i))

        # fig = pyplot.gcf()
        # buf = io.BytesIO()
        # fig.savefig(buf, format='png')
        # buf.seek(0)
        # string = base64.b64encode(buf.read())
        # uri = urllib.parse.quote(string)
        # predictions = zip(f_d, ls1)
        # global uri2
        # uri2 = uri
        # # ForecastClass.uri = uri

        # prams = {
        #     'data': uri,
        #     'values': predictions,
        # }
        return render(request, 'footcount/forecast.html', prams)

    # def adfuller_test(self, x):
    #     result = adfuller(x)
    #     labels = ['ADF Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used']
    #     for value, label in zip(result, labels):
    #         print(label+' : '+str(value))
    #     if result[1] <= 0.05:
    #         print("strong evidence against the null hypothesis(Ho), reject the null hypothesis. Data has no unit root and is stationary")
    #     else:
    #         print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")


# obj = ForecastClass()
# obj1 = CongestionHoursClass()


class AnalyzeClass(View):
    def post(self, request):
        # User Authentication
        database_data = login.objects.values('username', 'password')
        login_un = []
        for i in database_data:
            login_un.append(i['username'])
        login_pass = []
        for i in database_data:
            login_pass.append(i['password'])

        entered_username = request.POST.get('usr_name', 'default')
        entered_password = request.POST.get('pass', 'default')
        # obj.get(request)
        # obj1.get(request)
        for i, j in zip(login_un, login_pass):
            if i == entered_username and j == entered_password:
                return render(request, 'footcount/home.html', {'x': uri2, 'y': past_6_days})

        return render(request, 'footcount/login.html')


class CountingClass(View):
    def get(self, request):
        return render(request, 'footcount/counting.html')


class HomeClass(View):
    def get(self, request):
        # obj.get(request)
        graph = uri2

        # obj1.get(request)
        context = {
            'x': graph,
            'y': past_6_days
        }
        return render(request, 'footcount/home.html', context)


class EmployeeRegClass(View):
    def get(self, request):
        form = Employee_form
        prams = {
            'form': form
        }
        return render(request, 'footcount/emp_reg.html', prams)

    def post(self, request):
        form = Employee_form(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
        prams = {
            'form': form
        }
        return render(request, 'footcount/emp_reg.html', prams)


class IndexClass(View):
    def get(self, request):
        return render(request, 'footcount/login.html')


def classification(request):
    visitorType = Visitors.objects.values('vis_type')
    alert_object = VisitLog.objects.filter(log_visitor_id='001').values('log_time_in')
    new_visitor_count = 0
    frequent_visitor_count = 0
    old_visitor_count = 0
    vistorList = []
    total_visitors_count = 0
    for vis in visitorType:
        vistorList.append(vis['vis_type'])

    for i in vistorList:
        total_visitors_count += 1
        if i == 'new':
            new_visitor_count += 1
        elif i == 'old':
            old_visitor_count += 1
        elif i == 'frequent':
            frequent_visitor_count += 1
    str(alert_object)
    time_list = []
    for time in alert_object:
        time_list.append(time['log_time_in'])

    checkin_date = []
    for i in time_list:
        checkin_date.append(i.date())

    suspicious_count = 0

    for i in checkin_date:
        if i == date.today():
            suspicious_count += 1
    suspicious = 0
    if suspicious_count >= 6:
        suspicious += 1

    ############################

    # visitors_new = [new_visitor_count]
    # visitors_frequent = [frequent_visitor_count]
    # visitors_old = [old_visitor_count]
    # # total_visitors = [0,total_visitors_count]
    # plt.xlabel('Visitors Classes')
    # plt.ylabel('Total Visitors')
    # plt.title('Visitors Classification')
    # plt.yticks(range(0,11))
    # legend = ['New Visitors', 'Frequent Visitors', 'Occasional Visitors']
    # plt.hist([visitors_new,visitors_frequent,visitors_old], color=['orange','green','blue'])
    # plt.legend(legend)

    ############################
    labels = 'New Visitors', 'Frequent Visitors', 'Occasional Visitors'
    sizes = [new_visitor_count, frequent_visitor_count, old_visitor_count]
    colors = ['gold', 'blue', 'green']
    explode = (0.1, 0, 0)
    patches, texts, autotexts = pyplot.pie(sizes, radius=1.6, textprops = {"fontsize":15}, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%', shadow=True, startangle=120)
    for text in texts:
        text.set_color('white')
    # for autotext in autotexts:
    #     autotext.set_color('white')
    pyplot.axis('equal')
    pyplot.savefig('media/pie.png', transparent=True)

    ###########################
    params = {
        'new_vis': new_visitor_count,
        'frequent_vis': frequent_visitor_count,
        'old_vis': old_visitor_count,
        'suspicious': suspicious,

    }
    return render(request, 'footcount/classification.html', params)


def time_spent(request):
    visitors_time = VisitLog.objects.values('log_visitor_id', 'log_time_in', 'log_time_out').order_by('log_visitor_id')
    # visitors_record = Visitors.objects.filter(vis_id__in=Subquery(visitors_time.values('log_visitor_id'))).order_by('vis_id')
    visitors_record = Visitors.objects.values('vis_id', 'vis_type', 'vis_photo_path').order_by('vis_id')
    checkin = VisitLog.objects.values('log_time_in').order_by('log_visitor_id')
    checkout = VisitLog.objects.values('log_time_out').order_by('log_visitor_id')

    visits = []
    visitors = []
    for i in visitors_time:
        visits.append(i)
    for i in visitors_record:
        visitors.append(i)

    for i in visits:
        for j in visitors:
            if i['log_visitor_id'] == j['vis_id']:
                i['vis_type'] = j['vis_type']
                i['vis_photo_path'] = j['vis_photo_path']

    str(checkin)
    str(checkout)
    checkin_time = []
    checkout_time = []
    difference = []
    for i in checkin:
        checkin_time.append(i['log_time_in'])

    for i in checkout:
        checkout_time.append(i['log_time_out'])

    time_in = []
    time_out = []
    for i in checkin_time:
        time_in.append(i.time())
    for i in checkout_time:
        time_out.append(i.time())
    formate = '%H:%M:%S'
    for (i, j) in zip(time_in, time_out):
        difference.append(datetime.strptime(str(j), formate) - datetime.strptime(str(i), formate))
    
    halftime = datetime.strptime('00:30:00', formate).time()
    onetime = datetime.strptime('01:00:00', formate).time()
    onehalftime = datetime.strptime('01:30:00', formate).time()
    twotime = datetime.strptime('02:00:00', formate).time()
    twohalftime = datetime.strptime('02:30:00', formate).time()
    threetime = datetime.strptime('03:00:00', formate).time()
    threehalftime = datetime.strptime('03:30:00', formate).time()
    fourtime = datetime.strptime('04:00:00', formate).time()
    fourhalftime = datetime.strptime('04:30:00', formate).time()
    fivetime = datetime.strptime('05:00:00', formate).time()
    fivehalftime = datetime.strptime('05:30:00', formate).time()
    sixtime = datetime.strptime('06:00:00', formate).time()

    half = 0
    one = 0
    onehalf = 0
    two = 0
    twohalf = 0
    three = 0
    threehalf = 0
    four = 0
    fourhalf = 0
    five = 0
    fivehalf = 0
    six = 0

    for time in difference:
        if str(time) <= str(halftime)[1:]:
            half+=1
        elif str(time) > str(halftime)[1:] and str(time) <= str(onetime)[1:]:
            one+=1
        elif str(time) > str(onetime)[1:] and str(time) <= str(onehalftime)[1:]:
            onehalf+=1
        elif str(time) > str(onehalftime)[1:] and str(time) <= str(twotime)[1:]:
            two+=1
        elif str(time) > str(twotime)[1:] and str(time) <= str(twohalftime)[1:]:
            twohalf+=1
        elif str(time) > str(twohalftime)[1:] and str(time) <= str(threetime)[1:]:
            three+=1
        elif str(time) > str(threetime)[1:] and str(time) <= str(threehalftime)[1:]:
            threehalf+=1
        elif str(time) > str(threehalftime)[1:] and str(time) <= str(fourtime)[1:]:
            four+=1
        elif str(time) > str(fourtime)[1:] and str(time) <= str(fourhalftime)[1:]:
            fourhalf+=1
        elif str(time) > str(fourhalftime)[1:] and str(time) <= str(fivetime)[1:]:
            five+=1
        elif str(time) > str(fivetime)[1:] and str(time) <= str(fivehalftime)[1:]:
            fivehalf+=1
        elif str(time) > str(fivehalftime)[1:]:
            six+=1
        
    hours = [half,one,onehalf,two,twohalf,three,threehalf,four,fourhalf,five,fivehalf,six]
    pyplot.bar(range(len(hours)), hours, color = 'royalblue', alpha = 0.8)
    pyplot.xticks(range(len(hours)), [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6])
    pyplot.grid(color='grey', linestyle='dashed', linewidth=2, axis='y', alpha=0.8)
    pyplot.title('Time Spent By Visitors', color='orange', fontsize=20)
    pyplot.ylabel('No. of Visitors', color='white', fontsize=15)
    pyplot.xlabel('Hour(s)', color='white', fontsize=15)
    pyplot.tick_params(axis='x', colors='white')
    pyplot.tick_params(axis='y', colors='white')
    pyplot.savefig('media/bar.png', transparent=True)
        


    if request.method == 'POST':
        srch = request.POST.get('srch')
        if srch:
            match = VisitLog.objects.filter(Q(log_visitor_id=srch))
            match2 = Visitors.objects.filter(Q(vis_id__icontains=srch))
            vis_time_in = VisitLog.objects.values('log_time_in').filter(Q(log_visitor_id=srch))
            vis_time_out = VisitLog.objects.values('log_time_out').filter(Q(log_visitor_id=srch))
            str(vis_time_in)
            str(vis_time_out)
            sr_checkin_time = []
            sr_checkout_time = []
            for i in vis_time_in:
                sr_checkin_time.append(i['log_time_in'])
            for i in vis_time_out:
                sr_checkout_time.append(i['log_time_out'])
            sr_time_in = []
            sr_time_out = []
            for i in sr_checkin_time:
                sr_time_in.append(i.time())

            for i in sr_checkout_time:
                sr_time_out.append(i.time())

            formate = '%H:%M:%S'
            for (i, j) in zip(sr_time_in, sr_time_out):
                difference.append(datetime.strptime(str(j), formate) - datetime.strptime(str(i), formate))
            if match:
                return render(request, 'footcount/time_spent.html', {'sr': zip(match, difference), 'sr2': match2})
            else:
                messages.error(request, 'no result found')
        else:
            return HttpResponseRedirect('/time_spent')

    params = {
        'visitors_time': zip(visits, difference),
    }
    return render(request, 'footcount/time_spent.html', params)
def visitors_reg(request):
    if request.method == 'POST':
        form = Visitors_form(request.POST, request.FILES or None)
        if form.is_valid():
            vis_id = form.cleaned_data['vis_id']
            form.save()
            messages.success(request, "Visitor Registered Successfully")
            return HttpResponseRedirect('/visitors_reg/')
    else:
        form = Visitors_form()

    return render(request, 'footcount/vis_reg.html', {'form': form})