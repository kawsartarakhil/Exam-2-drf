from django.shortcuts import render
from .serializers import RegisterSerailizer,UserSerailizer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import CustomUser
from library.models import Institution
from library.models import Region


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    serailizer = RegisterSerailizer(data=request.data)

    if serailizer.is_valid(raise_exception=True):
        serailizer.save()
        return Response({"message":"Registration successfull","user":serailizer.data},status=status.HTTP_201_CREATED)

    return Response(serailizer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error":"All fields are required"})

    user = authenticate(request,username=username,password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh":str(refresh),
            "access":str(refresh.access_token),
            "user":{"id":user.id,"username":user.username}
        })

    return Response({"error":"Incorrect crediantiols"},status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token_view(request):
    serailizer = TokenRefreshSerializer(data=request.data)
    try:
        serailizer.is_valid(raise_exception=True)
    except Exception as err:
        return Response({"error":str(err)},status=status.HTTP_400_BAD_REQUEST)
    return Response(serailizer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    token = request.data.get("refresh")
    if not token:
        return Response({"error": "Refresh token required"}, status=400)
    try:
        refresh = RefreshToken(token)
        refresh.blacklist()
    except Exception:
        return Response({"error": "Invalid refresh token"}, status=400)
    return Response({"message": "Logout successful"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    serailizer = UserSerailizer(user)
    return Response(serailizer.data,status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def assign_role_view(request, pk):
    if request.user.role != "super_admin" or not request.user.is_superuser:
        return Response({"error": "Only super admins can assign roles"},status=status.HTTP_403_FORBIDDEN)

    user = CustomUser.objects.filter(id=pk).first()
    if user is None:
        return Response({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)

    if user.id == request.user.id:
        return Response({"error": "You cannot change your own role"},status=status.HTTP_403_FORBIDDEN)

    role = request.data.get("role")
    if role not in ["school_admin", "regional_admin", "super_admin"]:
        return Response({"error": "Invalid role"},status=status.HTTP_400_BAD_REQUEST)

    if user.is_superuser and user.id != request.user.id:
        return Response({"error": "Cannot change another Django superuser"},status=status.HTTP_403_FORBIDDEN)

    if role == "super_admin" and user.id != request.user.id:
        return Response({"error": "Cannot assign super admin through this endpoint"},status=status.HTTP_403_FORBIDDEN)

    if role == "school_admin":
        institution_id = request.data.get("institution")
        if not institution_id:
            return Response({"error": "Institution required"}, status=400)

        institution = Institution.objects.filter(id=institution_id).first()
        if institution is None:
            return Response({"error": "Institution not found"}, status=404)

        user.institution = institution
        user.region = None

    elif role == "regional_admin":
        region_id = request.data.get("region")
        if not region_id:
            return Response({"error": "Region required"}, status=400)

        region = Region.objects.filter(id=region_id).first()
        if region is None:
            return Response({"error": "Region not found"}, status=404)
        user.region = region
        user.institution = None
    else:
        user.region = None
        user.institution = None
    user.role = role
    user.is_active = True
    user.save()

    return Response({"message": "Role assigned successfully"})