from rest_framework import serializers
from .models import Category, User, Course, VideoClass

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    is_instructor = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email","password", "is_instructor"]

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance

class VideoClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoClass
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(required=False)
    students_count = serializers.SerializerMethodField()
    videoclass_list = VideoClassSerializer(read_only = True, many=True)
    is_joined = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "name", "instructor", "created_at", "description", "students_count", "videoclass_list", "is_joined", "cover"]

    def get_students_count(self, obj):
        return obj.students.count()

    def get_is_joined(self, obj):
        user =  self.context['request'].user
        if user != None:
            return obj.students.filter(id=user.id).exists()

class CategorySerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)

    class Meta:
        model = Category
        fields = ["name", "courses"]