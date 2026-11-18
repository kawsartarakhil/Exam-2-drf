from django.urls import path
from .views import *

urlpatterns = [
    path("regions/", RegionView.as_view()),
    path("regions/<int:pk>/", RegionDetailView.as_view()),
    path("institutions/", InstitutionView.as_view()),
    path("institutions/<int:pk>/", InstitutionDetailView.as_view()),
    path("students/", StudentView.as_view()),
    path("students/<int:pk>/", StudentDetailView.as_view()),
    path("books/", BookView.as_view()),
    path("books/<int:pk>/", BookDetailView.as_view()),
    path("book-loans/", BookLoanView.as_view()),
    path("book-loans/<int:pk>/", BookLoanDetailView.as_view()),
    path("book-loans/<int:pk>/return/", BookReturnView.as_view()),
    path("book-loans/<int:pk>/lost/", BookLostView.as_view()),
    path("factors/", BookPriceFactorView.as_view()),
path("factors/<int:pk>/", BookPriceFactorDetailView.as_view()),
]
