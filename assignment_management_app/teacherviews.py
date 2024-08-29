from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,logout,login,update_session_auth_hash
from .models import User,Teacher,Student,Course,Assignment,Subject,AssignmentSubmissionDetails,News,StudyMaterial
from .forms import StudyMaterialForm
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone


def is_teacher(user):
    return user.is_authenticated and user.usertype == 'teacher'


def teacherlogin(request):
    if request.method=="POST":
        USERNAME=request.POST["username"]
        PASSWORD=request.POST["password"]
        user=authenticate(request,username=USERNAME,password=PASSWORD)
            
        if user and user.is_staff==1:
            login(request,user)
            request.session["teacher_id"]=user.id
            return redirect("/teacher_dashboard")
        else:
            return HttpResponse('<script>alert("Incorrect Login Credentials"); window.history.back();</script>')

    else:
        return render(request,"teacher/teacher_login.html")


@user_passes_test(is_teacher)
def teacherdashboard(request):
    id=request.session["teacher_id"]
    teacher=User.objects.get(id=id)
    teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
    teacher_course=teacher.course
    student_count = User.objects.filter(usertype='student', course=teacher_course,is_active=1).prefetch_related('student_set').count
    assignment_count=Assignment.objects.filter(course=teacher_course,emp=id).count
    news_count=News.objects.filter(user=id).count
    return render(request,"teacher/teacher_dashboard.html",{"teacher_name":teacher_name,"student_count":student_count,"assignment_count":assignment_count,"news_count":news_count})


@user_passes_test(is_teacher)
def teacherAssignment(request):
    if request.method == "POST":
        course=request.POST["course"]
        subject=request.POST["subject"]
        assignment_title=request.POST["assignment_title"]
        assignment_description=request.POST["assignment_description"]
        last_date_of_submission=request.POST["last_date_of_submission"]
        assignment_marks=request.POST["assignment_marks"]
        assignment_file=request.FILES["assignment_file"]
        teacher_id = request.session["teacher_id"]
        
        assignment = Assignment.objects.create(
            course_id=course,
            subject_id=subject,
            assignment_title=assignment_title,
            assignment_description=assignment_description,
            last_date_of_submission=last_date_of_submission,
            assignment_marks=assignment_marks,
            assignment_file=assignment_file,
            emp_id=teacher_id 
        )
        assignment.save()
        return HttpResponse('<script>alert("New Assignment Added");window.history.back();</script>')
    else:
        id = request.session["teacher_id"]
        teacher = User.objects.get(id=id)
        teacher_course=teacher.course_id
        teacher_name = teacher.first_name.capitalize() + " " + teacher.last_name.capitalize()
        course = Course.objects.get(id=teacher_course)
        subjects = Subject.objects.filter(course=course.id)
        assignments=Assignment.objects.filter(emp=id)
        
        return render(request, "teacher/teacher_assignment.html", {
            "teacher_name": teacher_name,
            "course": course,
            "subjects": subjects,
            "assignments":assignments
        })


@user_passes_test(is_teacher)
def teacherEditAssignment(request,id):
    if request.method == "POST":
        course=request.POST["course"]
        subject=request.POST["subject"]
        assignment_title=request.POST["assignment_title"]
        assignment_description=request.POST["assignment_description"]
        last_date_of_submission=request.POST["last_date_of_submission"]
        assignment_marks=request.POST["assignment_marks"]
        assignment_file=request.FILES.get("assignment_file",None)

        assignment=Assignment.objects.get(assignment_no=id)

        assignment.subject_id=subject
        assignment.assignment_title=assignment_title
        assignment.assignment_description=assignment_description
        assignment.last_date_of_submission=last_date_of_submission
        assignment.assignment_marks=assignment_marks
        if assignment_file:
            assignment.assignment_file=assignment_file
        assignment.save()
        return HttpResponse('<script>alert("Assignment Details Updated"); window.history.back();</script>')

    else:
        assignment=Assignment.objects.get(assignment_no=id)
        id = request.session["teacher_id"]
        teacher = User.objects.get(id=id)
        teacher_course=teacher.course_id
        teacher_name = teacher.first_name.capitalize() + " " + teacher.last_name.capitalize()
        course = Course.objects.get(id=teacher_course)
        subjects = Subject.objects.filter(course=course.id)
        
        return render(request, "teacher/teacher_edit_assignment.html", {
            "teacher_name": teacher_name,
            "subjects": subjects,
            "assignment":assignment
        })


