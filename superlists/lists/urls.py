from django.urls import path
from lists import views

urlpatterns = [
    path('new', views.newListView, name = 'new_list'),
    path('<int:list_id>/', views.listView, name = 'view_list'),
    # path('<int:list_id>/add_item', views.newItemView, name = 'new_item'),
]
