from django import forms

class AlbumImageUploadForm(forms.Form):
    albumart = forms.ImageField()
    # file = forms.ImageField()
