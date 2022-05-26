from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.db.models import Q

from .serializers import CategorySerializer, UserSerializer, CourseSerializer, VideoClassSerializer
from .models import Category, Course

class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user_id": user.id,
            "username": user.username,
            "token": token.key,
            "is_instructor": user.is_instructor
        })

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_instructor': user.is_instructor
        })

class UpdateUser(APIView):
    serializer_class = UserSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

class Home(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class Explore(generics.ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        queryset = Course.objects.all()
        if q:
            #filtrar nome da categoria tambem
            queryset = queryset.filter(Q(name__icontains=q))
            print(queryset)

        return queryset

class CourseCreate(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_instructor:
            serializer.save(instructor=self.request.user)

class CourseRetrieve(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

class CourseUpdate(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    
class CourseDestroy(generics.DestroyAPIView):    
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

class MyCourseList(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Course.objects.all()
        if self.request.user.is_instructor:
            return self.request.user.course_list_instructor.all()

        return self.request.user.course_list.all()

class CourseJoin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        course = Course.objects.get(pk=kwargs['pk'])
        exists = request.user.course_list.filter(pk=kwargs['pk']).exists()
        if exists:
            self.request.user.course_list.remove(course)
        else:
            self.request.user.course_list.add(course)

        return Response({
            "joined": not exists
        })

class VideoClassCreate(generics.CreateAPIView):
    serializer_class = VideoClassSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = Course.objects.get(pk=serializer.validated_data["course"].id)
        if course.instructor.id == self.request.user.id :
            serializer.save()