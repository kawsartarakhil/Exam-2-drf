from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serailizers import *
from django.utils import timezone
from payments.models import Bill
from rest_framework.permissions import IsAuthenticated

class RegionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            regions = Region.objects.all()

        elif user.role in ["regional_admin", "school_admin"]:
            if user.role == "regional_admin":
                regions = Region.objects.filter(id=user.region_id)
            else:
                regions = Region.objects.filter(id=user.institution.region_id) if user.institution_id else Region.objects.none()

        else:
            return Response({"error": "Permission denied"}, status=403)
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "super_admin" or not request.user.is_superuser:
            return Response({"error": "Permission denied"}, status=403)
        serializer = RegionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            region = Region.objects.filter(id=pk).first()
        elif user.role == "regional_admin":
            region = Region.objects.filter(id=pk, id__in=[user.region_id]).first()


        elif user.role == "school_admin" and user.institution_id:
            region = Region.objects.filter(id=pk,id__in=Institution.objects.filter(id=user.institution_id).values("region_id")).first()
        else:
            return Response({"error": "Permission denied"}, status=403)
        if not region:
            return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RegionSerializer(region)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.role != "super_admin" or not request.user.is_superuser:
            return Response({"error": "Permission denied"}, status=403)
        region = Region.objects.filter(id=pk).first()

        if not region:
            return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RegionSerializer(region, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.role != "super_admin" or not request.user.is_superuser:
            return Response({"error": "Permission denied"}, status=403)
        region = Region.objects.filter(id=pk).first()

        if not region:
            return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

        region.delete()
        return Response({"message": "Region deleted successfully"}, status=status.HTTP_200_OK)


class InstitutionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            institutions = Institution.objects.all()
        elif user.role == "regional_admin" and user.region_id:
            institutions = Institution.objects.filter(region_id=user.region_id)

        elif user.role == "school_admin" and user.institution_id:
            institutions = Institution.objects.filter(id=user.institution_id)

        else:
            return Response({"error": "Permission denied"}, status=403)
        serializer = InstitutionSerializer(institutions, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            pass
        elif user.role == "regional_admin" and user.region_id:
            if str(request.data.get("region")) != str(user.region_id):
                return Response({"error": "Permission denied"}, status=403)

        else:
            return Response({"error": "Permission denied"}, status=403)
        serializer = InstitutionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstitutionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            institution = Institution.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            institution = Institution.objects.filter(id=pk, region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            institution = Institution.objects.filter(id=pk, id__in=[user.institution_id]).first()

        else:
            return Response({"error": "Permission denied"}, status=403)
        if not institution:
            return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InstitutionSerializer(institution)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            institution = Institution.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            institution = Institution.objects.filter(id=pk, region_id=user.region_id).first()
            if str(request.data.get("region")) != str(user.region_id):
                return Response({"error": "Cannot move institution to another region"}, status=403)
        else:
            return Response({"error": "Permission denied"}, status=403)
        if not institution:
            return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InstitutionSerializer(institution, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            institution = Institution.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            institution = Institution.objects.filter(id=pk, region_id=user.region_id).first()
        else:
            return Response({"error": "Permission denied"}, status=403)

        if not institution:
            return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)

        institution.delete()
        return Response({"message": "Institution deleted successfully"}, status=status.HTTP_200_OK)


class StudentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            students = Student.objects.all()
        elif user.role == "regional_admin" and user.region_id:
            students = Student.objects.filter(institution__region_id=user.region_id)
        elif user.role == "school_admin" and user.institution_id:
            students = Student.objects.filter(institution_id=user.institution_id)
        else:
            return Response({"error": "Permission denied"}, status=403)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user

        if user.role == "super_admin" and user.is_superuser:
            pass

        elif user.role == "regional_admin" and user.region_id:
            institution = Institution.objects.filter(id=request.data.get("institution"),region_id=user.region_id).first()
            if not institution:
                return Response({"error": "Permission denied"}, status=403)
        elif user.role == "school_admin" and user.institution_id:
            if str(request.data.get("institution")) != str(user.institution_id):
                return Response({"error": "Permission denied"}, status=403)
        else:
            return Response({"error": "Permission denied"}, status=403)
        
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            student = Student.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            student = Student.objects.filter(id=pk, institution__region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            student = Student.objects.filter(id=pk, institution_id=user.institution_id).first()
        else:
            return Response({"error": "Permission denied"}, status=403)
        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            student = Student.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            student = Student.objects.filter(id=pk, institution__region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            student = Student.objects.filter(id=pk, institution_id=user.institution_id).first()
        else:
            return Response({"error": "Permission denied"}, status=403)
        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        new_institution = request.data.get("institution")

        if user.role == "regional_admin":
            institution = Institution.objects.filter(id=new_institution, region_id=user.region_id).first()
            if not institution:
                return Response({"error": "Permission denied"}, status=403)

        elif user.role == "school_admin":
            if str(new_institution) != str(user.institution_id):
                return Response({"error": "Permission denied"}, status=403)
            
        serializer = StudentSerializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            student = Student.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            student = Student.objects.filter(id=pk, institution__region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            student = Student.objects.filter(id=pk, institution_id=user.institution_id).first()

        else:
            return Response({"error": "Permission denied"}, status=403)
        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        student.delete()
        return Response({"message": "Student deleted successfully"}, status=status.HTTP_200_OK)


class BookView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            books = Book.objects.all()
        elif user.role == "regional_admin" and user.region_id:
            books = Book.objects.filter(institution__region_id=user.region_id)
        elif user.role == "school_admin" and user.institution_id:
            books = Book.objects.filter(institution_id=user.institution_id)
        else:
            return Response({"error": "Permission denied"}, status=403)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            pass
        elif user.role == "regional_admin" and user.region_id:
            institution = Institution.objects.filter(id=request.data.get("institution"),region_id=user.region_id).first()

            if not institution:
                return Response({"error": "Permission denied"}, status=403)
            
        elif user.role == "school_admin" and user.institution_id:
            if str(request.data.get("institution")) != str(user.institution_id):
                return Response({"error": "Permission denied"}, status=403)
        else:
            return Response({"error": "Permission denied"}, status=403)
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            book = Book.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            book = Book.objects.filter(id=pk, institution__region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            book = Book.objects.filter(id=pk, institution_id=user.institution_id).first()
        else:
            return Response({"error": "Permission denied"}, status=403)

        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            book = Book.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            book = Book.objects.filter(id=pk, institution__region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            book = Book.objects.filter(id=pk, institution_id=user.institution_id).first()
        else:
            return Response({"error": "Permission denied"}, status=403)

        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        new_institution = request.data.get("institution")

        if user.role == "regional_admin":
            institution = Institution.objects.filter(id=new_institution, region_id=user.region_id).first()
            if not institution:
                return Response({"error": "Permission denied"}, status=403)
        elif user.role == "school_admin":
            if str(new_institution) != str(user.institution_id):
                return Response({"error": "Permission denied"}, status=403)

        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            book = Book.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            book = Book.objects.filter(id=pk, institution__region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            book = Book.objects.filter(id=pk, institution_id=user.institution_id).first()
        else:
            return Response({"error": "Permission denied"}, status=403)
        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_200_OK)


class BookLoanView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            loans = BookLoan.objects.all()

        elif user.role == "regional_admin" and user.region_id:
            loans = BookLoan.objects.filter(book__institution__region_id=user.region_id)

        elif user.role == "school_admin" and user.institution_id:
            loans = BookLoan.objects.filter(book__institution_id=user.institution_id)
        else:
            return Response({"error": "Permission denied"}, status=403)
        serializer = BookLoanSerializer(loans, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        
        serializer = BookLoanSerializer(data=request.data)

        if serializer.is_valid():
            student = serializer.validated_data["student"]
            book = serializer.validated_data["book"]
            year_of_use = serializer.validated_data["year_of_use"]
            if user.role == "super_admin" and user.is_superuser:
                pass
            elif user.role == "regional_admin" and user.region_id:
                if book.institution.region_id != user.region_id:
                    return Response({"error": "Permission denied"}, status=403)

            elif user.role == "school_admin" and user.institution_id:
                if book.institution_id != user.institution_id:
                    return Response({"error": "Permission denied"}, status=403)

            else:
                return Response({"error": "Permission denied"}, status=403)
            
            if student.institution_id != book.institution_id:
                return Response({"error": "Student and book must belong to the same institution"},status=status.HTTP_400_BAD_REQUEST)

            if book.available_quantity <= 0:
                return Response({"error": "Book is not available"},status=status.HTTP_400_BAD_REQUEST)

            if year_of_use < 1:
                return Response({"error": "Year of use must be at least 1"},status=status.HTTP_400_BAD_REQUEST)

            factor_year = min(year_of_use, 5)
            factor = BookPriceFactor.objects.filter(year_of_use=factor_year).first()

            if not factor:
                return Response({"error": "Book price factor not found"},status=status.HTTP_404_NOT_FOUND)
            
            calculated_price = round(float(book.price) * float(factor.percentage) / 100, 2)
            loan = serializer.save(calculated_price=calculated_price,status="borrowed",return_date=None)
            department_amount = round(calculated_price * 2 / 100, 2)
            school_amount = round(calculated_price - department_amount, 2)
            Bill.objects.create(book_loan=loan,total_amount=calculated_price,department_amount=department_amount,school_amount=school_amount,status="unpaid")
            book.available_quantity -= 1
            book.save()

            return Response(BookLoanSerializer(loan).data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BookLoanDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            loan = BookLoan.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            loan = BookLoan.objects.filter(id=pk,book__institution__region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            loan = BookLoan.objects.filter(id=pk,book__institution_id=user.institution_id).first()
        else:
            return Response({"error": "Permission denied"}, status=403)
        if not loan:
            return Response({"error": "Book loan not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = BookLoanSerializer(loan)
        return Response(serializer.data)


class BookReturnView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            loan = BookLoan.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            loan = BookLoan.objects.filter(id=pk,book__institution__region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            loan = BookLoan.objects.filter(id=pk,book__institution_id=user.institution_id).first()
        else:
            return Response({"error": "Permission denied"}, status=403)
        if not loan:
            return Response({"error": "Book loan not found"},status=status.HTTP_404_NOT_FOUND)

        if loan.status != "borrowed":
            return Response({"error": "This book cannot be returned"},status=status.HTTP_400_BAD_REQUEST)

        book = Book.objects.get(id=loan.book_id)
        loan.status = "returned"
        loan.return_date = timezone.now().date()
        loan.save()
        book.available_quantity += 1
        book.save()
        serializer = BookLoanSerializer(loan)
        return Response(serializer.data)


class BookLostView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        user = request.user
        if user.role == "super_admin" and user.is_superuser:
            loan = BookLoan.objects.filter(id=pk).first()
        elif user.role == "regional_admin" and user.region_id:
            loan = BookLoan.objects.filter(id=pk,book__institution__region_id=user.region_id).first()
        elif user.role == "school_admin" and user.institution_id:
            loan = BookLoan.objects.filter(id=pk,book__institution_id=user.institution_id).first()
        else:
            return Response({"error": "Permission denied"}, status=403)
        if not loan:
            return Response({"error": "Book loan not found"},status=status.HTTP_404_NOT_FOUND)

        if loan.status != "borrowed":
            return Response({"error": "Only borrowed books can be marked as lost"},status=status.HTTP_400_BAD_REQUEST)

        loan.status = "lost"
        loan.save()
        serializer = BookLoanSerializer(loan)
        return Response(serializer.data)


class BookPriceFactorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role not in ["super_admin", "regional_admin", "school_admin"]:
            return Response({"error": "Permission denied"}, status=403)
        if user.role == "super_admin" and not user.is_superuser:
            return Response({"error": "Permission denied"}, status=403)

        factors = BookPriceFactor.objects.all()
        serializer = BookPriceFactorSerializer(factors, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if user.role != "super_admin" or not user.is_superuser:
            return Response({"error": "Permission denied"}, status=403)
        serializer = BookPriceFactorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class BookPriceFactorDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user

        if user.role not in ["super_admin", "regional_admin", "school_admin"]:
            return Response({"error": "Permission denied"}, status=403)

        if user.role == "super_admin" and not user.is_superuser:
            return Response({"error": "Permission denied"}, status=403)

        factor = BookPriceFactor.objects.filter(id=pk).first()

        if not factor:
            return Response({"error": "Factor not found"}, status=404)

        serializer = BookPriceFactorSerializer(factor)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user
        if user.role != "super_admin" or not user.is_superuser:
            return Response({"error": "Permission denied"}, status=403)
        factor = BookPriceFactor.objects.filter(id=pk).first()

        if not factor:
            return Response({"error": "Factor not found"}, status=404)
        serializer = BookPriceFactorSerializer(factor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = request.user
        if user.role != "super_admin" or not user.is_superuser:
            return Response({"error": "Permission denied"}, status=403)
        factor = BookPriceFactor.objects.filter(id=pk).first()
        if not factor:
            return Response({"error": "Factor not found"}, status=404)

        factor.delete()
        return Response({"message": "Factor deleted successfully"})
