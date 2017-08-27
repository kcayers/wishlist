from __future__ import unicode_literals

from django.db import models
import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+._-]+@[a-zA-Z0-9+._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]\w+\ [a-zA-Z]\w+$')

class UserManager(models.Manager):
    def validate_date(self, postData):
        if postData['date_hired'] == '':
            return "Date Hired must not be left blank"

    def validate_registration(self, postData):
        errors = []

        if len(postData['name']) < 3:
            errors.append("Name should be longer than 3 letters")
        if len(postData['user_name']) < 3:
            errors.append("Username should be longer than 3 characters")
        if not NAME_REGEX.match(postData['name']):
            errors.append("Name should have a first and last name and letters only")
        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters")
        if postData['password'] != postData ['confirm']:
            errors.append("Password and Confirm must match")

        try:
            User.objects.get(user_name=postData['user_name'])
            errors.append("Username already exits")
        except:
            pass
        if len(errors):
            return errors
        encrypted = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            name = postData['name'],
            user_name = postData['user_name'],
            date_hired = postData['date_hired'],
            password = encrypted
            )
        return user.id

    def validate_login(self, postData):
        errors = []
        try:
            user = User.objects.get(user_name=postData['user_name'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                return user.id
            else:
                errors.append("wrong password")
        except:
            errors.append("invalid username")

        if len(errors):
            return errors

class ItemManager(models.Manager):
    def validate_item(self, postData, creator_id):
        errors = []
        if len(postData['item_name']) < 3:
            errors.append("Item/Product name should be longer than 3 letters")
        if len(errors):
            return errors

        item = Item.objects.create(
            item_name = postData['item_name'],
            created_by = User.objects.get(id=creator_id),
            )
        return item.id

class User(models.Model):
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {}>".format(self.name, self.user_name, self.date_hired)

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name = "created_items")
    added_by = models.ManyToManyField(User, related_name = "added_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
    def __repr__(self):
        return "<Item object: {} {} {}>".format(self.item_name, self.created_by.name, self.added_by.name)
