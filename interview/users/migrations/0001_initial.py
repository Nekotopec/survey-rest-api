# Generated by Django 2.2.10 on 2021-02-12 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sessions.Session')),
            ],
        ),
    ]