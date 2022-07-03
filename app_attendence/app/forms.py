from django import forms
from django.contrib.auth.models import User
from re import T
from unicodedata import category
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm
from .models import Branch,student,Class,class_student,Attendance,UserProfile,attendance2
#create your forms actions here
class save_branch(forms.ModelForm):
    branch_name=forms.CharField(max_length=250,help_text="this field is required")
    status=forms.IntegerField()

    class Meta:
        model=Branch
        fields=('branch_name','status')

    def check_branch(self):
        id=self.instance.id if not self.instance == None else 0
        try:
            if id.isnumeric() and id>0:
                branch=Branch.objects.exclude(id=id).get(branch_name=self.cleaned_data['branch_name'])
            else:
                branch=Branch.objects.get(branch_name=self.cleaned_data['branch_name'])
        except:
            return self.cleaned_data['branch_name']
        raise forms.ValidationError('Branch already exists')


#save class details
class save_class(forms.ModelForm):
    professor=forms.CharField(max_length=250)
    student_id=forms.CharField(max_length=250)
    class_name=forms.CharField(max_length=250)
    batch=forms.CharField(max_length=250)


    class Meta:
        model=Class
        fields=('professor','student_id','class_name','batch')

        def class_teacher(self):
            professor=self.cleaned_data['professor']
            try:
                faculty=user_profile.objects.get(id=professor)
                return faculty
            except:
                raise forms.ValidationError("Teacher is  invalid ")

class save_student(forms.ModelForm):
    batch=forms.CharField(max_length=250)

    class Meta:
        model=student
        fields=('student_id','first_name','last_name','gender','date_of_birth','contact','batch')

    def check_student(self):
        student_id=self.cleaned_data['student_id']
        try:
            if not self.instance.id is None:
                students=student.objects.exclude(id=self.instance.id).get(student_id=student_id)
            else:
                students=student.objects.get(student_id=student_id)
        except:
            return student_id
        raise forms.ValidationError('Student id is already exists')


class class_student_data(forms.ModelForm):
    class_details=forms.IntegerField()
    students=forms.IntegerField()

    class Meta:
        model=class_student
        fields=('class_details','students')

    def check_class_details(self):
        class_id=self.cleaned_data['class_details']
        try:
            class_details=Class.objects.get(id=class_id)
            return class_details
        except:
            raise forms.ValidationError("Class id is invalid")

    def check_student(self):
        student_id=self.cleaned_data['student_id']
        _class=Class.objects.get(id=self.data.get('class_details'))
        students=student.objects.get(id=student_id)
        try:
            stu=class_student.objects.get(class_details=_class,students=students)
            if len(stu)>0:
                raise forms.ValidationError("student already exists in the class list")
        except:
            return students


#create your forms actions here

class user_registration(UserCreationForm):
    first_name=forms.CharField()
    last_name=forms.CharField()
    contact=forms.CharField()

    class Meta:
        model=User
        fields=('email','first_name','last_name','password1','password2','username','contact')


    def  check_email(self):
        email_id=self.cleaned_data['email_id']
        try:
            user=User.objects.get(email_id=email_id)
        except  Exception as e:
            return email_id
        raise forms.ValidationError("This email id is already exists")

    def check_username(self):
        username=self.cleaned_data['username']
        try:
            user=User.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError("This username is already exists")

#if the teacher changed class and anything related updating
class update_professor(UserChangeForm):
    username=forms.CharField(max_length=250,help_text="This field is required")
    email_id=forms.EmailField(max_length=250,help_text="This field is required")
    first_name=forms.CharField(max_length=250,help_text="this field is required")
    last_name=forms.CharField(max_length=250,help_text="This field is required")
    contact=forms.CharField(max_length=250,help_text="This field is required")


    class Meta:
        model=User
        fields=('email_id','username','first_name','last_name')


    #updating users details
    def __init__(self):
        self.user=user
        super(update_professor,self).__init__(*args,**kwargs)

    def check_email(self):
        email_id=self.cleaned_data['email_id']
        try:
            user=User.objects.exclude(id=self.user.id).get(email_id=email_id)
        except Exception as e:
            return email_id
        raise forms.ValidationError("The email id is already exists")

    def check_username(self):
        username=self.cleaned_data['username']
        try:
            user.User.objects.exclude(id=self.user.id).get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError("The username is already exists")

#adding profile photo
class profile_image(forms.ModelForm):
    profile_photo=forms.ImageField(help_text="this field is required")

    class Meta:
        model=UserProfile
        fields=('profile_image',)



#cr'{action required}
#hod {action required}
#super admin {action required}




#updating user details

class update_user_details(forms.ModelForm):
    usernamme=forms.CharField(max_length=250,help_text="the username field is required")
    email_id=forms.EmailField(max_length=250,help_text="the email id is required")
    first_name=forms.CharField(max_length=250,help_text="This First name is required")
    last_name=forms.CharField(max_length=250,help_text="This last name is required")
    current_password=forms.CharField(max_length=250)
    date_of_birth=forms.DateField()
    contact=forms.CharField(max_length=250)
    branch_name=forms.CharField(max_length=250)

    class Meta:
        model=User
        fields=('email_id','username','first_name','last_name','date_of_birth','contact','branch_name')

    def check_current_password(self): #checking users password
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError('Password is incorrect')



    def  check_email(self):
        email_id=self.cleaned_data['email_id']# getting data
        try:
            user=User.objects.exclude(id=self.cleaned_data['id']).get(email_id=email_id)
        except  Exception as e:       #checking data
            return email_id
        raise forms.ValidationError("This email id is already exists")

    def check_username(self):
        username=self.cleaned_data['username']
        try:
            user=User.objects.exclude(id=self.cleaned_data['id']).get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError("This username is already exists")


class update_password(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}),label="Old password")
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-contro-sm rounded-0'}),label="New Password")
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}),label="confirm password")

    class Meta:
        model=User
        fields=('old_password','new_password1','new_password2')


class update_profile(forms.ModelForm):#updating profile photo
    profile_photo=forms.ImageField()
    current_password=forms.CharField(max_length=250)

    class Meta:
        model=UserProfile
        fields=('profile_image',)

    def __init__(self,*args,**kwargs):
        self.user=kwargs['instance']
        kwargs['instance']=self.user.profile
        super(update_profile,self).__init__(*args,**kwargs)

    def check_current_password(self):
        if not self.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError("password is incorrect")




#Attendance form action
class save_attendance(forms.ModelForm):
    student_att=forms.FileField()
    class_det=forms.CharField()

    class Meta:
        user=attendance2
        fields=("student_attendance","class_details")

    def students_data(self):
        student_att=self.cleaned_data['student_att']


        try:
            details=attendance2.objects.exclude(id=self.cleaned_data['student_att']).get(student_att)
        except Exception as e:
            raise forms.ValidationError("The file is not upload or something different error")

    def class_data(self):
        class_det=self.cleaned_data['class_det']

        try:
            details2=attendance2.objects.exclude(id=self.cleaned_data['class_det']).get(class_det=class_det)
        except Exception as e:
            raise forms.ValidationError("The class details is not included")
