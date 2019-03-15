from django.db import models
import re
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        if len(postData['name']) < 3:
            errors['name'] = 'Name must contain at least 2 characters!'

        if len(postData['username']) < 3:
            errors['username'] = 'Username must contain at least 3 characters!'

        if len(postData['username']) < 1:
            errors['username'] = 'You muts provide a username!'
        elif User.objects.filter(username=postData['username']):
            errors['username'] = "username is already taken."

        if len(postData['password']) <2 :
            errors['password'] = 'Password must contain at least 8 characters'
        if postData['confirm'] != postData['password']:
            errors['confirm'] = 'Password confirmation doesn not match the Password!'


        return errors

    def login_validator(self, postData):
        errors = {}

        if len(postData['passwordlogin']) < 1:
            errors['passwordlogin'] = "Password cannot be blank."

        if len(postData['usernamelogin']) < 1:
            errors['usernamelogin'] = "Username cannot be blank."
        elif not User.objects.filter(username=postData['usernamelogin']):
            errors['usernamelogin'] = "Username is not in database."

        else:
            user = User.objects.filter(username=postData['usernamelogin'])
            print(user)
            if not bcrypt.checkpw(postData['passwordlogin'].encode(), user[0].password.encode()):
                errors['passwordlogin'] = "Wrong password or username."
        return errors


class ItemManager(models.Manager):

    def item_validator(self, postData):
        errors = {}
        if len(postData['product']) < 3:
            errors['product'] = "Product must contain at least three characters"
        return errors


class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # Created items ---> One To Many
    # Faved items ---> Many To Many
    objects = UserManager()
    def __str__(self):
        return self.username

class Item(models.Model):
    product = models.CharField(max_length=255)
    faved_users = models.ManyToManyField(User, related_name="faved_items")
    creater = models.ForeignKey(User, related_name="created_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ItemManager()
    def __str__(self):
        return self.destination
