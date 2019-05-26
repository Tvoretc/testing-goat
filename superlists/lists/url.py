from django.urls import path
from lists import views

urlpatterns = [
    path('lists/new', views.newListView, name = 'new_list'),
    path('lists/<int:list_id>/', views.listView, name = 'view_list'),
    path('lists/<int:list_id>/add_item', views.newItem, name = 'new_item'),
]
