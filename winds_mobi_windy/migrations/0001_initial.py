# Generated by Django 3.2.13 on 2022-08-06 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Station",
            fields=[
                ("id", models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name="Id")),
            ],
        ),
    ]