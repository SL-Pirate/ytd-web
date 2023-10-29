# Generated by Django 4.2.5 on 2023-09-30 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Downloadable',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('path', models.TextField()),
                ('name', models.TextField()),
                ('folder', models.TextField()),
                ('expiration_period', models.IntegerField(default=1)),
            ],
        ),
    ]