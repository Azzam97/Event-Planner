from django.db import models
import re
import bcrypt
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['username']) < 2 or not postData['username'].isalpha():
            errors['username'] = "User name should be at least 2 characters long and only alphabet letters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        users = User.objects.all()
        for user in users:
            if postData['email'] == user.email:
                errors['unique'] = "This email is already taken"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be 8 characters long"
        if postData['password'] != postData['pwdconfirm']:
            errors['confirm'] = "Password not the same, try again"
        return errors
    
    def login_validator(self, postData2):
        errors2 = {}
        email2 = postData2['email2']
        password2 = postData2['password2']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData2['email2']):
            errors2['email2'] = "Invalid email address"
        users = User.objects.filter(email = email2)
        if users:
            logged_user = users[0]
            if not bcrypt.checkpw(password2.encode(), logged_user.password.encode()):
                errors2['password2'] = "Wrong password, try again"
        return errors2
    

class EventManager(models.Manager):
    def event_validator(self, postdata):
        errors3 = {}
        if len(postdata['eventname']) < 4:
            errors3['eventname'] = "Event name should be at least 4 charatcters long"
        if len(postdata['location']) < 3:
            errors3['location'] = "Location should be at least 3 characters long"
        location = postdata['location']
        events = Event.objects.all()
        date1 = datetime.strptime(postdata['date'], "%Y-%m-%d").date()
        print (date1)
        for event in events:
            if event.location == location:
                if date1 == event.date:
                    errors3['date'] = "This date is already taken"
        return errors3



class User(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.user_name}"


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    desc = models.TextField()
    date = models.DateField()
    creator = models.ForeignKey(User ,related_name='users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()