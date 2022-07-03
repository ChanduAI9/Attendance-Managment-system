from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from statistics import mode
from django.contrib.auth.models import  User
from django.dispatch import receiver
# Create your models here.

class Branch(models.Model):
    branch_name=models.CharField(max_length=250,blank=True,null=True)
    batch_year=models.CharField(max_length=250,blank=True,null=True)
    status=models.IntegerField(default=1)
    hod_name=models.CharField(max_length=250,blank=True,null=True)
    date_added=models.DateTimeField(default=timezone.now)
    date_updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.branch_name

class student(models.Model):
    student_id=models.CharField(max_length=250,blank=True,null=True)
    first_name=models.CharField(max_length=250,blank=True,null=True)
    last_name=models.CharField(max_length=250,blank=True,null=True)
    gender=models.CharField(max_length=100,choices=[('Male','Male'),('Female','Female')],blank=True,null=True)
    date_of_birth=models.DateField(blank=True,null=True)
    contact=models.CharField(max_length=250,blank=True,null=True)
    batch=models.CharField(max_length=250,blank=True,null=True)

    def __str__(self):
        return self.student_id+"-"+self.first_name+"-"+self.batch



# Create users models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_image=models.ImageField(blank=True,null=True,upload_to='profiles/')
    gender=models.CharField(max_length=250,choices=[('Male','Male'),('Female','Female')],blank=True,null=True)
    user_type=models.IntegerField(default=2)
    date_of_birth=models.DateField(blank=True,null=True)
    contact=models.CharField(max_length=250,blank=True,null=True)
    branch_name=models.CharField(max_length=250,blank=True,null=True)
    campus=models.CharField(max_length=250,choices=[('Nuzvid','Nuzvid'),('RK valley','RK valley'),('Ongole','Ongole'),('Srikakulam','Srikakulam')],blank=True,null=True)


    def __str__(self):
        return self.user.username

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    print(instance)
    try:
        profile=UserProfile.objects.get(user=instance)
    except Exception as e:
        UserProfile.objects.create(user=instance)
    instance.profile.save()



class Class(models.Model):
    professor=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    class_id=models.CharField(max_length=250,blank=True,null=True)
    class_name=models.CharField(max_length=250,blank=True,null=True)
    batch=models.CharField(max_length=250,blank=True,null=True)

    def __str__(self):
        return self.batch+"-"+self.class_name

class class_student(models.Model):
    class_details=models.ForeignKey(Class,on_delete=models.CASCADE)
    students=models.ForeignKey(student,on_delete=models.CASCADE)

    def __str__(self):
        return self.students.student_id

def present(self):
    students=self.students
    _class=self.class_details
    try:
        pre=attendance.objects.filter(class_details=_class,students=students,type=1).count()
        return pre
    except:
        return 0

def absent(self):
    students=self.students
    _class=self.class_details
    try:
        pre=attendance.objects.filter(class_details=_class,students=students,type=2).count()
        return pre
    except:
        return 0


class Attendance(models.Model):
    class_details=models.ForeignKey(Class,on_delete=models.CASCADE)
    student=models.ForeignKey(student,on_delete=models.CASCADE)
    attendance_date=models.DateField()
    type=models.CharField(max_length=250, choices=[('1','present'),('2','absent')])
    date_updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_details.class_name +"- "+self.student.student_id

# attendance  two
class attendance2(models.Model):
    student_attendance=models.FileField()
    class_details=models.ForeignKey(Class,on_delete=models.CASCADE)

    def __str__(self):
        return self.student_attendance
