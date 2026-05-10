from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Role, Tag, User, Post, Comment


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "username", "roles", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

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

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True, required=False)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "tags", "tag_ids", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def create(self, validated_data):
        tags = validated_data.pop('tag_ids', [])
        post = Post.objects.create(**validated_data)
        if tags:
            post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_ids', None)
        post = super().update(instance, validated_data)
        if tags is not None:
            post.tags.set(tags)
        return post
class PostWriteSerializer(serializers.ModelSerializer):
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True, required=False)
    class Meta:
        model = Post
        fields = ["title", "content", "tag_ids"]

    def create(self, validated_data):
        tags = validated_data.pop('tag_ids', [])
        post = Post.objects.create(**validated_data)
        if tags:
            post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_ids', None)
        post = super().update(instance, validated_data)
        if tags is not None:
            post.tags.set(tags)
        return post


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Comment
        fields = ["id", "content", "author", "post", "parent", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content", "post", "parent"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "full_name", "username", "password", "password_confirm"]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data, role_name=None):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        if role_name:
            role = Role.objects.get(name=role_name)
            user.roles.add(role)
        
        return user


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "full_name", "username", "password", "password_confirm"]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        # Assign user role
        role, _ = Role.objects.get_or_create(name=Role.ROLE_USER)
        user.roles.add(role)
        
        return user


class RegisterAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "full_name", "username", "password", "password_confirm"]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        # Assign both user and admin roles
        user_role, _ = Role.objects.get_or_create(name=Role.ROLE_USER)
        admin_role, _ = Role.objects.get_or_create(name=Role.ROLE_ADMIN)
        user.roles.add(user_role, admin_role)
        
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        request = self.context.get('request')
        user = authenticate(request=request, username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        data['user'] = user
        return data

    def response(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }

class UserDetailSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "username", "roles", "created_at", "updated_at"]
        read_only_fields = ["id", "email", "username", "created_at", "updated_at"]