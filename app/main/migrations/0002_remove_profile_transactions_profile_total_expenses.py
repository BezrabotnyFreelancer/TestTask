# Generated by Django 4.1.3 on 2022-11-14 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='transactions',
        ),
        migrations.AddField(
            model_name='profile',
            name='total_expenses',
            field=models.FloatField(default=0.0, verbose_name='Total_expenses'),
        ),
    ]
