from django.shortcuts import render
from unicodedata import category
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from app_attendence.settings import MEDIA_ROOT,MEDIA_URL
from django.http import HttpResponse
from datetime import datetime
import json
import pickle
import cdifflib
from django.contrib.auth.forms import UserCreationForm
from app.models import UserProfile,Branch,student,Class,class_student,Attendance,attendance2
from app.forms import user_registration,update_professor,profile_image,update_user_details,update_password,update_profile, save_branch,save_class,save_student,class_student_data
from django.views.generic import View
# Create your views here.
access={}
#user authentication

#user register

def user_register(request):
    user=request.user
    if user.is_authenticated:
        return redirect('homepage')
    context['title']="Register User"
    if request.method == 'POST':
        data=request.POST
        form_data =user_registration(data)
        if form_data.is_valid():
            user1=form_data.save()
            new_user=User.objects.all()
            try:
                profile=UserProfile.objects.get(user=new_user)
            except:
                profile_data= None
            if profile_data is None:
                UserProfile(user=new_user,date_of_birth=user['date_of_birth'],contact=user['contact'],branch_name=user['branch_name'],gender=user['gender'],profile_image=request.FILES['profile_image']).save()
            else:
                UserProfile.objects.filter(id=profile.id).update(user=new_user,date_of_birth=user['date_of_birth'],contact=user['contact'],branch_name=user['branch_name'],profile_image=request.FILES['profile_image'])
                profile_image=profile_image(request.POST,request.FILES,instance=profile_data)
                if profile_image.is_valid():
                    profile_image.save()
            username=form_data.cleaned_data.get('username')
            password=form_data.cleaned_data.get('password1')
            login_user=authenticate(username=username,password=password)
            login(request,login_user)
            return redirect("home page")
        else:
            context['form_data']=form_data
    return render(request,'signuppage.html',context)


@login_required
def home(request):
    access['title']="Home"
    branches=Branch.objects.count()
    teachers=UserProfile.objects.filter(user_type=1).count()
    if request.user.profile.user_type == 1:
        students=student.objects.count()
        classes=Class.objects.count()
    elif request.user.profile.user_type ==2:

        classes=Class.objects.filter(professor=request.user.profile).count()
        students=class_student.objects.filter(class_details__in=Class.objects.filter(professor=request.user.profile).values_list('id')).count()
    else:
        students=class_students.objects.filter(class_details__in=Class.objects.filter(professor=request.user.profile).values_list('id')).count()
    access['branches']=branches
    access['teachers']=teachers
    access['students']=students
    access['classes']=classes

    return render(request,'mainhome.html',access)



