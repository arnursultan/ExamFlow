from rest_framework import generics, permissions
from users.models import User
from .models import StudentProfile
from .serializers import UserProfileSerializer, StudentProfileSerializer
from .permissions import IsStudent, IsAdmin


class StudentProfileView(generics.RetrieveUpdateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_object(self):
        return self.request.user.student_profile


class AdminProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_object(self):
        return self.request.user
