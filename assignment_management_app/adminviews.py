
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.db.models import Max
from django.contrib.auth import authenticate,logout,login,update_session_auth_hash
from .models import User,Student,Teacher,Course,Subject,AssignmentSubmissionDetails,Assignment,News
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_authenticated and user.is_superuser 

def adminlogin(request):
    if request.method=="POST":
        USERNAME=request.POST["username"]
        PASSWORD=request.POST["password"]
        print(USERNAME,PASSWORD)
        user=authenticate(request,username=USERNAME,password=PASSWORD)
        print(user)
        if user and user.is_superuser==1:
            login(request, user)
            return redirect(dashboard)
        else:
            return HttpResponse('<script>alert("Incorrect Login Credentials"); window.history.back();</script>')
    else:
        return render(request,"admin/admin_login.html")


@user_passes_test(is_admin)
def dashboard(request):
    course_count=Course.objects.all().count()
    subject_count=Subject.objects.all().count()
    student_count=Student.objects.all().count()
    teacher_count=Teacher.objects.all().count()
    return render(request,"admin/dashboard.html",{"course_count":course_count,"subject_count":subject_count,"teacher_count":teacher_count,"student_count":student_count})


@user_passes_test(is_admin)
def course(request):
    if request.method=="POST":
        course=request.POST["course"]
        branch=request.POST["branch"]
        print(course,branch)
        c=Course.objects.create(course=course,branch=branch)
        c.save()
        print(c)
        return HttpResponse('<script>alert("New Course Added"); window.history.back();</script>')
    else:
        course_data=Course.objects.all()
        return render(request,"admin/course.html",{"data":course_data})


@user_passes_test(is_admin)
def editCourse(request,id):
    if request.method=="POST":
        course=request.POST["course"]
        branch=request.POST["branch"]
        
        e=Course.objects.get(id=id)
        e.course=course
        e.branch=branch
        e.save()
        return HttpResponse('<script>alert("Course Details Updated"); window.history.back();</script>')
    else:
        edit=Course.objects.get(id=id)
        return render(request,"admin/edit_course.html",{"edit":edit})


@user_passes_test(is_admin)
def deleteCourse(request,id):
    x=Course.objects.get(id=id)
    x.delete()
    return HttpResponse('<script>alert("Course Deleted"); window.history.back();</script>')


@user_passes_test(is_admin)
def subject(request):
    if request.method=="POST":
        course=request.POST["course"]
        subject=request.POST["subject"]
        subject_code=request.POST["subject_code"]
        print(course,subject,subject_code)
        s=Subject.objects.create(course_id=course,subject=subject,subject_code=subject_code)
        s.save()
        print(s)
        return HttpResponse('<script>alert("New Subject Added"); window.history.back();</script>')
    else:
        courses=Course.objects.all()
        subjects=Subject.objects.all()
        return render(request,"admin/subject.html",{"subjects":subjects,"courses":courses})


@user_passes_test(is_admin)
def deleteSubject(request,id):
    s=Subject.objects.get(id=id)
    s.delete()
    return HttpResponse('<script>alert("Subject Deleted"); window.history.back();</script>')


@user_passes_test(is_admin)
def editSubject(request,id):
    if request.method=="POST":
        course=request.POST["course"]
        subject=request.POST["subject"]
        subject_code=request.POST["subject_code"]
        
        course_instance = get_object_or_404(Course, id=course)
        # print(course,subject,subject_code)
        s=Subject.objects.get(id=id)
        s.course=course_instance
        s.subject=subject
        s.subject_code=subject_code
        s.save()
        return HttpResponse('<script>alert("Subject Details Updated"); window.history.back();</script>')
    
    else:
        courses=Course.objects.all()
        subject=Subject.objects.get(id=id)
        return render(request,"admin/edit_subject.html",{"edit":subject,"courses":courses})


@user_passes_test(is_admin)
def teacher(request):
    if request.method=="POST":
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        mobile_number=request.POST["mobile_number"]
        username=request.POST["username"]
        password=request.POST["password"]
        gender=request.POST["gender"]
        dob=request.POST["dob"]
        course=request.POST["course"]
        address=request.POST["address"]

        user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,is_staff=1,is_active=1,usertype="teacher",course_id=course)
        
        teacher=Teacher.objects.create(emp=user,mobile_number=mobile_number,gender=gender,date_of_birth=dob,address=address)
        user.save()
        teacher.save()
        
        return HttpResponse('<script>alert("New Teacher Added"); window.history.back();</script>')
    else:
        courses=Course.objects.all().order_by("course")
        # teachers=Teacher.objects.all().order_by("emp__course__course","emp__first_name")
        result = Teacher.objects.aggregate(max_id=Max('id'))
        max_id = int(result['max_id'])+1 if result['max_id'] is not None else 1
        teachers_by_course=[]
        for course in courses:
            teachers=Teacher.objects.filter(emp__course=course.id).order_by("emp__first_name")
            if teachers.exists():
                for index,teacher in enumerate(teachers,start=1):
                    teacher.serial_no=index
                teachers_by_course.append({
                'course': course,
                'teachers': teachers
            })

        return render(request,"admin/teacher.html",{"max_id":max_id,"courses":courses,"teachers":teachers,"teachers_by_course":teachers_by_course})
    

@user_passes_test(is_admin)
def deleteTeacher(request,id):
    u=User.objects.get(id=id)
    u.delete()
    return HttpResponse('<script>alert("Teacher Deleted"); window.history.back();</script>')


