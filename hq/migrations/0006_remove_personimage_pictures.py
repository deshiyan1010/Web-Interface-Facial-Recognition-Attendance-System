# Generated by Django 3.1.2 on 2020-10-14 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hq', '0005_auto_20201014_2329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personimage',
            name='pictures',
        ),
    ]
