from django.contrib.auth.models import Group
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from django.contrib.auth.password_validation import validate_password
from django.db.transaction import atomic

from .serializers.user import (
    CustomTokenObtainPairSerializer,
    ValidatePasswordSerializer,
    ValidatePasswordResponseSerializer,
    RegisterSerializer,
    ValidateDocumentNumberSerializer
)
from .utils.user import (
    find_user_info_by_document
)
from .validators.user import (
    UniqueUserWithDocumentNumberValidator
)
from .models import (
    CustomUser
)
from core.validators.validator import ValidatorRules

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

    @extend_schema(
        methods=['post'],
        summary='Validar contraseña',
        description='Valida que la contraseña no sea común o sea similar a atributos del usuario',
        tags=['v1'],
        responses={200: ValidatePasswordResponseSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.data['password']
        user = request.user

        common_validator = CommonPasswordValidator()
        similarity_validator = UserAttributeSimilarityValidator()

        response_data = {
            'common': True,
            'similarity': True,
        }

        try:
            common_validator.validate(password)
        except ValidationError as e:
            response_data['common'] = False

        try:
            similarity_validator.validate(password, user=user)
        except ValidationError as e:
            response_data['similarity'] = False

        return Response(response_data, status=status.HTTP_200_OK)


class ValidateInfoUserView(APIView):

    serializer_class = ValidateDocumentNumberSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        methods=['post'],
        summary='Validar usuario en sistema',
        description='Verifica si el número de documento proporcionado se encuentra en el sistema para poder crear un usuario.',
        tags=['v1'],
    )
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)

        validator = ValidatorRules()
        validator.add_rules(rules = [UniqueUserWithDocumentNumberValidator])
        try:
            validator.validate(data = serializer.data)
        except ValidationError as e:
            return Response({'detail': e.message,}, status = status.HTTP_400_BAD_REQUEST)
        
        valid = find_user_info_by_document(
            document_number = serializer.data['document_number']
        )

        status_response = status.HTTP_200_OK if valid['valid'] else status.HTTP_404_NOT_FOUND
        return Response(data = valid, status = status_response)

class RegisterView(APIView):

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        methods=['post'],
        summary='Registrarse',
        description='Registrar usuario',
        tags=['v1'],
    )
    @atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data
        validator = ValidatorRules()
        validator.add_rules(rules = [UniqueUserWithDocumentNumberValidator])
        try:
            validator.validate(data = data)
            validate_password(data['password'])
        except ValidationError as e:
            return Response({'detail': ' '.join(e.messages)})
        
        response = find_user_info_by_document(
            document_number = data['document_number'],
            full_info = True
        )

        if not response['valid']:
            return Response(response, status = status.HTTP_404_NOT_FOUND)

        role, _= Group.objects.get_or_create(name = response['role'])
        
        user = CustomUser.objects.create(
            first_name = response['data']['first_name'],
            last_name = response['data']['last_name'],
            role = role,
            email = response['instance'].email
        )

        user.groups.add(role)
        user.set_password(data['password'])
        user.save()

        instance = response['instance']
        instance.user = user
        instance.save()
        
        return Response(status = status.HTTP_201_CREATED)