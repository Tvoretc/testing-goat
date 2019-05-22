from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item
# Create your views here.

def indexView(request):
    if request.method == 'POST':
        Item.objects.create(text = request.POST['item_text'])
        return redirect('/lists/the-only-list/')

    return render(request, 'lists/index.html', {
        'items' : Item.objects.all()
    })

def listView(request):
        return render(request, 'lists/list.html', {
            'items' : Item.objects.all()
        })
