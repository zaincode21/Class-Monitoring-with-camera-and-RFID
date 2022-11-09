from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('api/', views.insert_attendance_post),
    path('api/<str:identifier>/card<str:card>alcohol<int:alcohol>/', views.insert_attendance_get),
    path('student_registertion/', views.student_reg),
    path('student_performance/', views.student_perf),
    path('teacher_perf/', views.teacher_perf),
    path('teacher_registertion/', views.teacher_reg),
    path('signup/', views.register_student),
    path('attendance/', views.student_attendance),
    path('today/', views.today_attendance),
    path('view/<int:myid>/', views.view_selected_attendance),
    path('test/', views.test),




]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
