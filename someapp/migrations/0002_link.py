# Generated by Django 3.1 on 2020-09-05 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('someapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=1024, null=True)),
                ('remark', models.TextField(max_length=1024, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
