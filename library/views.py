from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serailizers import *
from django.utils import timezone

class RegionView(APIView):
    def get(self, request):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegionDetailView(APIView):
    def get(self, request, pk):
        region = Region.objects.filter(id=pk).first()

        if not region:
            return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RegionSerializer(region)
        return Response(serializer.data)

    def put(self, request, pk):
        region = Region.objects.filter(id=pk).first()

        if not region:
            return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RegionSerializer(region, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        region = Region.objects.filter(id=pk).first()

        if not region:
            return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

        region.delete()
        return Response({"message": "Region deleted successfully"}, status=status.HTTP_200_OK)


class InstitutionView(APIView):
    def get(self, request):
        institutions = Institution.objects.all()
        serializer = InstitutionSerializer(institutions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InstitutionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstitutionDetailView(APIView):
    def get(self, request, pk):
        institution = Institution.objects.filter(id=pk).first()

        if not institution:
            return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InstitutionSerializer(institution)
        return Response(serializer.data)

    def put(self, request, pk):
        institution = Institution.objects.filter(id=pk).first()

        if not institution:
            return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InstitutionSerializer(institution, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        institution = Institution.objects.filter(id=pk).first()

        if not institution:
            return Response({"error": "Institution not found"}, status=status.HTTP_404_NOT_FOUND)

        institution.delete()
        return Response({"message": "Institution deleted successfully"}, status=status.HTTP_200_OK)


class StudentView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    def get(self, request, pk):
        student = Student.objects.filter(id=pk).first()

        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = Student.objects.filter(id=pk).first()

        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = Student.objects.filter(id=pk).first()

        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        student.delete()
        return Response({"message": "Student deleted successfully"}, status=status.HTTP_200_OK)


class BookView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    def get(self, request, pk):
        book = Book.objects.filter(id=pk).first()

        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = Book.objects.filter(id=pk).first()

        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = Book.objects.filter(id=pk).first()

        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_200_OK)


class BookLoanView(APIView):
    def get(self, request):
        loans = BookLoan.objects.all()
        serializer = BookLoanSerializer(loans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookLoanSerializer(data=request.data)

        if serializer.is_valid():
            student = serializer.validated_data["student"]
            book_id = serializer.validated_data["book"].id
            year_of_use = serializer.validated_data["year_of_use"]

            book = Book.objects.filter(id=book_id).first()

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
            book.available_quantity -= 1
            book.save()

            return Response(BookLoanSerializer(loan).data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BookLoanDetailView(APIView):
    def get(self, request, pk):
        loan = BookLoan.objects.filter(id=pk).first()
        if not loan:
            return Response({"error": "Book loan not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = BookLoanSerializer(loan)
        return Response(serializer.data)


class BookReturnView(APIView):
    def put(self, request, pk):
        loan = BookLoan.objects.filter(id=pk).first()
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
    def put(self, request, pk):
        loan = BookLoan.objects.filter(id=pk).first()
        if not loan:
            return Response({"error": "Book loan not found"},status=status.HTTP_404_NOT_FOUND)

        if loan.status != "borrowed":
            return Response({"error": "Only borrowed books can be marked as lost"},status=status.HTTP_400_BAD_REQUEST)

        loan.status = "lost"
        loan.save()
        serializer = BookLoanSerializer(loan)
        return Response(serializer.data)
