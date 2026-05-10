from rest_framework import serializers
from user.models import Tag
from .user import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Tag
        fields = ["id", "name", "user", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at", "user"]


class TagWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]
