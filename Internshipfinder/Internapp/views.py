from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re  


# Create your views here.

def index(request):
    return render(request,'home.html')

def stdlogin(request):
    return render(request,'login.html')

def cmplogin(request):
    return render(request,'cmplogin.html')


def userreg(request):
    if request.method == 'POST':
        Firstname = request.POST.get('fname', '').strip()
        Lastname = request.POST.get('lname', '').strip()
        Email = request.POST.get('email', '').strip()
        DOB = request.POST.get('dob', '').strip()
        Password = request.POST.get('password', '').strip()
        ConfirmPassword = request.POST.get('Confirm Password', '').strip()

        # Helper function for alerts
        def alert(msg, back=True):
            if back:
                return HttpResponse(f"<script>alert('{msg}'); window.history.back();</script>")
            else:
                return HttpResponse(f"<script>alert('{msg}');</script>")

        # ---- Validations ----
        if not Firstname or not Lastname or not Email or not DOB or not Password or not ConfirmPassword:
            return alert("⚠️ All fields are required!")

        if not Firstname.isalpha():
            return alert("⚠️ First name must contain only alphabets!")

        if not Lastname.isalpha():
            return alert("⚠️ Last name must contain only alphabets!")

        try:
            validate_email(Email)
        except ValidationError:
            return alert("⚠️ Invalid email format!")

        if student.objects.filter(Email=Email).exists():
            return alert("⚠️ Email already registered!")

        if not re.match(r'^\d{4}-\d{2}-\d{2}$', DOB):
            return alert("⚠️ DOB must be in YYYY-MM-DD format!")

        if len(Password) < 6:
            return alert("⚠️ Password must be at least 6 characters long!")
        if not re.search(r'[A-Z]', Password):
            return alert("⚠️ Password must contain at least one uppercase letter!")
        if not re.search(r'[a-z]', Password):
            return alert("⚠️ Password must contain at least one lowercase letter!")
        if not re.search(r'[0-9]', Password):
            return alert("⚠️ Password must contain at least one digit!")
        if not re.search(r'[@$!%*?&]', Password):
            return alert("⚠️ Password must contain at least one special character (@$!%*?&)!")

        if Password != ConfirmPassword:
            return alert("⚠️ Passwords do not match!")

        # ---- Save data ----
        student.objects.create(
            first_name=Firstname,
            last_name=Lastname,
            Email=Email,
            date=DOB,
            password=Password
        )

        return HttpResponse("<script>alert('✅ Registration successful!'); window.location='/';</script>")

    return HttpResponse("<script>alert('⚠️ Invalid request method!'); window.history.back();</script>")
    

def userlogin(request):
    if request.method == 'POST':
        Email = request.POST['email']
        Password = request.POST['password']
        if Email == "admin@gmail.com" and Password == "admin":
            total_companies = company.objects.count()
            pending_companies = company.objects.filter(status=0).count()
            active_users = company.objects.filter(status=1).count()
            blocked_count = company.objects.filter(status=2).count()
            companies = company.objects.all().order_by('-id')

            context = {
                "total_companies": total_companies,
                "pending_companies": pending_companies,
                "active_users": active_users,
                'blocked_count': blocked_count,
                'companies': companies
            }
            return render(request,'Adminhome.html',context) 

        
        try:
            data = student.objects.get(Email=Email, password=Password)
            request.session['sid'] = Email
            return render(request, "index.html")
        except student.DoesNotExist:
            return HttpResponse('<script>alert("Invalid email or password!"); window.location.href="/stdlogin";</script>')
    
    return HttpResponse('invalid')


      
