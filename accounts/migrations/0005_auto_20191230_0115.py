# Generated by Django 3.0 on 2019-12-30 01:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_blogger_displayname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogger',
            old_name='timeFirstLogin',
            new_name='timeFirstModification',
        ),
    ]
