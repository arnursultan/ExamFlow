app_name = 'streams'

from django.urls import path
from .views import (
    StreamListCreateView, StreamRetrieveView,
    StreamStudentsListView, SubmitExamAPIView
)

urlpatterns = [
    path('', StreamListCreateView.as_view()),
    path('<uuid:pk>/', StreamRetrieveView.as_view()),
    path('<uuid:stream_id>/students/', StreamStudentsListView.as_view()),
    path('submit-exam/', SubmitExamAPIView.as_view()),
]
