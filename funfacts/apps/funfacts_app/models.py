from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        NAME_REGEX = re.compile(r'^[a-zA-Z]+[ ]+[a-zA-Z]+$')
        if not NAME_REGEX.match(postData['name']):    # test whether a field matches the pattern            
            errors['name'] = ("Invalid name")
        if len(postData['name']) < 2:
            errors["name_len"] = "User name should be at least 2 characters"
        if postData['dob'] =='':
            errors["date"] = "Please choose a date"
        elif datetime.strptime(postData['dob'], '%Y-%m-%d') > datetime.today():
            errors["date_past"] = "Please choose a date from past"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateField()
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 
