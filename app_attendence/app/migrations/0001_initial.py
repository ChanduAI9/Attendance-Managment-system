# Generated by Django 3.2.13 on 2022-06-09 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(blank=True, max_length=250, null=True)),
                ('batch_year', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.IntegerField(default=1)),
                ('hod_name', models.CharField(blank=True, max_length=250, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.CharField(blank=True, max_length=250, null=True)),
                ('class_name', models.CharField(blank=True, max_length=250, null=True)),
                ('batch', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(blank=True, max_length=250, null=True)),
                ('first_name', models.CharField(blank=True, max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('contact', models.CharField(blank=True, max_length=250, null=True)),
                ('batch', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profiles/')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=250, null=True)),
                ('user_type', models.IntegerField(default=2)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('contact', models.CharField(blank=True, max_length=250, null=True)),
                ('branch_name', models.CharField(blank=True, max_length=250, null=True)),
                ('campus', models.CharField(blank=True, choices=[('Nuzvid', 'Nuzvid'), ('RK valley', 'RK valley'), ('Ongole', 'Ongole'), ('Srikakulam', 'Srikakulam')], max_length=250, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='class_student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.class')),
                ('students', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userprofile'),
        ),
        migrations.CreateModel(
            name='attendance2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_attendance', models.FileField(upload_to='')),
                ('class_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.class')),
            ],
        ),
        migrations.CreateModel(
            name='attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateField()),
                ('type', models.CharField(choices=[('1', 'present'), ('2', 'absent')], max_length=250)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('class_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.class')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student')),
            ],
        ),
    ]