# Generated by Django 5.0.4 on 2024-05-01 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_books_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='books',
            old_name='author',
            new_name='bauthor',
        ),
        migrations.RenameField(
            model_name='books',
            old_name='id',
            new_name='bid',
        ),
        migrations.RenameField(
            model_name='books',
            old_name='title',
            new_name='btitle',
        ),
    ]