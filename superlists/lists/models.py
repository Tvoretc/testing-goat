from django.db import models
from django.urls import reverse

# Create your models here.

class List(models.Model):
    url = models.TextField()

    def get_absolute_url(self):
        return reverse('list_view', args=[self.id])


class Item(models.Model):
    text = models.TextField(blank = False)
    list = models.ForeignKey(List, on_delete = models.CASCADE, default = None)

    def __str__(self):
        return self.text
