from django import forms

from bcmr.models import Token


class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = (
            'category',
            'name',
            'description',
            'symbol',
            'decimals',
            'icon',
        )
