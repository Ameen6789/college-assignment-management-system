from django.urls import path
from assignment_management_app.studentviews import *
from assignment_management_app.teacherviews import *
from assignment_management_app.adminviews import *
from assignment_management_app.views import *
urlpatterns = [
    
    path("",home),
    path("logout",logouts),

    #admin urls

    path('admin_login',adminlogin),
    path("dashboard",dashboard),
    path("teacher",teacher),
    path("delete_teacher/<int:id>",deleteTeacher),
    path("change_password",changePassword),
    path("course",course,name="course"),
    path("delete_course/<int:id>",deleteCourse),
    path("edit_course/<int:id>",editCourse),
    path("subject",subject),
    path("delete_subject/<int:id>",deleteSubject),
    path("edit_subject/<int:id>",editSubject),
    path("reg_stud",regStud),
    path("approve_student/<int:id>",approveStudent),
    path("delete_student/<int:id>",deleteStudent),
    path("news",news),
    path("delete_news/<int:id>",deleteNews),
    path("edit_news/<int:id>",editNews),
    path("unchecked_assignment",uncheckedAssignment),
    path("checked_assignment",checkedAssignment),
    path("admin_view_unchecked_assign/<int:assignment_no>/<int:student_id>",admin_view_unchecked_assignment),
    path("admin_view_checked_assign/<int:assignment_no>/<int:student_id>",admin_view_checked_assignment),
    path("btw_date_assignment",btw_date_assignment,name="btw_date_assignment"),
    path("search",search),


    #teacher urls

    path("teacher_login",teacherlogin),
    path("teacher_dashboard",teacherdashboard),
    path("teacher_assignment",teacherAssignment),
    path("teacher_edit_assignment/<int:id>",teacherEditAssignment),
    path("teacher_news",teacherNews),
    path("teacher_delete_news/<int:id>",teacherDeleteNews),
    path("teacher_edit_news/<int:id>",teacherEditNews),
    path("teacher_unchecked_assignment",teacherUncheckedAssignment,name='teacher_unchecked_assignment'),
    path("teacher_checked_assignment",teacherCheckedAssignment),
    path("view_unchecked_assignment/<int:assignment_no>/<int:student_id>",viewUncheckedAssignment),
    path("view_checked_assignment/<int:assignment_no>/<int:student_id>",viewCheckedAssignment),
    path("study_material",studyMaterial,name="study_material"),
    path("edit_study_material/<int:id>",editStudyMaterial,name="edit_study_material"),
    path("delete_study_material/<int:id>",deleteStudyMaterial,name="delete_study_material"),
    path("course_wise_student",courseWiseStudent),
    path("teacher_profile",teacherProfile),
    path("teacher_change_password",teacherChangePassword),



    #student urls
    
    path("student_login",studentlogin),
    path("student_dashboard",studentdashboard),
    path("new_assignment",newAssignment),
    path("submit_assignment/<int:id>",submitAssignment),
    path("upload_assignment",uploadAssignment),
    path("view_submitted_assignment/<int:id>",viewSubmittedAssignment),
    path("student_study_material",studentStudyMaterial),
    path("view_study_material/<int:id>",studentViewStudyMaterial),
    path("view_teacher",viewTeacher,name="view_teacher"),
    path("student_profile",studentProfile),
    path("register",register),
    path("student_change_password",studentChangePassword),
]