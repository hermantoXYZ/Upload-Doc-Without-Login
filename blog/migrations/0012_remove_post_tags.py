# Generated by Django 4.2.5 on 2023-12-19 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_dokumen_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
    ]
