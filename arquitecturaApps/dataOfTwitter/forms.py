from django import forms

class ProcessUrl(forms.Form):
    url_tags = forms.URLField(label=False, max_length=1000,
                              widget=forms.TextInput(attrs={'placeholder': 'Url de documento de TAGS'}))
