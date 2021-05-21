from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField(read_only=True)
    interests = serializers.SerializerMethodField(read_only=True)
    skills = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_profile_pic(self, obj):
        try:
            pic = 'static' + obj.profile_pic.url
        except:
            pic = None
        return pic

    def get_interests(self, obj):
        interests = obj.interests.values_list('name', flat=True)
        return interests

    def get_skills(self, obj):
        skills = obj.skills.values_list('name', flat=True)
        return skills


class CurrentUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'profile', 'username','email','is_superuser', 'is_staff']

    def get_profile(self, obj):
        profile = obj.userprofile
        serializer = UserProfileSerializer(profile, many=False)
        return serializer.data

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'profile', 'username', 'is_superuser', 'is_staff']

    def get_profile(self, obj):
        profile = obj.userprofile
        serializer = UserProfileSerializer(profile, many=False)
        return serializer.data


class UserSerializerWithToken(UserSerializer):
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_access(self, obj):
        token = RefreshToken.for_user(obj)

        token['username'] = obj.username
        token['name'] = obj.userprofile.name
        token['profile_pic'] = 'static' + obj.userprofile.profile_pic.url
        token['is_staff'] = obj.is_staff
        token['id'] = obj.id
        return str(token.access_token)
    
    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)