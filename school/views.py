from django.shortcuts import render, redirect

# mail
from django.core.mail import send_mail

# models
from .models import Principal, School, Partner
from event.models import Event
from account.models import TeacherUser
from news.models import News

from django.contrib import messages

def landing_page(request):
    partner = Partner.objects.all()
    event = Event.objects.all()
    school = School.objects.all()
    school_ = School.objects.get(id=1)
    teacher = TeacherUser.objects.all()
    news_latest = None
    try:
        news_latest = News.objects.latest('-date')
    except Exception:
        print("Who")
    news = News.objects.all()
    data = {
        'partners': partner,
        'events': event,
        'school_data': school,
        'teachers': teacher,
        'news_latest': news_latest,
        'news': news,
        'school': school_,

    }
    return render(request, 'index.html', data)


subject = "Connection"


def connect(request):
    mail_address = request.POST.get('email_address')
    print(mail_address)
    send_mail(
        subject,
        mail_address,
        'stha.binod1000@gmail.com',
        ['stha.binod1000@gmail.com'],
    )
    return redirect('landing-page')


def about(request):
    principal = Principal.objects.get(id=1)
    data = {
    'principal': principal
    }
    return render(request, 'school/about.html', data)


def admission(request):
    return render(request, 'school/admission.html')


def contact(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email_address = request.POST.get('eaddress')
        number = request.POST.get('number')
        message = request.POST.get('message')
        print(fname, lname, email_address, number, message)
        send_message = f' First Name: {fname}\n Last name: {lname} \n Email Addresss: {email_address} \n Number: {number} \n Message: {message}'
        send_mail(
            'Contact',
            send_message,
            'stha.binod1000@gmail.com',
            [email_address],
        )
        messages.success(request, "We will contact you soon!")

    return render(request, 'school/contact.html')
