from django.urls import path
from .views import StudentProfileView, AdminProfileView

app_name = "profiles"

urlpatterns = [
    path('student/', StudentProfileView.as_view(), name='student-profile'),
    path('admin/', AdminProfileView.as_view(), name='admin-profile'),
]
