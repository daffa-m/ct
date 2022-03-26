from django.forms import ModelForm
from image_process.models import ImageFile


class UploadImageForm(ModelForm):
    class Meta:
        model = ImageFile
        fields = ['image']