# Generated by Django 3.2.7 on 2021-09-24 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
