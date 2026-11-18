from django.db import models
from django.conf import settings


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    full_name = models.CharField(max_length=200)
    grade = models.PositiveIntegerField()
    class_letter = models.CharField(max_length=5)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    acquisition_year = models.PositiveIntegerField()
    total_quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()
    grade = models.PositiveIntegerField()
    class_letter = models.CharField(max_length=5)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class BookPriceFactor(models.Model):
    year_of_use = models.PositiveIntegerField(unique=True)
    percentage = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return str(self.year_of_use)


class BookLoan(models.Model):
    status_choice = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('lost', 'Lost'),
    ]

    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    year_of_use = models.PositiveIntegerField()
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=status_choice,default='borrowed')
    calculated_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __str__(self):
        return f"{self.student.full_name} - {self.book.title}"
