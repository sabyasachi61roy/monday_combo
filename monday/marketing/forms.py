from django import forms

from.models import Marketing

class MarketingForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Receive promotional email?', required=False)
    class Meta:
        model = Marketing
        fields = [
            'subscribed'
        ]