# Generated by Django 2.2.1 on 2019-05-11 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'ordering': ('user', '-created_at')},
        ),
        migrations.AlterModelOptions(
            name='rate',
            options={'ordering': ('user', '-created_at')},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-created_at',)},
        ),
    ]