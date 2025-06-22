from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'created_at', 'is_active')
        read_only_fields = ('id', 'created_at', 'is_active', 'email', 'role')
