from django.urls import path
from .views import ReportListCreate, UserCreate, UserLogin, UserLogout, ListCreateFriendRequests, ConfirmFriendRequest, ListFriends
urlpatterns = [
    path('/', ReportListCreate.as_view()),
    path('/register', UserCreate.as_view()),
    path('/login', UserLogin.as_view()),
    path('/logout', UserLogout.as_view()),
    path('/confirmFriendRequest', ConfirmFriendRequest.as_view()),
    path('/addFriend', ListCreateFriendRequests.as_view()),
    path('/friends', ListFriends.as_view()),
]
