from accounts.models import User, Roles
from trs.models import Room, Semester, TimeSlot, Semseters, Days_Of_Week
from courses.models import CourseTitle, Course, CourseTime
from teachers.models import Teacher
from students.models import Student, StudentEnroll


def run():
    superuser = User.objects.create_superuser(
        'amir',
        email='amir@amir.amir',
        password='Abcd_1234',
        first_name="amir",
        last_name='espahbodi',
        phone_number='+989013971301',
    )
    print(f"superuser {superuser} created!\n\n")

    users: list[User] = [
        User.objects.create_user(
            f'teacher{i}' if i < 3 else f'student{i-3}',
            email=f'teacher{i}@teacher.teacher' if i < 3 else f'student{i-3}@student.student',
            password=f'Abcd_1234',
            first_name=f"teacher{i}" if i < 3 else f"student{i-3}",
            last_name=f'teacher' if i < 3 else f'student',
            phone_number=f'+98901397140{i}' if i < 3 else f'+98901397150{i-3}',
            role=Roles.NOT_DEFINED
        )
        for i in range(10)
    ]
    print(f"users {users} created!\n\n")

    student: list[Student] = [
        Student.objects.create(
            user=users[i],
            school="some",
            degree=1,
            field="some"
        ) for i in range(3, 10)
    ]
    print(f"student {student} created!\n\n")

    teachers: list[Teacher] = [
        Teacher.objects.create(
            user=users[i],
            experience=30
        ) for i in range(3)
    ]
    print(f"teachers {teachers} created!\n\n")

    rooms: list[Room] = [
        Room.objects.create(
            room_title="room 1",
            capacity=45
        ),
        Room.objects.create(
            room_title="room 2",
            capacity=50
        )
    ]
    print(f"rooms {rooms} created!\n\n")

    semesters: list[Semester] = [
        Semester.objects.create(
            year='1402-1403',
            semester=Semseters.FIRST_SEMESTER
        ),
        Semester.objects.create(
            year='1402-1403',
            semester=Semseters.SECOND_SEMESTER
        )
    ]
    print(f"semesters {semesters} created!\n\n")

    times = [
        {'start': '08:00:00', 'end': '09:30:00'},
        {'start': '10:00:00', 'end': '11:30:00'},
        {'start': '14:00:00', 'end': '15:30:00'}
    ]
    timeslots: list[TimeSlot] = [
        TimeSlot.objects.create(
            room_number=rooms[i],
            day=day_of_week,
            start=time['start'],
            end=time['end']
        )
        for time in times
        for i in range(0, 2)
        for day_of_week in [Days_Of_Week.MONDAY, Days_Of_Week.THURSDAY, Days_Of_Week.TUESDAY, Days_Of_Week.SUNDAY]
    ]
    print(f"timeslots {timeslots} created!\n\n")

    coursetitles: list[CourseTitle] = [
        CourseTitle.objects.create(
            title='math'
        ),
        CourseTitle.objects.create(
            title='physic'
        ),
        CourseTitle.objects.create(
            title='algebra'
        )
    ]
    print(f"coursetitles {coursetitles} created!\n\n")

    courses: list[Course] = [
        Course.objects.create(
            group_course_number=j,
            course_title=coursetitles[i],
            semester=semesters[0],
            teacher=teachers[i],
            start_date='2023-6-1',
            end_date='2023-9-1',
            tuition=10000000,
            percentage_required_for_tuition=27.5
        ) for j in range(1, 4) for i in range(0, 3)
    ]
    print(f"courses {courses} created!\n\n")

    studentEnroll: list[StudentEnroll] = [
        StudentEnroll.objects.create(
            student=student[j],
            course=courses[i],
        ) for j in range(0, len(student)) for i in range(0, len(courses)) if (i+j < len(student))
    ]
    print(f"studentEnroll {studentEnroll} created!\n\n")

    course_time: list[CourseTime] = [
        CourseTime.objects.create(
            course=courses[index % len(courses)],
            semester=courses[index % len(courses)].semester,
            time_slot=timeslots[index]
        )
        for index in range(len(timeslots))
    ]
    print(f"course_time {course_time} created!\n\n")
