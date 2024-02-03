from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

#custom manager in Django is a way to add extra methods to a model to perform querying operations
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, password=None): #firstname, lastname,
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        
        if not password:
            raise ValueError('Users must have a password')

        #username = models.CharField(('username'), max_length=30, blank=True)

        user.set_password(password)
        user.save(using=self._db)
        return user


#AbstractBaseUser: This is a base class provided by Django's authentication system. 
#It's an abstract class that implements the core authentication framework but leaves out some details which you need to specify in your User model. By inheriting from AbstractBaseUser, your User class can have custom user-related fields and methods, while still plugging into Django's authentication framework. 
#This is useful if you want to define a user model that differs from Django's built-in user model.
#models.Model: This is the base class for all models in Django's ORM. Inheriting from models.Model means that User is a Django model and can be mapped to a database table. 
#models.Model provides essential functionalities like saving to or fetching from the database, defining fields, etc.
class User(AbstractUser, models.Model):
    # email = models.EmailField(
    #     verbose_name='email address',
    #     max_length=255,
    #     unique=True,
    # )
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    #USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True