from django.db import models
import uuid

# Create your models here.

class User(models.Model):
    email = models.EmailField(unique = True, primary_key = True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True

    def __str__(self):
        return f'{self.email}'

class Token(models.Model):
    uid = models.CharField(default = uuid.uuid4, max_length = 40)
    email = models.EmailField()
