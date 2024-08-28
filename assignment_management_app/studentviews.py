from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,logout,login,update_session_auth_hash
from .models import User,Student,Course,Assignment,AssignmentSubmissionDetails,News,Teacher,StudyMaterial,Subject


from django.contrib.auth.decorators import user_passes_test

def is_student(user):
    return user.is_authenticated and user.usertype == 'student'

def studentlogin(request):
    if request.method=="POST":
        USERNAME=request.POST["username"]
        PASSWORD=request.POST["password"]
        print(USERNAME,PASSWORD)
        user=authenticate(request,username=USERNAME,password=PASSWORD)   
        if user is not None and user.is_staff==0 and user.is_active==1:
            login(request,user)
            request.session["student_id"]=user.id 
            print(user.id)
            return redirect("/student_dashboard")
        else:
            return HttpResponse('<script>alert("Incorrect Login Credentials"); window.history.back();</script>')
    else:
        return render(request,"student/student_login.html")

@user_passes_test(is_student)
def studentdashboard(request):
    id=request.session["student_id"]
    student=User.objects.get(id=id)
    student_name=student.first_name.capitalize()+ " "+student.last_name.capitalize()
    student_course=student.course_id
    print(student_course)
    news=News.objects.all()
    print(news)
    return render(request,"student/student_dashboard.html",{"student_name":student_name,"student_course":student_course,"news":news})

def register(request):
    if request.method=="POST":
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        username=request.POST["username"]
        password=request.POST["password"]
        confirm_password=request.POST["confirm_password"]
        roll_no=request.POST["roll_no"]
        mobile_number=request.POST["mobile_number"]
        course=request.POST["course"]

        if confirm_password==password:
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,is_active=0,usertype="student",course_id=course)
            student=Student.objects.create(student=user,roll_no=roll_no,mobile_number=mobile_number)
            user.save()
            student.save()
            return HttpResponse('''
                <script>
                    alert("Account Successfully Created");
                    window.location.href = "/";
                </script>
            ''')
        
    else:
        courses=Course.objects.all()
        return render(request,"student/register.html",{"courses":courses})
    

@user_passes_test(is_student)
def newAssignment(request):
    id=request.session["student_id"]
    student=User.objects.get(id=id)
    student_name=student.first_name.capitalize()+ " "+student.last_name.capitalize()
    student_course=student.course_id
    assignments = Assignment.objects.filter(course_id=student_course).exclude(
    assignment_no__in=AssignmentSubmissionDetails.objects.filter(student=student.id).values('assignment'))
    return render(request,"student/new_assignment.html",{"student_name":student_name,"assignments":assignments,})


@user_passes_test(is_student)
def submitAssignment(request,id):
    if request.method=="POST":
        studentid=request.session["student_id"]
        assignment_answer_description=request.POST["assignment_description"]
        answer_paper=request.FILES["answer_paper"]
        assignment=AssignmentSubmissionDetails.objects.create(student_id=studentid,assignment_id=id,assignment_description=assignment_answer_description,answer_paper=answer_paper)
        assignment.save()
        return HttpResponse('<script>alert("Assignment Submitted"); window.history.back();</script>') 
    
    else:
        studentid=request.session["student_id"]
        student=User.objects.get(id=studentid)
        student_name=student.first_name.capitalize()+ " "+student.last_name.capitalize()
        assignment=Assignment.objects.get(assignment_no=id)
        return render(request,"student/submit_assignment.html",{"student_name":student_name,"assignment":assignment})


@user_passes_test(is_student)
def uploadAssignment(request):
    id=request.session["student_id"]
    student=User.objects.get(id=id)
    student_name=student.first_name.capitalize()+ " "+student.last_name.capitalize()
    assignment_details=AssignmentSubmissionDetails.objects.filter(student_id=id)
    return render(request,"student/upload_assignment.html",{"student_name":student_name,"assignment_details":assignment_details})


@user_passes_test(is_student)
def viewSubmittedAssignment(request,id):
    studentid=request.session["student_id"]
    student=User.objects.get(id=studentid)
    student_name=student.first_name.capitalize()+ " "+student.last_name.capitalize()
    assignment_details=AssignmentSubmissionDetails.objects.get(assignment_id=id,student_id=studentid)
    return render(request,"student/view_submitted_assignment.html",{"student_name":student_name,"assignment_details":assignment_details})



@user_passes_test(is_student)
def studentStudyMaterial(request):
    studentid=request.session["student_id"]
    student=User.objects.get(id=studentid)
    student_name=student.first_name.capitalize()+ " "+student.last_name.capitalize()
    student_course=student.course_id
    studymaterials=StudyMaterial.objects.filter(subject__course=student_course).order_by("subject__subject")
    subjects=Subject.objects.filter(course_id=student_course)
    print(subjects)
    return render(request,"student/student_study_material.html",{"student_name":student_name,"study_materials":studymaterials,"subjects":subjects})


def studentViewStudyMaterial(request,id):
    studentid=request.session["student_id"]
    student=User.objects.get(id=studentid)
    student_name=student.first_name.capitalize()+ " "+student.last_name.capitalize()
    studymaterial=StudyMaterial.objects.get(id=id)
    file_name=studymaterial.file.name.split("/")[-1]
    return render(request,"student/student_view_study_material.html",{"student_name":student_name,"material":studymaterial,"file_name":file_name})



@user_passes_test(is_student)
def viewTeacher(request):
    id=request.session["student_id"]
    student=User.objects.get(id=id)
    student_name=student.first_name.capitalize()+ " "+student.last_name.capitalize()
    teachers=Teacher.objects.filter(emp__course_id=student.course_id,emp__usertype="teacher")
    return render(request,"student/view_teacher_info.html",{"teachers":teachers,"student_name":student_name})



@user_passes_test(is_student)
def studentProfile(request):
    if request.method=="POST":
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        mobile_number=request.POST["mobile_number"]
        id=request.session["student_id"]
        s=Student.objects.get(student=id)
        s.mobile_number=mobile_number
        u=User.objects.get(id=id)
        u.first_name=first_name
        u.last_name=last_name
        u.save()
        s.save()
        return HttpResponse('<script>alert("Profile Updated"); window.history.back();</script>') 
        
    else:
        id=request.session["student_id"]
        student=User.objects.get(id=id)
        student_name=student.first_name.capitalize()+ " "+student.last_name.capitalize()
        student=Student.objects.get(student=id)
        return render(request,"student/student_profile.html",{"edit":student,"student_name":student_name})

@user_passes_test(is_student)
def studentChangePassword(request):
    if request.method=="POST":
        current_password=request.POST["current_password"]
        print(current_password)
        new_password=request.POST["new_password"]
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
        id=request.session["student_id"]
        student=User.objects.get(id=id)
        student_name=student.first_name.capitalize()+ " "+student.last_name.capitalize()
        return render(request,"student/student_change_password.html",{"student_name":student_name})



def logouts(request):
    logout(request)
    return redirect("/")