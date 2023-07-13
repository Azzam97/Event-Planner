from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User, Event
import bcrypt

# Create your views here.
def index(request):
    return render(request, "register.html")


def index2(request):
    return render(request, "login.html")


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    else:
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        request.session['username'] = uname
        request.session['status'] = "You have registered successfully"
        User.objects.create(user_name = uname,
                        email = email,
                        password = pw_hash
                        )
        return redirect('/welcome')


def success(request):
    if 'username' not in request.session:
        return redirect('/')
    context = {
        'events': Event.objects.all().order_by("date"),
        'status': request.session['status']
    }
    return render(request, "main_page.html", context)


def login(request):
    errors2 = User.objects.login_validator(request.POST)
    if len(errors2) > 0:
        for value in errors2.values():
            messages.error(request, value)
        return redirect('/')
    else:
        email2 = request.POST['email2']
        user = User.objects.filter(email = email2) 
        request.session['username'] = user[0].user_name
        request.session['status'] = "You have logged in successfully logged in"
        return redirect('/welcome')
    
    
def new(request):
    if 'username' not in request.session:
        return redirect('/')
    return render(request, 'new_event.html')


def create(request):
    errors3 = Event.objects.event_validator(request.POST)
    if len(errors3) > 0:
        for value in errors3.values():
            messages.error(request, value)
        return redirect('/new_event')
    username = request.session['username']
    user = User.objects.get(user_name = username)
    Event.objects.create(event_name = request.POST['eventname'],
                         location = request.POST['location'],
                         desc = request.POST['desc'],
                         date = request.POST['date'],
                         creator = User.objects.get(id = user.id)
                         )
    request.session['status'] = "Thanks for booking with us"
    return redirect('/welcome')


def view(request, id):
    if 'username' not in request.session:
        return redirect('/')
    event = Event.objects.get(id = id)
    user = User.objects.get(user_name = request.session['username'])
    context = {
        "event": event
    }
    if user.id == event.creator_id:
        return render(request, "details1.html", context)
    return render(request, "details2.html", context)


def edit(request, id):
    if 'username' not in request.session:
        return redirect('/')
    event = Event.objects.get(id = id)
    context = {
        'event': event
    }
    return render(request, "edit.html", context)


def update(request, id):
    event = Event.objects.get(id = id)
    errors3 = Event.objects.event_validator(request.POST)
    if len(errors3)>0:
        for value in errors3.values():
            messages.error(request, value)
        return redirect(f'/view/{event.id}/edit')
    event.event_name = request.POST['eventname']
    event.location = request.POST['location']
    event.desc = request.POST['desc']
    event.date = request.POST['date']
    event.save()
    return redirect(f"/view/{event.id}")


def delete(request, id):
    event = Event.objects.get(id = id)
    event.delete()
    return redirect('/welcome')


def logout(request):
    request.session.flush()
    return redirect('/')