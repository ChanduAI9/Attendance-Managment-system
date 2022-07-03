from . import views
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns=[
path('redirect-admin',RedirectView.as_view(url="/admin"),name="redirect-admin"),
path('login',auth_views.LoginView.as_view(template_name="loginpage.html",redirect_authenticated_user=True),name='login'),
path('loginuser',views.user_login,name='loginuser'),
path('registeruser',views.user_register,name='registeruser'),
path('',views.home,name='homepage'),
path('logout',views.user_logout,name='logout'),
path('profile',views.profile_data,name='profile'),
path('forgotpassword',views.forgot_password,name='forgotpassword'),
path('branch',views.branch_data,name='branch'),
path('teachers',views.teacher_data,name='teachers'),
path('class',views.classes_data,name='class'),
path('student',views.student_data,name='student'),
path('attendance',views.attendance_data,name='attendance'),
path('passwordupdate',views.password_update,name="passwordupdate"),
path('updateprofile',views.profile_update,name='updateprofile'),
]
