from rest_framework import serializers
from user.models import User
from .role import RoleSerializer


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "username", "roles", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserDetailSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "username", "roles", "created_at", "updated_at"]
        read_only_fields = ["id", "email", "username", "created_at", "updated_at"]
