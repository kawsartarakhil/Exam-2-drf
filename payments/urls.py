from django.urls import path
from .views import *

urlpatterns = [
    path("invoices/", BillView.as_view()),
    path("invoices/<int:pk>/", BillDetailView.as_view()),
    path("payments/", PaymentView.as_view()),
    path("payments/<int:pk>/", PaymentDetailView.as_view()),
]
