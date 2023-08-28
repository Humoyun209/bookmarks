from django import forms
import requests
from django.core.files.base import ContentFile

from django.utils.text import slugify

from images.models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'description', 'url']
        widgets = {
            'url': forms.HiddenInput
        }
    def save(self, commit=True):
        image = super().save(commit=False)
        url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        response = requests.get(url)
        image.image.save(image_name,
                         ContentFile(response.content),
                         save=False)
        if commit:
            image.save()
        return image
    def clean_url(self):
        url: str = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            forms.ValidationError('The given URL does not\
                                  match valid image extensions.')
        return url

