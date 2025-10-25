from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(student)
admin.site.register(company)
admin.site.register(Internship)
admin.site.register(Application)
admin.site.register(Feedback)