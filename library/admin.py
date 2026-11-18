from django.contrib import admin
from .models import *

admin.site.register(Region)
admin.site.register(Institution)
admin.site.register(Student)
admin.site.register(Book)
admin.site.register(BookPriceFactor)
admin.site.register(BookLoan)