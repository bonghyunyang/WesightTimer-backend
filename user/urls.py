from django.urls import path

from .views     import(
    SignInView,
    SignUpView,
    TeacherView
)

urlpatterns =[
    path('/signin', SignInView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/teacher', TeacherView.as_view())
]
