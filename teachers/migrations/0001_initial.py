# Generated by Django 4.2.1 on 2023-05-29 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='teacher_user', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('experience', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherPublished',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published', models.CharField(max_length=300)),
                ('publisher', models.CharField(max_length=300)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers.teacher')),
            ],
            options={
                'db_table': 'teachers_teacher_published',
            },
        ),
        migrations.CreateModel(
            name='TeacherEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.CharField(max_length=300)),
                ('university', models.CharField(max_length=300)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers.teacher')),
            ],
            options={
                'db_table': 'teachers_teacher_education',
            },
        ),
    ]