def register_company(request):
    if request.method == "POST":
        company_name = request.POST.get("cmpname", "").strip()
        company_owner = request.POST.get("cmpowner", "").strip()
        company_email = request.POST.get("cmpemail", "").strip()
        company_address = request.POST.get("cmpaddress", "").strip()
        company_password = request.POST.get("cmppassword", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        # helper function for alerts
        def alert(msg, redirect="/cmplogin"):
            return HttpResponse(f'<script>alert("{msg}"); window.location.href="{redirect}";</script>')

        # ---- Validations ----
        if not company_name or not company_owner or not company_email or not company_address or not company_password or not confirm_password:
            return alert("⚠️ All fields are required!")

        if not company_name.replace(" ", "").isalpha():
            return alert("⚠️ Company name must contain only alphabets!")

        if not company_owner.replace(" ", "").isalpha():
            return alert("⚠️ Owner name must contain only alphabets!")

        try:
            validate_email(company_email)
        except ValidationError:
            return alert("⚠️ Invalid email format!")

        if company.objects.filter(company_email=company_email).exists():
            return alert("⚠️ Email is already registered!")

        if len(company_password) < 6:
            return alert("⚠️ Password must be at least 6 characters long!")
        if not re.search(r'[A-Z]', company_password):
            return alert("⚠️ Password must contain at least one uppercase letter!")
        if not re.search(r'[a-z]', company_password):
            return alert("⚠️ Password must contain at least one lowercase letter!")
        if not re.search(r'[0-9]', company_password):
            return alert("⚠️ Password must contain at least one digit!")
        if not re.search(r'[@$!%*?&]', company_password):
            return alert("⚠️ Password must contain at least one special character (@$!%*?&)!")

        if company_password != confirm_password:
            return alert("⚠️ Passwords do not match!")

        # ---- Save company ----
        company.objects.create(
            company_name=company_name,
            company_owner=company_owner,
            company_email=company_email,
            company_address=company_address,
            company_password=company_password,  # (⚠️ better to hash this)
            status=0
        )

        return alert("✅ Company registered successfully!", redirect="/cmplogin")

    return render(request, "cmplogin.html")



def login_company(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            comp = company.objects.get(company_email=email, company_password=password)
            
            if comp.status == 0:
                return HttpResponse('<script>alert("Admin needs to approve your registration. Please wait."); window.location.href="/cmplogin";</script>')
            else:
                
                request.session['cid'] = email  

                comp = company.objects.get(company_email=request.session['cid'])

                internships = Internship.objects.filter(company=comp)
           
                
                return render (request,'cmpindex.html',{"internships": internships})        
        except company.DoesNotExist:
            return HttpResponse('<script>alert("Invalid email or password!"); window.location.href="/cmplogin";</script>')

    return render(request, "cmplogin.html")



def update_company_status(request, cid, action):
    comp = get_object_or_404(company, id=cid)

    if action == "approve":
        comp.status = 1   # Active
        comp.save()
    elif action == "reject":
        comp.delete()     # Delete company
    elif action == "block":
        comp.status = 2   # Blocked
        comp.save()
    elif action == "unblock":
        comp.status = 1   # Back to Active
        comp.save()

    total_companies = company.objects.count()
    pending_companies = company.objects.filter(status=0).count()
    active_users = company.objects.filter(status=1).count()
    blocked_count = company.objects.filter(status=2).count()
    companies = company.objects.all().order_by('-id')

    context = {
        "total_companies": total_companies,
        "pending_companies": pending_companies,
        "active_users": active_users,
        'blocked_count': blocked_count,
        'companies': companies
    }
    return render(request,'Adminhome.html',context)

def openintern(request):
    return render(request,'post_internship.html')

def post_internship(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")
        stipend = request.POST.get("stipend")
        duration = request.POST.get("duration")

        # get logged in company from session
        comp = company.objects.get(company_email=request.session['cid'])

        # create internship
        Internship.objects.create(
            company=comp,
            title=title,
            description=description,
            location=location,
            stipend=stipend,
            duration=duration,
            status="active"
        )

        return HttpResponse("<script>alert('Internship Posted Successfully!');window.location='openintern';</script>")

    return render(request, "post_internship.html")


def company_applications(request):
    if 'cid' not in request.session:  
        return render(request,'cmplogin.html')

    try:
        comp = company.objects.get(company_email=request.session['cid'])
    except company.DoesNotExist:
        return render(request,'cmplogin.html')


    applications = Application.objects.filter(internship__company=comp).select_related("student", "internship")

    return render(request, "company_applications.html", {"applications": applications})


def accept_application(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    app.status = "accepted"
    app.save()
    return redirect("company_applications")

def reject_application(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    app.status = "rejected"
    app.save()
    return redirect("company_applications")

def logout(request):
    if 'cid' in request.session:
        request.session.flush()

        return render(request,'home.html')
    elif  'sid' in request.session:
        request.session.flush()
        return render(request,'home.html')
    
    else:
        return render(request,'home.html')
    


def student_internships(request):
    # Base queryset
    internships_list = Internship.objects.filter(status="active").order_by('-created_at')


    # Filtering
    title = request.GET.get('title')
    location = request.GET.get('location')
    duration = request.GET.get('duration')

    if title:
        internships_list = internships_list.filter(title__icontains=title)
    if location:
        internships_list = internships_list.filter(location__icontains=location)
    if duration:
        internships_list = internships_list.filter(duration=duration)

    # Pagination
    paginator = Paginator(internships_list, 6)  # 6 internships per page
    page_number = request.GET.get('page')
    internships = paginator.get_page(page_number)

    return render(request, "student_internships.html", {
        "internships": internships
    })


def company_detail(request, id):
    company_obj = get_object_or_404(company, id=id)
    internships = company_obj.internships.filter(status="active").order_by('-created_at')

    return render(request, "company_detail.html", {
        "company": company_obj,
        "internships": internships
    })

def apply_internship(request, internship_id):
    if request.method == "POST":
        internship = get_object_or_404(Internship, id=internship_id)
        
        student_id = request.session.get("sid")  # Assuming student is logged in
        if not student_id:
            messages.error(request, "You must log in to apply.")
            return redirect("student_internships")

        try:
            student_obj = get_object_or_404(student, Email=student_id)
        except:
            messages.error(request, "Student not found.")
            return redirect("student_internships")

        cover_letter = request.POST.get("cover_letter", "")
        resume = request.FILES.get("resume")

        # Check if application already exists
        if Application.objects.filter(student=student_obj, internship=internship).exists():
            messages.error(request, "You have already applied for this internship.")
            return redirect("student_internships")

        Application.objects.create(
            student=student_obj,
            internship=internship,
            cover_letter=cover_letter,
            resume=resume,
            status="pending",
            applied_at=timezone.now()
        )
        messages.success(request, "Application submitted successfully!")
        return redirect("student_internships")

    messages.error(request, "Invalid request method.")
    return redirect("student_internships")

def student_applications(request):
    student_id = request.session.get("sid")
    if not student_id:
        messages.error(request, "Please log in first.")
        return redirect("stdlogin")

    try:
        student_obj = student.objects.get(Email=student_id)
    except student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect("stdlogin")

    applications = Application.objects.filter(student=student_obj).select_related("internship", "internship__company").order_by('-applied_at')

    return render(request, "student_applications.html", {"applications": applications})


def student_profile(request):
    student_id = request.session.get("sid")
    if not student_id:
        messages.error(request, "Please log in first.")
        return redirect("stdlogin")

    try:
        student_obj = student.objects.get(Email=student_id)
    except student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect("stdlogin")

    return render(request, "student_profile.html", {"student": student_obj})


def cmpback(request):
    if 'cid' in request.session:
        comp = company.objects.get(company_email=request.session['cid'])
        internships = Internship.objects.filter(company=comp)        
        return render (request,'cmpindex.html',{"internships": internships})
        
    return render(request,'home.html')

def comprofile(request):
    if 'cid' in request.session:
        comp = company.objects.get(company_email=request.session['cid'])
        return render(request,'cmpprofile.html',{'cmp':comp})
    return render(request,'home.html')

def company_profile(request, company_id):
    cmp = get_object_or_404(company, id=company_id)

    if request.method == "POST":
        cmp.company_name = request.POST.get("cmpname", cmp.company_name).strip()
        cmp.company_owner = request.POST.get("cmpowner", cmp.company_owner).strip()
        cmp.company_email = request.POST.get("cmpemail", cmp.company_email).strip()
        cmp.company_address = request.POST.get("cmpaddress", cmp.company_address).strip()
        cmp.save()
        return HttpResponse(f'<script>alert("✅ Profile updated successfully!"); window.location.href="/cprofile";</script>')

    return render(request, "cmpprofile.html", {"cmp": cmp})

def delete_internship(request, id):
    internship = get_object_or_404(Internship, id=id)
    internship.delete()
    comp = company.objects.get(company_email=request.session['cid'])

    internships = Internship.objects.filter(company=comp)
           
                
    return render (request,'cmpindex.html',{"internships": internships})


def stdback(request):
    if 'sid' in request.session:
        
        return render (request,'index.html')
        
    return render(request,'home.html')


def student_profile(request):
    students = get_object_or_404(student, Email=request.session['sid'])  # assuming Student has a OneToOne with User

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("Email")
        date = request.POST.get("date")
        photo = request.FILES.get("photo")

        # update fields
        students.first_name = first_name
        students.last_name = last_name
        students.Email = email
        students.date = date

        if photo:
            students.photo = photo   # student model should have ImageField (photo)

        students.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("student_profile")  # name of your profile url

    return render(request, "student_profile.html", {"student": students})



def admin_users(request):
    users = student.objects.all()
    return render(request, "students.html", {"students": users})


def admin_companies(request):
    companies = company.objects.all()
    return render(request, "company.html", {"companies": companies})



def admin_internships(request):
    internships = Internship.objects.select_related("company").all()
    return render(request, "internship.html", {"internships": internships})



def forgot_password(request, user_type):
    if request.method == "POST":
        email = request.POST.get("email")
        
        if user_type == "student":
            user = student.objects.filter(Email=email).first()
        else:
            user = company.objects.filter(company_email=email).first()
        
        if user:
            request.session['reset_email'] = email
            request.session['reset_type'] = user_type
            return redirect("reset_password")
        else:
            messages.error(request, "Email not found. Please try again.")
    
    return render(request, "forgot_password.html", {"user_type": user_type})


# Reset password - step 2 (enter new password)
def reset_password(request):
    email = request.session.get("reset_email")
    user_type = request.session.get("reset_type")

    if not email or not user_type:
        messages.error(request, "Invalid password reset request.")
        return redirect("home") 

    if request.method == "POST":
        new_pass = request.POST.get("password")
        confirm_pass = request.POST.get("confirm_password")
        
        if new_pass != confirm_pass:
            messages.error(request, "❌ Passwords do not match!")
            return redirect("reset_password")
        
        if user_type == "student":
            user = student.objects.get(Email=email)
            user.password = new_pass
            user.save()
            messages.success(request, "✅ Password updated successfully. Please login.")
            request.session.flush()
            return render(request,'login.html') 
        
        elif user_type == "company":
            user = company.objects.get(company_email=email)
            user.company_password = new_pass
            user.save()
            messages.success(request, "✅ Password updated successfully. Please login.")
            request.session.flush()
            return render(request,'cmplogin.html') 
    
    return render(request, "reset_password.html", {"email": email})


def student_feedback(request):
    if request.method == "POST":
        Feedback.objects.create(
            student_name=request.POST.get("student_name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")
        )
        messages.success(request, "Thanks for your feedback!")
        return redirect("student_feedback")
    return render(request, "student_feedback.html")

def admin_view_feedbacks(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, "admin_feedback.html", {"feedbacks": feedbacks})