# Generated by Django 4.0 on 2022-06-28 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_alter_datatraining_penulis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datatraining',
            name='judul',
            field=models.CharField(max_length=70, null=True),
        ),
    ]
