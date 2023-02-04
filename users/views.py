from django.contrib.auth.models import User
from drf_util.decorators import serialize_decorator
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, EmailTokenObtainSerializer, UserNamesSerializer
# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView

class EmailTokenObtainPairView(GenericAPIView):
    serializer_class = EmailTokenObtainSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({"error": "User not found"}, status=404)
        if not user.check_password(password):
            return Response({"error": "Wrong password"}, status=400)
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            , status=status.HTTP_200_OK
        )

class UsersListView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        users = User.objects.all()
        serialized_users = UserNamesSerializer(users, many=True)
        return Response(serialized_users.data, status=status.HTTP_200_OK)

class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(UserSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data
        password = validated_data.pop("password")

        user = User.objects.create(
            **validated_data,
            username=validated_data["email"],
            is_superuser=True,
            is_staff=True,
        )

        user.set_password(password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=200,
        )