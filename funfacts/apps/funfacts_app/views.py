from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from .models import User
from .import web_scrapping
# Create your views here.
#  url(r'^$', views.index),
#     url(r'^funfacts$', views.funfacts),
def index(request):
    return render(request,"funfacts_app/index.html")
    # img_src = web_scrapping.get_src(dob)
    #     context ={
    #         "img_src" : img_src
    #     }
    #     #return redirect("/books",)
    #     return render(request,"funfacts_app/funfacts.html",context)


def funfacts_process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    User.objects.create(name = request.POST['name'], dob = request.POST['dob'], category = request.POST['category'])
    request.session['id'] =User.objects.last().id
    return redirect('/funfacts')



def funfacts(request):
    print(request.POST)
    date_chk = User.objects.last().dob
    #date_chk  = datetime.strptime(date_chk, "%Y-%m-%d")
    print (f"Month  = {date_chk.month}")
    print (f"Day  = {date_chk.day}")
    print (f"Year  = {date_chk.year}")
    new_str = date_chk.strftime("%B %d")
    category = User.objects.last().category
    todays_horoscope = web_scrapping.getHoroscope(date_chk.year,new_str)
    #name_img = web_scrapping.get_src(new_str,category)
    events = web_scrapping.get_historical_data(new_str,date_chk.year)
    context ={
        "user":User.objects.last(),
        "img_src" : events['image'],
        "celeb_name" : events['name'],
        "todays_horoscope" : todays_horoscope['p_vals'],
        "horoscope" : todays_horoscope['atro'],
        "events": web_scrapping.events_past(new_str)

    }

    return render(request,"funfacts_app/funfacts.html",context)