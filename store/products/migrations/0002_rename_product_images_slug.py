# Generated by Django 3.2.3 on 2021-06-04 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='product',
            new_name='slug',
        ),
    ]