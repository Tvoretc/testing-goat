from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.

class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        blank=True, null=True, on_delete=models.DO_NOTHING)

    @property
    def name(self):
        return self.item_set.first().text

    def get_absolute_url(self):
        return reverse('list_view', args=[self.id])

    @staticmethod
    def create_new(first_item_text, owner=None):
        list_ = List.objects.create(owner = owner)
        Item.objects.create(list = list_, text = first_item_text)
        return list_


class Item(models.Model):
    text = models.TextField(blank = False)
    list = models.ForeignKey(List, on_delete = models.CASCADE, default = None)

    class Meta:
        unique_together = ('text', 'list')

    def __str__(self):
        return self.text
