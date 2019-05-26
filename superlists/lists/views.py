from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
# Create your views here.

def indexView(request):
    return render(request, 'lists/index.html')

def listView(request, list_id):
        return render(request, 'lists/list.html', {
            'list' : List.objects.get(id = list_id)
        })

def newListView(request):
    list_ = List.objects.create()
    Item.objects.create(text = request.POST['item_text'], list = List.objects.get(id = list_.id))
    return redirect(f'/lists/{list_.id}/')

def newItem(request, list_id):
    list_ = List.objects.get(id = list_id)
    Item.objects.create(text = request.POST['item_text'], list = list_)
    return redirect(f'/lists/{list_id}/')
