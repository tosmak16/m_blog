# Generated by Django 2.0.5 on 2018-05-24 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0011_auto_20180524_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_date',
            field=models.DateTimeField(null=True),
        ),
    ]