#login
def user_login(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')


#logout
def user_logout(request):
    logout(request)
    return redirect('/')

#Home Data

#forgot password
def forgot_password(request):
    return render(request,'forgetpassword.html')

#profile
def profile_data(request):
    access['title']="user's profile"
    return render(request,'profilepage.html',access)

#departments data
def branch_data(request):
    access['title']="Departments Details"
    user=UserProfile.objects.all()
    branch=Branch.objects.all()
    access['branch']=branch
    access['user']=user
    return render(request,'branch.html',access)

def teacher_data(request):
    access['title']="Teachers Details"
    teacher=UserProfile.objects.filter(user_type=2).all()
    access['teacher']=teacher
    return render(request,'teacher.html',access)

def classes_data(request):
    access['title']="Classes Details"
    if request.user.profile.user_type==1:
        classes=Class.objects.all()
    else:
        classes=Class.objects.filter(professor=request.user.profile).all()

    access['classes']=classes
    return render(request,'class.html',access)

def student_data(request):
    access['title']="Student Details"
    students=student.objects.all()
    access['students']=students
    return render(request,'student.html',access)


def attendance_data(request):
    access['title']="Attendance Details"
    if request.user.profile.user_type == 1:
        classes=Class.objects.all()
    else:
        classes=Class.objects.filter(professor=request.user.profile).all()

    access['classes']=classes
    return render(request,'attendance.html',access)








#update profile
@login_required
def profile_update(request):
    access['title']="profile update"
    user_data=User.objects.get(id=request.user.id)
    profile_data=UserProfile.objects.get(user_data=user_data)
    access['user_data']=user_data
    access['profile_data']=profile_data
    if request.method == 'POST':
        data=request.method.POST
        form=update_profile(data,instance=user_data)
        if form.is_valid():
            form.save()
            form2=update_user_details(data,instance=profile_data)
            if form2.is_valid():
                form2.save()
                messages.success(request,"Your profile has been updated successfully")
                return redirect('profile')
            else:
                access['form2']=form2
        else:
            access['form']=form
            form=update_profile(instance=request.user)
    return render(request,'profile_update.html',access)




def password_update(request):
    access['title']="password update"
    if request.method == 'POST':
        data=update_password(user=request.user,data=request.POST)
        if data.is_valid():
            data.save()
            messages.success(request,"account is password updated successfully")
            update_session_auth_hash(request,form.user)
            return redirect('profile')
        else:
            access['data']=data
    else:
        data=update_password(request.POST)
        access['data']=data
    return render(request,'newpassword.html',access)

def profile_updatemeta(request):
    access['title']='Profile update'
    user=User.objects.get(id=request.user.id)
    profile_data=UserProfile.objects.get(user=user)
    access['user']=user
    access['profile_data']=profile_data
    if request.method =='POST':
        data=request.POST

        form=update_profile(data,instance=user)
        if form.is_valid():
            form.save()
            form2=update_user_details(data,instance=profile)
            if form2.is_valid():
                form2.save()
                messges.success(request,'Data is updated successfully')
                return redirect('profile')
            else:
                access['form']=form
        else:
            access['form2']=form2
            form=update_profile(instance=request.user)
    return render(request,'editprofile.html',access)


def update_image(request):
    access['title']="Profile Image Update"
    user=User.objects.get(id=request.user.id)
    #profile_data=UserProfile.objects.get(user=user)
    access['user_data']=user
    access['profile_data']=user.profile
    if user.profile.profile_image:
        img=MEDIA_URL+"photos/photos-Rajiv_Gandhi_University_of_Knowledge_Technologies.png"

    access['img']=img
    form=profile_image(request.POST,request.FILES,instance=user)
    if form.is_valid():
        form.save()
        access['status']='success'
        messages.success(request,'Your profile image is updated successfully')
    else:
        access['form']=form
    form=profile_image(request.POST,instance=user)
    return HttpResponse("return to profile page with updated profile page")


def department_view(request,pk=None):
    if pk == None:
        dept={}
    elif pk >0:
        dept=Branch.objects.filter(id=pk).first()
    else:
        dept={}
    access['dept']=dept
    return HttpResponse("Branch view with specified users")

def user_view(request,pk=None):
    access['title']="users Data"
    if pk == None:
        user1={}
    elif pk > 0:
        user1=UserProfile.objects.filter(id=pk).first()
    else:
        user1={}
    access['user1']=user1
    return HttpResponse("user's data view")

def class_view(request,pk=None):
    access['title']='Class View'
    user1=UserProfile.objects.filter(user_type=2).first()
    if pk == None:
        _class={}
    elif pk > 0:
        _class=Class.objects.filter(id=pk).first()
    else:
        _class={}
    return HttpResponse("Class data views")

def student_view(request,pk=None):
    access['title']="student view"
    if pk == None:
        stu={}
    elif pk > 0:
        stu=student.objects.filter(id=pk).first()
    else:
        stu={}
    access['students']=stu
    return HttpResponse("Students data view")



#Save models details

def save_branches(request):
    if request.method == 'POST':
        branch=None
        if request.POST['id'] == '':
            print("Field values showing erros")
        else:
            dept=Branch.objects.filter(id=request.POST['id']).first()
        if dept == None:
            form=save_branch(request.POST,instance=dept)
        else:
            form=save_branch(request.POST)

    if form.is_valid():
        form.save()
        access['form']=form
        access['status']="success"
        messages.success(request,"Your data is stored successfully")

    return HttpResponse("Branch Details views")


def save_user(request):
    access['title']="User Details"
    if request.method == 'POST':
        data=request.POST
        if data['id'] != '':
            user=User.objects.get(id=data['id'])
        else:
            user=None
        if not user == None:
            form=update_professor(data=data,user=user,instance=user)
        else:
            form=user_registration(data)
        if form.is_valid():
            form.save()

            if user == None:
                user=User.objects.all.last()
            try:
                profile=UserProfile.objects.get(user=user)
            except:
                profile=None
            if profile == None:
                form2=update_professor(request.POST,request.FILES)
            else:
                form2=update_professor(request.POST,request.FILES,instance=user)

            if form.is_valid():
                form.save()
                access['status']="success"
                messages.success(request,"Your profile data is stored successfully")

            else:
                User.objects.filter(id=user.id).delete()
                access['form']=form
    return HttpResponse("saving the users details")


# save students data
def student_save_class(request):
    access['title']="Saving the students data"

    if request.method =='POST':
        studata=None

        if not request.POST['id']=='':
            studentdata=student.objects.filter(id=request.POST['id']).first()

        if not studata == None:
            form=save_student(request.POST,request.FILES,instance=user)
        else:
            form=save_student(request.POST)
        if form.is_valid():
            form.save()
            access['status']="success"
            access['form']=form
            messages.success(request,"Student data is added successfully")
    return HttpResponse("Student data is added")



#Attendance data
def attendance_data(request,class_id=None,date=None):
    access['title']="Attendance Data"
    _class=Class.objects.get(id=class_id)
    students=Student.objects.filter(id__in=class_student.objects.filter(class_details=_class).values_list('student')).all()
    access['class1']=_class
    access['students']=students

    data_attendance={}
    for class_stu in students:
        data_attendance[class_stu.id]={}
        data_attendance[class_stu.id]['data']=student
    if not date is None:
        date=datetime.strptime(date,'%y-%m-%d')
        year=date.strftime('%y')
        month=date.strftime('%m')
        day=date.strftime('%d')
        attendance=Attendance.objects.filter(year=year,month=month,day=day,class_details=_class).all()
        for atte in attendance:
            data_attendance[atte.student.PK]['type']=atte.type

    access['data_attendance']=data_attendance
    access['student']=student

    return HttpResponse("Attendance details for Class Studets")




#save class data

def data_class(request):
    access['status']="Class Data"

    if request.method == 'POST':
        _class =None

        if not request.POST['id']=='':
            classes_data=Class.objects.filter(id=request.POST['id']).first()

        if not _class == None:
            form=save_class(request.POST,instanc=user)
        else:
            form=save_class(request.POST)
    if form.is_valid():
        form.save()
        access['status']="success"
        messages.success(request,"Your class data is stored successfully")
    else:
        class_data1=Class.objects.filter(id=user.id).delete()
    return HttpResponse("Class data")


#save class student
def save_class_student(request):
    if request.method =='POST':
        form=class_student_data(request.POST)
        if form.is_valid():
            form.save()
    messages.success("Student data is added successfully in your class")
    return HttpResponse("Student data added into the class")






#Data  Deleting from database
def delete_user(request):
    access['title']="Deleting the User Profile"
    if request.method == 'POST':
        id=request.POST['id']
    try:
        dept=Branch.objects.filter(id=id).first()
        dept.delete()
    except Exception as e:
        print(e)

    access['status']="success"
    messages.success(request,"your profile data is delete successfully")
    return redirect('login')
    return HttpResponse("Deleting the data")

#delete the class

def delete_class(request):
    access['title']="Deleting the class"
    if request.method == 'POST':
        id=request.POST['id']
    try:
        cls=Class.objects.filter(id=id).first()
        cls.delete()
    except Exception as e:
        print(e)
    access['status']="success"
    messages.success(request,"Class data is deleted successfully")

    return HttpResponse("Class data is deleted")

def delete_professor(request):
    access['title']="Deleting the teachers data"
    if request.method == 'POST':
        id=request.POST['id']
    try:
        teac=User.objects.filter(id=id).first()
        teac.delete()
    except Exception as e:
        print(e)
    access['status']="success"
    messages.success(request,"professor data is deleted successfully")
    return HttpResponse("Faculty data is deleted")

#student deleting
def delete_student(request):
    access['title']="Deleting the students data"
    if request.method == 'POST':
        id=request.POST['id']
    try:
        stu=student.objects.filter(id=id).first()
        stu.delete()
    except Exception as E:
        print(e)
    access['status']="success"
    messages.success(request,"student data is deleted")

#class student data

def delete_class_student(request):
    access['title']=" class students"
    if request.method == 'POST':
        id=request.POST['id']
    try:
        classda=class_student.objects.filter(id=id).first()
        classda.delete()
    except Exception as e:
        print(e)
    access['status']='success'
    messages.success(request,"Your class data is deleted successfully")

    return HttpResponse("Class students data deleted")




#Attendance 2
def attendance_data2(request):
    if request.method == 'POST':
        id=request.POST['id']
        _class=Class.objects.get(id=id)
        cls_attendance=attendance2.objects.filter(id__in=class_student.objects.filter(class_details=_class)).values_list().all()
        access['class_stu']=_class
        access['cls_attendance1']=cls_attendance

        if not request.POST =='':
            with open("") as f, open("") as g:
                    flines=f.readline()
                    glines=g.readline()
                    d=difflib.Differ()
                    diff=d.compare(flines,glines)
                    print('\n'.join(diff))
                    att=[]
                    att1=[]
                    for i in diff:
                        att.append(i)

                    if att not in diff:
                        att1.append(diff)


        with open('file.txt','w+') as a, open('file1.txt','w+') as b:
            data1=pickle.dump(att,file)
            data2=pickle.dump(att1,file1)

        access['data1']=data1
        access['data2']=data2
    return HttpResponse("Attendance data in file formats")


@login_required
def save_attendance(request):
    access['title']="Save Attendance"

    if request.method =="POST":
        data=request.POST
        date=datetime.strptime(post['date_attendance'],'%y-%m-%d')
        day=date.strftime('%d')
        year=date.strftime('%y')
        month=date.strftime('%m')
        _class=Class.objects.get(id=post['class_details'])
        Attendance.objects.filter(date=date,year=year,month=month,day=day)
        for student in data.getlist('student[]'):
            student_type=data[student]
            student_data=Student.objects.get(id=student)
            att_data=Attendance(student=student_data,student_type=student_type,class_details=class_details,data_attendance=post['data_attedance']).save()
        access['status']='success'
        messages.success(request,'Saving the attendance data')
    return HttpResponse("Saving attendance data")
