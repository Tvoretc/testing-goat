from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import ItemForm
# Create your views here.

def indexView(request):
    return render(request, 'lists/index.html', {'form': ItemForm()})

def listView(request, list_id):
    if request.method == 'POST':
        text = request.POST['item_text']
        if len(text) == 0:
            return render(request, 'lists/list.html', {
                'list' : List.objects.get(id = list_id),
                'error' : 'Can`t have an empty list item,'
                })
        list_ = List.objects.get(id = list_id)
        Item.objects.create(text = text, list = list_)

    return render(request, 'lists/list.html', {
        'list' : List.objects.get(id = list_id)
    })

def newListView(request):
    text = request.POST['item_text']
    if len(text) == 0:
        return render(request, 'lists/index.html', {'error' : 'Can`t have an empty list item,'})
    list_ = List.objects.create()
    Item.objects.create(text = text, list = List.objects.get(id = list_.id))
    return redirect('list_view', list_.id)
