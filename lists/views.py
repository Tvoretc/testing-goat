from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm

User = get_user_model()
# Create your views here.

def indexView(request):
    return render(request, 'lists/index.html', {'form': ItemForm()})

def listView(request, list_id):
    list_ = List.objects.get(id = list_id)
    form = ExistingListItemForm(list_ = list_)
    if request.method == 'POST':
        form = ExistingListItemForm(list_ = list_, data = request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'lists/list.html', {
        'list' : list_,
        'form' : form,
    })

def newListView(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'lists/index.html', {'form': form})

def myListsView(request, email):
    owner = User.objects.get(email = email)

    return render(request, 'lists/my_lists.html', {'owner':owner})
