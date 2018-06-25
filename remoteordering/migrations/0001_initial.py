# Generated by Django 2.0.5 on 2018-05-30 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu_items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(max_length=200)),
                ('Sub_Category', models.CharField(max_length=200)),
                ('Item_name', models.CharField(max_length=250)),
                ('Price', models.IntegerField()),
                ('Description', models.CharField(max_length=500)),
                ('Status', models.CharField(max_length=50)),
            ],
        ),
    ]
