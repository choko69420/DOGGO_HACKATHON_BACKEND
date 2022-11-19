from django.urls import path
from .views import ReportListCreate, UserCreate, UserLogin, UserLogout
urlpatterns = [
    path('/', ReportListCreate.as_view()),
    path('/register', UserCreate.as_view()),
    path('/login', UserLogin.as_view()),
    path('/logout', UserLogout.as_view())
]
