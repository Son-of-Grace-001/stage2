from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Organisation
from .serializers import UserSerializer, OrganisationSerializer

class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': serializer.data
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Registration unsuccessful',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': serializer.data
                }
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad request',
            'message': 'Authentication failed',
            'statusCode': 401
        }, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
            if user == request.user or request.user.organisations.filter(users__pk=id).exists():
                serializer = UserSerializer(user)
                return Response({
                    "status": "success",
                    "message": "User details retrieved successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "status": "Unauthorized",
                "message": "You do not have permission to view this user's details",
                "statusCode": 403
            }, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({
                "status": "Not found",
                "message": "User not found",
                "statusCode": 404
            }, status=status.HTTP_404_NOT_FOUND)

class UserOrganisationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        organisations = request.user.organisations.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response({
            'status': 'success',
            'message': 'Organisations retrieved successfully',
            'data': {'organisations': serializer.data}
        }, status=status.HTTP_200_OK)

class OrganisationDetailView(generics.RetrieveAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

class CreateOrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            organisation.users.add(request.user)
            return Response({
                'status': 'success',
                'message': 'Organisation created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad Request',
            'message': 'Client error',
            'statusCode': 400
        }, status=status.HTTP_400_BAD_REQUEST)

class AddUserToOrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, orgId, *args, **kwargs):
        organisation = Organisation.objects.filter(orgId=orgId).first()
        if not organisation:
            return Response({
                'status': 'Bad Request',
                'message': 'Organisation not found',
                'statusCode': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data.get('userId')
        user = User.objects.filter(userId=user_id).first()
        if not user:
            return Response({
                'status': 'Bad Request',
                'message': 'User not found',
                'statusCode': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        organisation.users.add(user)
        return Response({
            'status': 'success',
            'message': 'User added to organisation successfully',
        }, status=status.HTTP_200_OK)
