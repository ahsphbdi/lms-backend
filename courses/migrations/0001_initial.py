# Generated by Django 4.2 on 2023-05-20 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teachers', '__first__'),
        ('trs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_course_number', models.PositiveSmallIntegerField()),
                ('start_date', models.DateField(help_text='The date of the first session')),
                ('end_date', models.DateField(help_text='The date of the last session')),
                ('tuition', models.DecimalField(decimal_places=3, help_text='course tuition', max_digits=14)),
                ('percentage_required_for_tuition', models.DecimalField(decimal_places=3, default=100, help_text='Tuition percentage required to enter the course', max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='CourseTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupCourseTimes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trs.semester')),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_times', to='trs.timeslot')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='course_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='courses.coursetitle'),
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trs.semester'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='courses', to='teachers.teacher'),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_number', models.PositiveBigIntegerField(blank=True, null=True)),
                ('date', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('title', models.CharField(blank=True, max_length=300)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='courses.course')),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trs.timeslot')),
            ],
            options={
                'unique_together': {('date', 'time_slot')},
            },
        ),
        migrations.AddConstraint(
            model_name='groupcoursetimes',
            constraint=models.UniqueConstraint(fields=('time_slot', 'semester'), name='unique_course_times'),
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.UniqueConstraint(fields=('course_title', 'group_course_number', 'semester'), name='unique_course'),
        ),
    ]