@user_passes_test(is_teacher)
def teacherUncheckedAssignment(request):
    if request.method=="POST":
        subject=request.POST["subject"]
        assignments=Assignment.objects.filter(subject=subject).prefetch_related("assignmentsubmissiondetails_set")
        teacherid=request.session["teacher_id"]
        teacher=User.objects.get(id=teacherid)
        teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
        teacher_course=teacher.course_id
        subjects=Subject.objects.filter(course=teacher_course)
        subject_name=Subject.objects.get(id=subject).subject
        return render(request,"teacher/teacher_unchecked_assignment.html",{"subjects":subjects,"assignments":assignments,"subject_name":subject_name,"submitted":"submitted","teacher_name":teacher_name})
    
    else:
        teacherid=request.session["teacher_id"]
        teacher=User.objects.get(id=teacherid)
        teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
        teacher_course=teacher.course_id
        subjects=Subject.objects.filter(course=teacher_course)
        return render(request,"teacher/teacher_unchecked_assignment.html",{"subjects":subjects,"teacher_name":teacher_name})


@user_passes_test(is_teacher)
def teacherCheckedAssignment(request):
    if request.method=="POST":
        subject=request.POST["subject"]
        assignments=Assignment.objects.filter(subject=subject).prefetch_related("assignmentsubmissiondetails_set")
        teacherid=request.session["teacher_id"]
        teacher=User.objects.get(id=teacherid)
        teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
        teacher_course=teacher.course_id
        subjects=Subject.objects.filter(course=teacher_course)
        subject_name=Subject.objects.get(id=subject).subject
        return render(request,"teacher/teacher_checked_assignment.html",{"subjects":subjects,"assignments":assignments,"subject_name":subject_name,"submitted":"submitted","teacher_name":teacher_name})
   
    else:
        teacherid=request.session["teacher_id"]
        teacher=User.objects.get(id=teacherid)
        teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
        teacher_course=teacher.course_id
        subjects=Subject.objects.filter(course=teacher_course)
        return render(request,"teacher/teacher_checked_assignment.html",{"subjects":subjects,"teacher_name":teacher_name})
    


@user_passes_test(is_teacher)
def viewUncheckedAssignment(request,assignment_no,student_id):
    if request.method=="POST":
        remarks=request.POST["remarks"]
        marks=request.POST["marks"]
        assignment_details=AssignmentSubmissionDetails.objects.get(assignment=assignment_no,student_id=student_id)
        assignment_details.remarks=remarks
        assignment_details.marks_obtained=marks
        assignment_details.save()
        return redirect("teacher_unchecked_assignment")

    else:
        teacherid=request.session["teacher_id"]
        teacher=User.objects.get(id=teacherid)
        teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
        assignment_details=AssignmentSubmissionDetails.objects.get(assignment=assignment_no,student_id=student_id)
        student=assignment_details.student_id
        student_roll_no=Student.objects.get(student_id=student).roll_no
        return render(request,"teacher/teacher_view_unchecked_assignment.html",{"assignment_details":assignment_details,"teacher_name":teacher_name,"student_roll_no":student_roll_no})
       

@user_passes_test(is_teacher)
def viewCheckedAssignment(request,assignment_no,student_id):
    teacherid=request.session["teacher_id"]
    teacher=User.objects.get(id=teacherid)
    teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
    assignment_details=AssignmentSubmissionDetails.objects.get(assignment=assignment_no,student_id=student_id)
    student=assignment_details.student_id
    student_roll_no=Student.objects.get(student_id=student).roll_no
    return render(request,"teacher/teacher_view_checked_assignment.html",{"assignment_details":assignment_details,"teacher_name":teacher_name,"student_roll_no":student_roll_no})



@user_passes_test(is_teacher)
def studyMaterial(request):
    teacherid=request.session["teacher_id"]
    teacher=User.objects.get(id=teacherid)
    teacher_course=teacher.course_id
    if request.method == "POST":
        form = StudyMaterialForm(request.POST, request.FILES, teacher_course=teacher_course)
        if form.is_valid():
            study_material = form.save(commit=False)
            study_material.emp_id = teacherid  
            study_material.save()
            return redirect('study_material')
    else:
        teacherid=request.session["teacher_id"]
        teacher=User.objects.get(id=teacherid)
        teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
        studymaterials=StudyMaterial.objects.filter(emp_id=teacherid).order_by("subject__subject")
        teacher_course=teacher.course_id
        form = StudyMaterialForm(teacher_course=teacher_course)
        return render(request,"teacher/teacher_study_materials.html",{"teacher_name":teacher_name,"study_materials":studymaterials,"form":form})