@user_passes_test(is_admin)
def regStud(request):
    students=Student.objects.all().order_by("student__course__course","student__first_name")
    courses=Course.objects.all().order_by("course")

    courses = Course.objects.all().order_by("course")  # Assuming you have a Course model
    students_by_course = []
    
    for course in courses:
        students = Student.objects.filter(student__course_id=course.id).order_by('student__first_name')
        if students.exists():
        # Add serial numbers manually
            for index, student in enumerate(students, start=1):
                student.serial_no = index
            students_by_course.append({
                'course': course,
                'students': students
            })

    return render(request,"admin/reg_student.html",{"students_by_course":students_by_course,"courses":courses})


@user_passes_test(is_admin)
def approveStudent(request,id):
    x=User.objects.get(id=id)
    x.is_active=1
    x.save()
    return redirect("/reg_stud")


@user_passes_test(is_admin)
def deleteStudent(request,id):
    x=User.objects.get(id=id)
    x.delete()
    return redirect("/reg_stud")


@user_passes_test(is_admin)
def news(request):
    if request.method=="POST":
        news_title=request.POST["title"]
        news_description=request.POST["description"]
        news=News.objects.create(user_id=1,title=news_title,description=news_description)
        news.save()
        return HttpResponse('<script>alert("News Added"); window.history.back();</script>')
    
    else:
        news=News.objects.filter(user_id=1).order_by("-created_date")
        return render(request,"admin/news.html",{"news":news})
    


@user_passes_test(is_admin)
def deleteNews(request,id):
    news=News.objects.get(id=id)
    news.delete()
    return HttpResponse('<script>alert("News Deleted"); window.history.back();</script>')



@user_passes_test(is_admin)
def editNews(request,id):
    if request.method=="POST":
        news_title=request.POST["title"]
        news_description=request.POST["description"]
        news=News.objects.get(id=id)
        news.title=news_title
        news.description=news_description
        news.save()
        return HttpResponse('<script>alert("News Details Updated"); window.history.back();</script>')
    
    else:
        news=News.objects.get(id=id)
        return render(request,"admin/edit_news.html",{"news":news})



@user_passes_test(is_admin)
def uncheckedAssignment(request):
    if request.method=="POST":
        subject=request.POST["subject"]
        subjects=Subject.objects.all()
        subject_name=Subject.objects.get(id=subject).subject
        assignments=Assignment.objects.filter(subject_id=subject).prefetch_related("assignmentsubmissiondetails_set")
        return render(request,"admin/unchecked_assignment.html",{"subjects":subjects,"assignments":assignments,"subject_name":subject_name,"submitted":"submitted"})

    else:
        subjects=Subject.objects.all()
        return render(request,"admin/unchecked_assignment.html",{"subjects":subjects})


@user_passes_test(is_admin)
def checkedAssignment(request):
    if request.method=="POST":
        subject=request.POST["subject"]
        subjects=Subject.objects.all()
        subject_name=Subject.objects.get(id=subject).subject
        assignments=Assignment.objects.filter(subject_id=subject).prefetch_related("assignmentsubmissiondetails_set")
        return render(request,"admin/checked_assignment.html",{"subjects":subjects,"assignments":assignments,"subject_name":subject_name,"submitted":"submitted"})

    else:
        subjects=Subject.objects.all()
        return render(request,"admin/checked_assignment.html",{"subjects":subjects})
    

@user_passes_test(is_admin)
def admin_view_checked_assignment(request,assignment_no,student_id):
    assignment_details=AssignmentSubmissionDetails.objects.get(assignment=assignment_no,student_id=student_id)
    student=assignment_details.student_id
    student_roll_no=Student.objects.get(student_id=student).roll_no
    return render(request,"admin/admin_view_submitted_assignment.html",{"assignment_details":assignment_details,"student_roll_no":student_roll_no})
    

@user_passes_test(is_admin)
def admin_view_unchecked_assignment(request,assignment_no,student_id):
    assignment_details=AssignmentSubmissionDetails.objects.get(assignment=assignment_no,student_id=student_id)
    student=assignment_details.student_id
    student_roll_no=Student.objects.get(student_id=student).roll_no
    return render(request,"admin/admin_view_unchecked_assignment.html",{"assignment_details":assignment_details,"student_roll_no":student_roll_no})
    

@user_passes_test(is_admin)
def btw_date_assignment(request):
    if request.method == "POST":
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        assignments = AssignmentSubmissionDetails.objects.filter(submitted_date__range=[from_date, to_date])
        return render(request,"admin/btw_date_assignment.html", {"assignments":assignments,"from_date":from_date,"to_date":to_date,"submitted":"submitted"})
    else:

        return render(request, "admin/btw_date_assignment.html")


@user_passes_test(is_admin)
def search(request):
    if request.method=="POST":
        searchquery=request.POST["search_query"]
        query_words = searchquery.split()
        q_objects = Q()

        for word in query_words:
            q_objects |= Q(emp__first_name__icontains=word) | Q(emp__last_name__icontains=word)
        results = Assignment.objects.filter(
            q_objects |
            Q(assignment_no__icontains=searchquery) |
            Q(subject__subject__icontains=searchquery)
        )
        submission_details = AssignmentSubmissionDetails.objects.filter(
            assignment__in=results
        )
        return render(request,"admin/search.html",{"assignments":submission_details,"searchquery":searchquery,"submitted":"submitted"})
    else:

        return render(request,"admin/search.html")
    
    
@user_passes_test(is_admin)
def changePassword(request):
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
                return HttpResponse('<script>alert("Password is Successfully updated");window.history.back();</script>')
            else:
                return HttpResponse('<script>alert("Current password is incorrect."); window.history.back();</script>')

    else:
        x=User.objects.get(id=1)
        password=x.password
        return render(request,"admin/change_password.html",{"password":password})



def logouts(request):
    logout(request)
    return redirect("/")