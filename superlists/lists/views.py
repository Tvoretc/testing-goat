from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
# Create your views here.

def indexView(request):
    return render(request, 'lists/index.html')

def listView(request, list_id):
    if request.method == 'POST':
        text = request.POST['item_text']
        if len(text) == 0:
            return render(request, 'lists/index.html', {'error' : 'Can`t have an empty list item,'})
        list_ = List.objects.get(id = list_id)
        Item.objects.create(text = text, list = list_)
        return redirect(f'/lists/{list_id}/')

    return render(request, 'lists/list.html', {
        'list' : List.objects.get(id = list_id)
    })

def newListView(request):
    text = request.POST['item_text']
    if len(text) == 0:
        return render(request, 'lists/index.html', {'error' : 'Can`t have an empty list item,'})
    list_ = List.objects.create()
    Item.objects.create(text = text, list = List.objects.get(id = list_.id))
    return redirect(f'/lists/{list_.id}/')

# def newItemView(request, list_id):
#     text = request.POST['item_text']
#     if len(text) == 0:
#         return render(request, 'lists/index.html', {'error' : 'Can`t have an empty list item,'})
#     list_ = List.objects.get(id = list_id)
#     Item.objects.create(text = text, list = list_)
#     return redirect(f'/lists/{list_id}/')
