from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.exceptions import ValidationError
from drf_spectacular.utils import (
    extend_schema
)

from .serializers.user import (
    CustomTokenObtainPairSerializer,
    ValidatePasswordSerializer,
    ValidatePasswordResponseSerializer
)

# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# views.py
from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    UserAttributeSimilarityValidator,
)
class PasswordValidationView(APIView):

    serializer_class = ValidatePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]


    @extend_schema(
        methods = ['post'],
        summary = 'Comentarios de sustentación',
        description = 'Crea un comentario a una sustentación',
        tags = ['v1'],
        responses = {
            200: ValidatePasswordResponseSerializer
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)

        password = serializer.data['password']
        user = request.user

        common_validator = CommonPasswordValidator()
        similarity_validator = UserAttributeSimilarityValidator()

        response_data = {
            "common": True,
            "similarity": True,
        }

        try:
            common_validator.validate(password)
        except ValidationError as e:
            response_data["common"] = False

        try:
            similarity_validator.validate(password, user=user)
        except ValidationError as e:
            response_data["similarity"] = False

        return Response(response_data, status=status.HTTP_200_OK)
