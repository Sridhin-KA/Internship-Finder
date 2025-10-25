"""
URL configuration for fireandsafety project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Internapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",index,name='home'),
    path('register',userreg),
    path("login",userlogin),
    path('stdlogin',stdlogin),
    path('cmplogin',cmplogin),
    path('cmpregister',register_company),
    path('logincmp',login_company),
    path('update_company/<int:cid>/<str:action>/',update_company_status, name="update_company_status"),
    path('openintern',openintern),
    path("post_internship",post_internship, name="post_internship"),
    path("applications/", company_applications, name="company_applications"),
    path("applications/<int:app_id>/accept/", accept_application, name="accept_application"),
    path("applications/<int:app_id>/reject/", reject_application, name="reject_application"),
    path('logout',logout),
    path('student/internships/', student_internships, name="student_internships"),
    path('apply/<int:internship_id>/', apply_internship, name="apply_internship"),
    path('student/applications/',student_applications, name='student_applications'),
    path('student/profile/',student_profile, name='student_profile'),
    path('cmpback',cmpback),
    path('stdback',stdback),
    path('cprofile',comprofile),
    path("company_profile/<int:company_id>",company_profile, name="company_profile"),
    path('internship/delete/<int:id>/', delete_internship, name='delete_internship'),
     path("profile/",student_profile, name="student_profile"),
    path("users",admin_users, name="users"),
    path("companies",admin_companies, name="companies"),
    path("internships", admin_internships, name="internships"),
    path("company/<int:id>/", company_detail, name="company_detail"),
    path("forgot-password/<str:user_type>/",forgot_password, name="forgot_password"),
    path("reset-password/", reset_password, name="reset_password"),
    path('feedback/', student_feedback, name='student_feedback'),
    path('adminfeedback', admin_view_feedbacks, name='admin_view_feedbacks'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)