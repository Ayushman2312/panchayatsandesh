# Generated by Django 5.1.6 on 2025-03-31 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0008_archivenews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivenews',
            name='news_type',
            field=models.CharField(default='Archive News', max_length=100),
        ),
    ]
