# Generated by Django 3.0.6 on 2020-06-03 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20200603_0532'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='category',
            field=models.CharField(default='pizza', max_length=64),
        ),
    ]
