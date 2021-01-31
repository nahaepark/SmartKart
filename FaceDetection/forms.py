from django import forms

class UploadImageForm(forms.Form):
    title = forms.CharField(max_length=50)
    image = forms.ImageField()

from .models import ImageUploadModel, basket, memo
from django_summernote.widgets import SummernoteWidget

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploadModel
        fields = ('document',)

class basketForm(forms.ModelForm):
    class Meta:
        model = basket
        fields = ('pdname','pdprice')
        #help_text="제품명 수정"

class memoModelForm(forms.ModelForm):
    class Meta:
        model = memo
        fields = ('label',)