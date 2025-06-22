from rest_framework import serializers
from users.models import User
from .models import StudentProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'created_at')
        read_only_fields = ('id', 'role', 'created_at', 'email')


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('id', 'avatar', 'bio', 'language')