@user_passes_test(is_teacher)
def editStudyMaterial(request,id):
    teacherid=request.session["teacher_id"]
    teacher=User.objects.get(id=teacherid)
    teacher_course=teacher.course_id
    studymaterial=StudyMaterial.objects.get(id=id)
    if request.method == "POST":
        form = StudyMaterialForm(request.POST, request.FILES, teacher_course=teacher.course_id, instance=studymaterial)
        if form.is_valid():
            form.save()  # Save the updated study material
            return redirect('study_material')
    else:
        teacherid=request.session["teacher_id"]
        teacher=User.objects.get(id=teacherid)
        teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
        
        teacher_course=teacher.course_id
        form = StudyMaterialForm(teacher_course=teacher_course,instance=studymaterial)
        subjects = Subject.objects.filter(course=teacher.course_id).order_by('subject')
        formatted_subjects = [(subject.id, subject.subject.capitalize() + ' [' + subject.subject_code.upper() + ']') for subject in subjects]
        form.fields['subject'].choices = formatted_subjects
        file_name=StudyMaterial.objects.get(id=id).file.name.split("/")[-1]
        return render(request,"teacher/teacher_edit_study_material.html",{"teacher_name":teacher_name,"study_material":studymaterial,"form":form,"file_name":file_name})
    


@user_passes_test(is_teacher)
def deleteStudyMaterial(request,id):
    
    studymaterial=StudyMaterial.objects.get(id=id)
    studymaterial.delete()
    return redirect('study_material')


@user_passes_test(is_teacher)
def teacherNews(request):
    if request.method=="POST":
        news_title=request.POST["title"]
        news_description=request.POST["description"]
        teacherid=request.session["teacher_id"]
        news=News.objects.create(user_id=teacherid,title=news_title,description=news_description)
        news.save()
        return HttpResponse('<script>alert("News Added");window.history.back();</script>')
    else:
        teacherid=request.session["teacher_id"]
        teacher=User.objects.get(id=teacherid)
        teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
        news=News.objects.filter(user_id=teacherid)
        for item in news:
            item.created_date = timezone.localtime(item.created_date)
        return render(request,"teacher/teacher_news.html",{"teacher_name":teacher_name,"news":news})

@user_passes_test(is_teacher)
def teacherDeleteNews(request,id):
    news=News.objects.get(id=id)
    news.delete()
    return HttpResponse('<script>alert("News Deleted");window.history.back();</script>')



@user_passes_test(is_teacher)
def teacherEditNews(request,id):
    if request.method=="POST":
        news_title=request.POST["title"]
        news_description=request.POST["description"]
        news=News.objects.get(id=id)
        news.title=news_title
        news.description=news_description
        news.save()
        return HttpResponse('<script>alert("News Updated");window.history.back();</script>')
    else:
        teacherid=request.session["teacher_id"]
        teacher=User.objects.get(id=teacherid)
        teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
        news=News.objects.get(id=id)
        print(news)
        return render(request,"teacher/teacher_edit_news.html",{"teacher_name":teacher_name,"news":news})



@user_passes_test(is_teacher)
def courseWiseStudent(request):
    id=request.session["teacher_id"]
    teacher=User.objects.get(id=id)
    teacher_name=teacher.first_name.capitalize()+ " "+teacher.last_name.capitalize()
    teacher_course=teacher.course
    students = User.objects.filter(usertype='student', course=teacher_course,is_active=1).prefetch_related('student_set')
    print(students)
    return render(request,"teacher/course_wise_student.html",{"students":students,"teacher_name":teacher_name})


    
@user_passes_test(is_teacher)
def teacherProfile(request):
    if request.method=="POST":

        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        mobile_number=request.POST["mobile_number"]
        gender=request.POST["gender"]
        dob=request.POST["date_of_birth"]
        address=request.POST["address"]
        id=request.session["teacher_id"]

        u=User.objects.get(id=id)
        u.first_name=first_name
        u.last_name=last_name
        t=Teacher.objects.get(emp=id)

        t.mobile_number=mobile_number
        t.gender=gender
        t.date_of_birth=dob
        t.address=address
        u.save()
        t.save()
        
        return HttpResponse('<script>alert("Profile Updated"); window.history.back();</script>')

    else:
        id=request.session["teacher_id"]
        teacher=Teacher.objects.get(emp=id)
        teacher_name=teacher.emp.first_name.capitalize()+" "+teacher.emp.last_name.capitalize()
        return render(request,"teacher/teacher_profile.html",{"edit":teacher,"teacher_name":teacher_name})



@user_passes_test(is_teacher)
def teacherChangePassword(request):
    if request.method=="POST":
        current_password=request.POST["old_password"]
        print(current_password)
        new_password=request.POST["password"]
        confirm_password=request.POST["confirm_password"]
        if new_password==confirm_password:
            username = request.user.username
            print(username)
            user = authenticate(username=username, password=current_password)
            print(user)
            if user is not None:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return HttpResponse('<script>alert("Passowrd is Successfully updated");window.history.back();</script>')
            
            else:
                return HttpResponse('<script>alert("Current password is incorrect."); window.history.back();</script>')
    
    else:
        id=request.session["teacher_id"]
        teacher=User.objects.get(id=id)
        teacher_name=teacher.first_name.capitalize()+" "+teacher.last_name.capitalize()
        return render(request,"teacher/teacher_change_password.html",{"teacher_name":teacher_name})


def logouts(request):
    logout(request)
    return redirect("/")