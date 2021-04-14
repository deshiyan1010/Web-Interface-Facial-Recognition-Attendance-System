# Generated by Django 3.1.2 on 2020-10-14 18:08

from django.db import migrations, models
import hq.models


class Migration(migrations.Migration):

    dependencies = [
        ('hq', '0006_remove_personimage_pictures'),
    ]

    operations = [
        migrations.AddField(
            model_name='personimage',
            name='pictures',
            field=models.ImageField(default=1, upload_to=hq.models.get_upload_path),
            preserve_default=False,
        ),
    ]