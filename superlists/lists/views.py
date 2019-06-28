from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
# Create your views here.

def indexView(request):
    return render(request, 'lists/index.html', {'form': ItemForm()})

def listView(request, list_id):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if len(text) == 0:
            return render(request, 'lists/list.html', {
                'list' : List.objects.get(id = list_id),
                'form' : ItemForm(data=request.POST)
            })
        list_ = List.objects.get(id = list_id)
        Item.objects.create(text = text, list = list_)

    return render(request, 'lists/list.html', {
        'list' : List.objects.get(id = list_id),
        'form' : ItemForm(),
    })

def newListView(request):
    text = request.POST.get('text', '')
    if len(text) == 0:
        return render(
            request,
            'lists/index.html',
            {
                'form' : ItemForm(data=request.POST)
             }
        )
    list_ = List.objects.create()
    Item.objects.create(text = text, list = List.objects.get(id = list_.id))
    return redirect('list_view', list_.id)
