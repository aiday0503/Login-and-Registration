from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
from datetime import datetime, timedelta

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def validation(self, postdata):
        errors = []
       
        if len(postdata['fName'])<1 and len(postdata['lName'])<1 and len (postdata['email'])<1 and len(postdata['date'])<1:
            errors.append("Please fill outs the form to register")
        if len(postdata['fName']) < 2:
            errors.append("User name should be more than 2 characters")
        if len(postdata['lName']) < 2:
            errors.append("User name should be more than 2 characters")
        if len(postdata['email']) < 0:
            errors.append("Sorry you need an email to register.")

        if not re.match(EMAIL_REGEX, postdata['email']):
            errors.append("Hmm this doesn't look like a valid email")
        else:
            if len(self.filter(email=postdata['email']))>0:
                errors.append("Email already in use.")
        
        if postdata['date'] !='':
            date = datetime.strptime(postdata['date'], "%Y-%m-%d")
            now = datetime.now()
            if date > now:
                errors.append("Invalid Birthday Field")
            else:
                if now - date  < timedelta(6570):
                    errors.append("Can not register due to under age.")
        else:
            errors.append("Birthday date is invalid.")
                        
        if len(postdata['password1']) < 8:
            errors.append("Password cannot be less than 8 characters!")

        if postdata['password1'] != postdata['password2']:
            errors.append("Password and password confirmation must match!")

        if len(errors) == 0:
            hash_pw = bcrypt.hashpw(postdata['password1'].encode(), bcrypt.gensalt())
            new_user = self.create(
                fName = postdata["fName"],
                lName = postdata["lName"],
                email = postdata["email"],
                gender = postdata["gender"],
                birthday = postdata["date"],
                password = hash_pw  
            )   
            return new_user
        return errors

    def validation_2(self, postdata):
        errors = []        
        if len(self.filter(email=postdata['email'])) > 0:           
            user = self.filter(email=postdata['email'])[0]
            if not bcrypt.checkpw(postdata['password'].encode(), user.password.encode()):
                errors.append('Hmm email or password incorrect, try again!')
        else:
            errors.append(' Email and password cannot be empty, please try again!')

        if errors:
            return errors
        return user
                 
            
class User(models.Model):
    fName = models.CharField(max_length = 20)
    lName = models.CharField(max_length= 20)
    email = models.CharField(max_length= 20)
    password = models.CharField(max_length= 20, default="none")
    gender = models.CharField(max_length = 20)
    birthday = models.DateTimeField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

