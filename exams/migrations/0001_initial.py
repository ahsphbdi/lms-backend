# Generated by Django 4.2.1 on 2023-05-29 11:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('exam_number', models.PositiveSmallIntegerField(blank=True, editable=False, null=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='courses.session')),
            ],
            options={
                'db_table_comment': 'exam for each session of course',
            },
        ),
        migrations.CreateModel(
            name='FTQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='exam/questions/')),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.exam')),
            ],
            options={
                'db_table': 'exams_ftquestion',
                'db_table_comment': 'Each exam can have several file/text type questions. This table stores questions of this type for each exam',
            },
        ),
        migrations.CreateModel(
            name='FTQuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(blank=True, null=True)),
                ('answer_file', models.FileField(upload_to='assignment/teacher/answers/')),
                ('ft_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.ftquestion')),
            ],
            options={
                'db_table': 'exams_ftquestion_answer',
                'db_table_comment': 'answer of the file/text type questions',
            },
        ),
        migrations.CreateModel(
            name='EnrolledStudenTakeExam',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('visit_datetime', models.DateTimeField(auto_now_add=True)),
                ('finish_datetime', models.DateTimeField(blank=True, null=True)),
                ('score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolled_students_exam', to='exams.exam')),
                ('student_enroll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.studentenroll')),
            ],
            options={
                'db_table': 'exams_enrolled_students_take_exam',
                'db_table_comment': 'a table betwen student takes and exam. It shows that the student participated in the exam',
            },
        ),
        migrations.CreateModel(
            name='EnrolledStudenExamFTQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('send_datetime', models.DateTimeField()),
                ('finish_datetime', models.DateTimeField()),
                ('answered_text', models.TextField(blank=True, null=True)),
                ('answered_file', models.FileField(blank=True, null=True, upload_to='exam/students/answers/')),
                ('enrolled_students_take_exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.enrolledstudentakeexam')),
                ('ft_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.ftquestion')),
            ],
            options={
                'db_table': 'exams_enrolled_studen_exam_ftquestion',
                'db_table_comment': "This table stores the student's answer to the exam file/text question",
            },
        ),
        migrations.AddConstraint(
            model_name='enrolledstudentakeexam',
            constraint=models.UniqueConstraint(fields=('exam', 'student_enroll'), name='unique_exams_enrolled_students_take_exam'),
        ),
        migrations.AddConstraint(
            model_name='enrolledstudenexamftquestion',
            constraint=models.UniqueConstraint(fields=('enrolled_students_take_exam', 'ft_question'), name='unique_exams_enrolled_studen_exam_ftquestion'),
        ),
    ]