from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import CourseDestroy, CourseJoin, CourseRetrieve, CourseUpdate, CustomAuthToken, RegisterView, Home, Explore, CourseCreate, MyCourseList, UpdateUser, VideoClassCreate
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', CustomAuthToken.as_view()),
    path('user/update', UpdateUser.as_view()),
    path('', Home.as_view()),
    path('explore', Explore.as_view()),
    path('course/create', CourseCreate.as_view()),
    path('course/<int:pk>', CourseRetrieve.as_view()),
    path('course/<int:pk>/update', CourseUpdate.as_view()),
    path('course/<int:pk>/delete', CourseDestroy.as_view()),
    path("course/<int:pk>/join", CourseJoin.as_view()),
    path('my_courses', MyCourseList.as_view()),
    path('course/add_video', VideoClassCreate.as_view())
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)