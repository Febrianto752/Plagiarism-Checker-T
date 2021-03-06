# Generated by Django 4.0 on 2022-06-25 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mahasiswa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('npm', models.CharField(max_length=20, unique=True)),
                ('nama', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('jurusan', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('no_telp', models.CharField(blank=True, max_length=20, null=True)),
                ('semester', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'mahasiswa',
            },
        ),
        migrations.CreateModel(
            name='Skripsi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('pdf', models.FileField(upload_to='mahasiswa/skripsi/')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('mahasiswa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mahasiswa.mahasiswa')),
            ],
            options={
                'db_table': 'skripsi',
            },
        ),
        migrations.CreateModel(
            name='ReportPlagiarism',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_similiarity', models.TextField(null=True)),
                ('plagiarism_percentage', models.FloatField(null=True)),
                ('is_done', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('skripsi', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mahasiswa.skripsi')),
            ],
            options={
                'db_table': 'report_plagiarism',
            },
        ),
    ]
