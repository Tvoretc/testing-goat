from django import forms

from lists.models import Item, List

EMPTY_ITEM_ERROR = 'Can`t have an empty list item,'

class ItemForm(forms.models.ModelForm):

    def __init__(self, list_ = None, *args, **kwargs):
        ret = super().__init__(*args, **kwargs)
        self.list = list_
        return ret


    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text' : forms.fields.TextInput(attrs={
                'placeholder' : "Enter a to-do item",
                'class' : "form-controll input-lg",
            })
        }
        error_messages={
            'text' : {'required' : EMPTY_ITEM_ERROR}
        }

    def save(self, list_):
        if self.list == None:
            self.instance.list = list_
        else:
            self.instance.list = self.list
        return super().save()
