from django.db import models
from teachers.models import Teacher
from jalali_date import date2jalali
from trs.models import TimeSlot, Semester
# Create your models here.


class CourseTitle(models.Model):
    id = models.AutoField(
        primary_key=True,
        auto_created=True,
        serialize=False,
        verbose_name='ID'
    )
    title = models.CharField(
        unique=True,
        max_length=255
    )

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.title


class Course(models.Model):
    id = models.AutoField(
        primary_key=True,
        auto_created=True,
        serialize=False,
        verbose_name='ID',
        db_index=True
    )
    group_course_number = models.PositiveSmallIntegerField()
    course_title = models.ForeignKey(
        CourseTitle, on_delete=models.PROTECT, related_name="courses")
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.DO_NOTHING, related_name="courses")
    start_date = models.DateField(help_text='The date of the first session')
    end_date = models.DateField(help_text='The date of the last session')
    tuition = models.DecimalField(
        max_digits=14, decimal_places=3,
        help_text='course tuition'
    )
    percentage_required_for_tuition = models.DecimalField(
        default=100, max_digits=6, decimal_places=3,
        help_text='Tuition percentage required to enter the course'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'course_title',
                    'group_course_number',
                    'semester'
                ],
                name='unique_course'
            )
        ]

    def get_jalali_end_date(self):
        return str(date2jalali(self.end_date))

    def get_jalali_start_date(self):
        return str(date2jalali(self.start_date))

    def __str__(self):
        return f"{self.course_title.title} {self.group_course_number} {self.semester}"

    def __unicode__(self):
        return self.__str__()


class CourseTime(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course_times'
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='course_times'
    )

    # def save(self, orce_insert=False, force_update=False, using=None, update_fields=None):
    #     self.semester = self.course.semester
    #     super().save(orce_insert, force_update, using, update_fields)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'time_slot', 'semester'
                ],
                name='unique_courses_course_time'
            )
        ]
        db_table = "courses_course_time"

    def __str__(self):
        return f"{self.time_slot} {self.course}"


class Session(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='sessions'
    )

    session_number = models.PositiveBigIntegerField(null=True, blank=True)

    date = models.DateField()
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE
    )
    description = models.TextField(blank=True)
    title = models.CharField(blank=True, max_length=300)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'date', 'time_slot'
                ],
                name='unique_session_date_time_slot'
            )
        ]

    def get_jalali_date(self):
        return str(date2jalali(self.date))

    def __str__(self):
        return f"{self.course} - session : {self.session_number}"
