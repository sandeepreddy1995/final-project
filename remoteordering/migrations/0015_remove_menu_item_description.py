# Generated by Django 2.0.5 on 2018-06-17 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remoteordering', '0014_auto_20180615_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu_item',
            name='Description',
        ),
    ]