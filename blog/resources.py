# blog/resources.py
from import_export import resources, fields
from django.urls import reverse
from django.utils.html import format_html

from .models import Dokumen

class DokumenResource(resources.ModelResource):
    display_document = fields.Field(column_name='Document', attribute='document')
    status_display = fields.Field(column_name='Status', attribute='status')
    program_pendidikan = fields.Field(column_name='Program Pendidikan', attribute='program_pendidikan')
    user_username = fields.Field(column_name='User', attribute='user__username')

    class Meta:
        model = Dokumen
        fields = ('nama', 'status_display', 'program_pendidikan', 'display_document', 'user_username')
        export_order = ('nama', 'status_display', 'program_pendidikan', 'display_document', 'user_username')

    def dehydrate_display_document(self, dokumen):
        return format_html('{}{}', reverse('admin:blog_dokumen_change', args=[dokumen.id]), dokumen.document.name)

    def dehydrate_status_display(self, dokumen):
        return dokumen.get_status_display()

    def dehydrate_user_username(self, dokumen):
        return dokumen.user.username if dokumen.user else "None"
