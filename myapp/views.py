from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer
from rest_framework.decorators import api_view  
# , permission_classes
# from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer
# UserSerializer, 


class RegisterUserView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET', 'PUT'])
# @permission_classes([IsAuthenticated])
# def Edit_Profile(request):
#     user = request.user  # Get the currently logged-in user

#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_profile(request):
    try:
        user_profile = request.user.profile  # Assuming you have a related profile
        serializer = CustomUserSerializer(user_profile)
        return Response(serializer.data)
    except CustomUserSerializer.DoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_user_profile(request):
    try:
        user_profile = request.user.profile  # Assuming you have a related profile
        serializer = CustomUserSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except CustomUserSerializer.DoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
