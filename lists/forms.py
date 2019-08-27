from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item, List

EMPTY_ITEM_ERROR = 'Can`t have an empty list item,'
DUPLICATE_ITEM_ERROR = 'You`ve already entered this item. Can`t have duplicates.'

class ItemForm(forms.models.ModelForm):

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
        self.instance.list = list_
        return super().save()


class ExistingListItemForm(ItemForm):
    def __init__(self, list_,  *args, **kwargs):
        ret = super().__init__(*args, **kwargs)
        self.instance.list = list_
        return ret

    def save(self):
        return forms.models.ModelForm.save(self)

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
