app_name = 'streams'

from django.urls import path
from .views import (
    StreamListCreateView,
    StreamRetrieveView,
    StreamStudentsListView,
    SubmitExamAPIView,
    StreamResultsPDFView
)

urlpatterns = [
    path('', StreamListCreateView.as_view()),
    path('<uuid:pk>/', StreamRetrieveView.as_view()),
    path('<uuid:stream_id>/students/', StreamStudentsListView.as_view()),
    path('<uuid:stream_id>/pdf/', StreamResultsPDFView.as_view()),  # PDF выгрузка
    path('submit/', SubmitExamAPIView.as_view()),
]
