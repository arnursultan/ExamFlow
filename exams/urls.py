app_name = 'exams'

from django.urls import path
from .views import ExamListCreateView, ExamRetrieveView, ExamImportAPIView

urlpatterns = [
    path('', ExamListCreateView.as_view()),
    path('<uuid:pk>/', ExamRetrieveView.as_view()),
    path('import/ai/', ExamImportAPIView.as_view())
]
