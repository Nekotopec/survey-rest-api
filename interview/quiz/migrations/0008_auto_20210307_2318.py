# Generated by Django 2.2.16 on 2021-03-07 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20210302_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answeroption',
            name='id',
            field=models.PositiveIntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.PositiveIntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
