from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
# Create your views here.

def indexView(request):
    return render(request, 'lists/index.html', {'form': ItemForm()})

def listView(request, list_id):
    list_ = List.objects.get(id = list_id)
    form = ItemForm(list_ = list_)
    if request.method == 'POST':
        form = ItemForm(list_ = list_, data = request.POST)
        if form.is_valid():
            form.save(list_ = list_)
            return render(request, 'lists/list.html', {
                'list' : list_,
                'form' : form,
            })

    return render(request, 'lists/list.html', {
        'list' : list_,
        'form' : form,
    })

def newListView(request):
    form = ItemForm(data = request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(list_ = list_)
        return redirect(list_)
    return render(request, 'lists/index.html', {'form' : form})
