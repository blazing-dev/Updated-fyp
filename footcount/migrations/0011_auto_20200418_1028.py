# Generated by Django 3.0.3 on 2020-04-18 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('footcount', '0010_auto_20200418_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footcount',
            name='count',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='footcount',
            name='month',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
