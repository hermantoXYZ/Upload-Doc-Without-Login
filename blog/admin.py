# admin.py
from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ExportActionMixin
from .models import Dokumen
from .resources import DokumenResource

class DokumenAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = DokumenResource
    list_display = ('nama', 'status_display', 'program_pendidikan', 'display_document', 'user_username')

    def display_document(self, obj):
        document_url = obj.document.url
        return format_html('<a href="{}" target="_blank">{}</a>', document_url, obj.document.name)

    display_document.short_description = 'Document'

    def user_username(self, obj):
        return obj.user.username if obj.user else "None"

    user_username.short_description = 'User'

admin.site.register(Dokumen, DokumenAdmin)
