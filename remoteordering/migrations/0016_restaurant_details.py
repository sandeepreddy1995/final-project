# Generated by Django 2.0.5 on 2018-06-18 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remoteordering', '0015_remove_menu_item_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('No_Of_Tables', models.IntegerField()),
                ('Restaurant_Name', models.CharField(max_length=250)),
            ],
        ),
    ]