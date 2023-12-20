# forms.py
from django import forms
from .models import Dokumen

class DokumenForm(forms.ModelForm):
    class Meta:
        model = Dokumen
        fields = ['nama', 'document', 'program_pendidikan']  # Sertakan program_pendidikan di sini