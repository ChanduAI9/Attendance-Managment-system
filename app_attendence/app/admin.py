from django.contrib import admin
from app.models import Branch,UserProfile,student,Class,class_student,Attendance,attendance2
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Branch)
admin.site.register(student)
admin.site.register(Class)
admin.site.register(class_student)
admin.site.register(Attendance)
admin.site.register(attendance2)
