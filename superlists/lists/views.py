from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item
# Create your views here.

def indexView(request):
    print('entered index view. Method = ' + request.method)
    if request.method == 'POST':
        Item.objects.create(text = request.POST['item_text'])
        return redirect('/')

    return render(request, 'lists/index.html', {
        'items' : Item.objects.all()
    })
