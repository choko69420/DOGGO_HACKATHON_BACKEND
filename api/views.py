# Create your views here.
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .models import Report, User
from .serializers import ReportSerializer, UserSerializer, LoginSerializer, LogoutSerializer, AddFriendSerializer, UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import serializers


class ConfirmFriendRequest(APIView):
    def patch(self, request):
        token = request.headers['Authorization'].split(' ')[1]
        user = Token.objects.get(key=token).user
        # get who the user wants to add with username
        target = User.objects.filter(
            username=self.request.data['username']).first()
        # check if user is already friends
        if target in user.friends.all():
            raise serializers.ValidationError("Already friends")
        # check if there is a pending request
        if not target in user.friend_requests.all():
            raise serializers.ValidationError(
                "The user has not sent a friend request")

        # add friend
        user.friends.add(target)
        # remove friend request
        user.friend_requests.remove(target)
        user.save()
        return Response({'message': 'Friend request confirmed'})


class ListCreateFriendRequests(APIView):
    def get(self, request):
        token = request.headers['Authorization'].split(' ')[1]
        user = Token.objects.get(key=token).user

        serializer = AddFriendSerializer(user.friend_requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        token = request.headers['Authorization'].split(' ')[1]
        user = Token.objects.get(key=token).user

        target = User.objects.filter(
            username=self.request.data['username']).first()
        # check if user is already friends
        if target in user.friends.all():
            raise serializers.ValidationError("Already friends")
        # check if there is a pending request
        if target in user.friend_requests.all():
            raise serializers.ValidationError("Already requested")
        # add friend request
        user.friend_requests.add(target)
        user.save()
        return Response("Friend request sent")


class ListFriends(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        token = self.request.headers['Authorization'].split(' ')[1]
        user = Token.objects.get(key=token).user
        return user.friends.all()


class ReportListCreate(ListCreateAPIView):
    """
    List all reports, or create a new report.
    Args:
        ListCreateAPIView (): Lists reports if get request, creates report if post request
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        token = self.request.headers['Authorization'].split(' ')[1]
        user = Token.objects.get(key=token).user
        serializer.save(**self.request.data, author=user)


class UserCreate(CreateAPIView):
    """
    Create a new user in the system.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, serializer, *args, **kwargs):
        # get the user password, username, and email
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            # create the user
            user = User.objects.create_user(**serializer.validated_data)
            token = Token.objects.create(user=user)
            json = serializer.validated_data
            json['token'] = token.key
            if user:
                return Response(json, status=201)
        return Response(serializer.errors, status=400)


class UserLogin(APIView):
    """
    Login a user in the system and return a token.
    """
    authentication_classes = []
    permission_classes = []

    # login a user
    def post(self, request):
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # we take the 0th index because it returns a tuple (tokenkey, someboolean) idk why
            token = Token.objects.get_or_create(user=user)[0]
            json = UserSerializer(user).data
            json['token'] = token.key
            return Response(json, status=200)
        return Response(serializer.errors, status=400)


class UserLogout(APIView):
    """
    Logs a user out of the system.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # get the token from the request
        serializer = LogoutSerializer(data=request.data)
        # delete the token
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            Token.objects.get(key=serializer.validated_data).delete()
            return Response(status=204)
        return Response(serializer.errors, status=400)
