# Generated by Django 4.2.3 on 2023-09-01 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('used_car', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usedcar',
            name='comment',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
