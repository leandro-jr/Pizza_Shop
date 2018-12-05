# Generated by Django 2.0.3 on 2018-12-04 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(max_length=64)),
                ('size', models.CharField(max_length=64)),
                ('flavor', models.CharField(max_length=64)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
