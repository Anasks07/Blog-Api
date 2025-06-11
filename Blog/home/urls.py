from django.urls import path
from .views import RegisterView,DisplayUser,CreateBlogView,UserloginView,ListBlogView,DeleteBlogView,DeleteUserView
urlpatterns = [
    path("api/register/",RegisterView.as_view(),name="Register"),
    path("api/getuser/",DisplayUser.as_view()),
    path("api/createblog/",CreateBlogView.as_view()),
    path("api/login/",UserloginView.as_view()),
    path("api/listblog/",ListBlogView.as_view()),
    path("api/listblog/<int:id>/",ListBlogView.as_view()),
    path("api/deleteblog/<int:id>/",DeleteBlogView.as_view()),
    path("api/deleteuser/<int:id>/",DeleteUserView.as_view()),

]
