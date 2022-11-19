# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import Report, User
from .serializers import ReportSerializer, UserSerializer, LoginSerializer, LogoutSerializer
from rest_framework.response import Response


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
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, serializer, *args, **kwargs):
        # get the user password, username, and email
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
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
