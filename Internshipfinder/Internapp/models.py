from django.db import models
from django.utils import timezone

# Create your models here.

class student(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=40)
    Email=models.EmailField()
    date=models.DateField()
    password=models.CharField(max_length=20)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)


    def __str__(self):
        return self.first_name



class company(models.Model):
    company_name=models.CharField(max_length=30)
    company_owner = models.CharField(max_length=30)
    company_email=models.EmailField()
    company_address=models.CharField(max_length=100)
    company_password=models.CharField(max_length=20)
    status  = models.IntegerField(default=0)

    def __str__(self):
        return self.company_name
    
class Internship(models.Model):
    company = models.ForeignKey(company, on_delete=models.CASCADE, related_name="internships")
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    stipend = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('closed', 'Closed')],
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    student = models.ForeignKey(
        student, on_delete=models.CASCADE, related_name="applications"
    )
    internship = models.ForeignKey(
        Internship, on_delete=models.CASCADE, related_name="applications"
    )
    cover_letter = models.TextField(blank=True, null=True) 
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)  
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'internship') 

    def __str__(self):
        return f"{self.student.first_name} -> {self.internship.title} ({self.status})"
    
class Feedback(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student_name} - {self.subject}"