from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class Course(models.Model):
    course = models.CharField(max_length=60)
    branch = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.course} [{self.branch}]"

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Reference to Course
    subject = models.CharField(max_length=60)
    subject_code = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.subject} ({self.subject_code})"

class User(AbstractUser):
    usertype = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

class Teacher(models.Model):
    
    emp = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to User
    mobile_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=60)
    date_of_birth = models.DateField()
    address = models.TextField()

class Student(models.Model):
    student= models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to User
    roll_no = models.IntegerField()
    mobile_number = models.CharField(max_length=15)


class Assignment(models.Model):
    assignment_no = models.AutoField(primary_key=True)
    emp = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to User
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # Reference to Subject
    assignment_title = models.CharField(max_length=100)
    assignment_description = models.TextField()
    posting_date=models.DateField(auto_now_add=True)
    last_date_of_submission = models.DateField()
    assignment_marks = models.IntegerField(default=-1)
    assignment_file = models.FileField(upload_to='media/assignments/')

class AssignmentSubmissionDetails(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to User
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)  # Reference to Assignment
    assignment_description = models.TextField()
    answer_paper = models.FileField(upload_to='media/submissions/')
    remarks = models.TextField()
    marks_obtained = models.IntegerField(default=-1)
    submitted_date = models.DateField(auto_now_add=True)



class News(models.Model):
    title=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)

class StudyMaterial(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True, null=True)
    file=models.FileField(upload_to="media/study_materials")
    upload_date=models.DateField(auto_now_add=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    emp=models.ForeignKey(User,on_delete=models.CASCADE)





