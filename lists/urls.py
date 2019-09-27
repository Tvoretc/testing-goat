from django.urls import path, register_converter

from lists import views, converters

register_converter(converters.EmailConverter, 'emailconv')

# 'lists/'
urlpatterns = [
    path('new', views.newListView, name = 'new_list'),
    path('<int:list_id>', views.listView, name = 'list_view'),
    path('<int:list_id>/share', views.listShareView, name ='list_share'),
    # path('<int:list_id>/add_item', views.newItemView, name = 'new_item'),
    path('users/<emailconv:email>', views.myListsView, name = 'my_lists'),
]
