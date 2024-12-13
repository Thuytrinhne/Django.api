# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

# API: Register# API: Register
class RegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Hash mật khẩu trước khi lưu
            from django.contrib.auth.hashers import make_password
            data = serializer.validated_data
            data['password'] = make_password(data['password'])
            
            user = User.objects.create(**data)
            return Response({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# API: Login
class LoginView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            print("Login attempt - Email:", email)
            print("Login attempt - Password:", password)
            try:
                user = User.objects.get(email=email)
                if user.verify_password(password):
                    user.last_login_at = now()
                    user.save()
                    return Response({'message': 'Login successful', 'user': UserSerializer(user).data})
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API: Get all users (admin only)
class AdminUserListView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
