from django.db import models
from django.contrib.auth.models import User

# Create your models here.
user_types =(
    ('user','user'),
    ('school','school'),
    ('admin','admin'),
    ('not-active','not-active'),
)


class School(models.Model):
    school_id = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    school = models.CharField(null=False, max_length=40)
    school_tel = models.CharField(null=False, max_length=20)

    def __str__(self):
        return self.school


class OurClass(models.Model):
    class_id = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    school = models.ForeignKey(School, null=False, on_delete=models.CASCADE)
    identifier = models.CharField(null=False, unique=True, max_length=40)
    name = models.CharField(null=False, max_length=40)
    class_tel = models.CharField(null=False, max_length=20)

    def __str__(self):
        return self.name

class Student(models.Model):
    # student_id = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    class_name = models.ForeignKey(OurClass, null=False, on_delete=models.CASCADE, default=1)
    user_type = models.CharField(default='user', max_length=24, choices=user_types)
    card_id = models.CharField(max_length=100, null=True, unique=True)
    fullname = models.CharField(null=False, max_length=40)
    address = models.CharField(null=False, max_length=40)
    telephone = models.CharField(null=False, max_length=20)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.fullname


class Attendance(models.Model):
    student = models.ForeignKey(Student, null=False, on_delete=models.CASCADE)
    class_attend = models.ForeignKey(OurClass, null=False, on_delete=models.CASCADE)
    arrive_time = models.DateTimeField(auto_now=True)
    alcohol_level = models.FloatField(default=0)

    def __str__(self):
        if self.alcohol_level > 20:
            my_status = "Drunk"
        else:
            my_status = "Attendance"
        return f'{my_status}: {self.class_attend} -- {self.student} -- AT -- {self.arrive_time}'
