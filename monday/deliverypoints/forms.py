from django import forms
from .models import SelectDeliveryPoint

class SelectDeliveryPointForm(forms.ModelForm):
    class Meta:
        model = SelectDeliveryPoint
        fields = [
            'delivery_point'
        ]