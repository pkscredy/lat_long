from address.models import Document
from django import forms


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('id', 'file_name', 'document', )
