# Generated by Django 3.1.2 on 2020-10-14 17:56

from django.db import migrations, models
import django.db.models.deletion
import hq.models


class Migration(migrations.Migration):

    dependencies = [
        ('hq', '0003_person_id_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='pictures',
        ),
        migrations.AlterField(
            model_name='person',
            name='id_number',
            field=models.CharField(max_length=128),
        ),
        migrations.CreateModel(
            name='PersonImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pictures', models.ImageField(upload_to=hq.models.get_upload_path)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hq.person')),
            ],
        ),
    ]
