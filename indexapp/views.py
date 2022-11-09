from atexit import register
from datetime import datetime
from urllib import request
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import *
from .forms import *


# Create your views here.
def index(request):
    data = Student.objects.all().order_by('-id')
    context = {'datas': data}
    return render(request,'index.html', context)


def student_attendance(request):
    data = Attendance.objects.all().order_by('-id')
    context = {'datas': data, 'name':'All attandance'}
    return render(request, 'attendance.html', context)


def student_reg(request):
    return render(request,'student_registration.html')

def student_perf(request):
    return render(request,'student_performance.html')

def teacher_reg(request):
    return render(request,'teacher_registertion.html')

def teacher_perf(request):
    return render(request,'teacher_perf.html')


@api_view(['POST'])
def insert_attendance_post(request):
    print(request.data)
    card = str(request.data['card'].replace(' ', ''))
    alcohol = int(request.data['alcohol'])
    identifier = request.data['identifier']
    user = '- No student found'
    attend_status = "" # by default attandance is okay

    if alcohol >= 30:
        attend_status = "drunk" # he is drunk
    try:
        get_student = Student.objects.get(card_id=card)
        get_student_class = get_student.class_name
        try:
            get_identifier_class = OurClass.objects.get(identifier=identifier)
        except:
            attend_status = "class not found" #invalid class identifier
            return Response(attend_status, status=status.HTTP_304_NOT_MODIFIED)

        if get_identifier_class != get_student_class:
            attend_status = "not our student" # not belong to this class
            return Response(attend_status)
        insert_data = Attendance()
        insert_data.student = get_student
        insert_data.class_attend = get_identifier_class
        insert_data.alcohol_level = alcohol
        insert_data.save()
        user = get_student.fullname
    except:
        attend_status = "student card not found" # student not found
    return HttpResponse(f'{attend_status}{user}', status=status.HTTP_200_OK)


# http://127.0.0.1/api/idatechiot/card1002alcohol8/
@api_view(['GET'])
def insert_attendance_get(request, identifier, card, alcohol):
    attend_status = "" # by default attandance is okay
    user = 'No student found'
    if alcohol >= 30:
        attend_status = "drunk" # he is drunk
    try:
        get_student = Student.objects.get(card_id=card)
        get_student_class = get_student.class_name
        try:
            get_identifier_class = OurClass.objects.get(identifier=identifier)
        except:
            attend_status = "class not found" #invalid class identifier
            return Response(attend_status)

        if get_identifier_class != get_student_class:
            attend_status = "not our student" # not belong to this class
            return Response(attend_status)
        insert_data = Attendance()
        insert_data.student = get_student
        insert_data.class_attend = get_identifier_class
        insert_data.alcohol_level = alcohol
        insert_data.save()
        user = get_student.fullname
    except:
        attend_status = "student card not found " # student was not found
    return HttpResponse(f'{attend_status} {user}', status=status.HTTP_200_OK)


def register_student(request):
    form = CreateUserForm()
    if  request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../')

    context = {'form': form}
    return render(request, 'signup.html', context)

# datetime.today().date()

def today_attendance(request):
    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day
    data = Attendance.objects.filter(arrive_time__year=year,
    arrive_time__month=month, arrive_time__day=day).order_by('-id')
    context = {'datas': data, 'name':'TODAY ATTANDANCE'}
    return render(request, 'attendance.html', context)


def view_selected_attendance(request, myid):
    get_student = Student.objects.get(id=myid)
    data = Attendance.objects.filter(student=get_student).order_by('-id')
    context = {'datas': data, 'name':'SELECTED STUDENT ATTANDENCE'}
    return render(request, 'attendance.html', context)


def test(request):
    pass
