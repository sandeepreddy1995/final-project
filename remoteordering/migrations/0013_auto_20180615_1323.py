# Generated by Django 2.0.6 on 2018-06-15 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remoteordering', '0012_order_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Name',
        ),
        migrations.AddField(
            model_name='order_management',
            name='Name',
            field=models.CharField(default='sandeep', max_length=250),
            preserve_default=False,
        ),
    ]
