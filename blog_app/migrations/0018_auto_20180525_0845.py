# Generated by Django 2.0.5 on 2018-05-25 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0017_auto_20180525_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]