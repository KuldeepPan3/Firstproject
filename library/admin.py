from django.contrib import admin
from .models import Student,Books, IssuedItem
# Register your models here.
admin.site.register(Student)
admin.site.register(Books)
admin.site.register(IssuedItem)