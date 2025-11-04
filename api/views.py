from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer

from rest_framework import viewsets, permissions
from .models import Activity
from .serializers import ActivitySerializer

# Registration view
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)


# Logout view
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Client must send refresh token in the body
            refresh_token = request.data.get("refresh")
            if refresh_token is None:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"detail": "User logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user).order_by('-date', '-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {"detail": "Activity updated successfully."}
        return response

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        #deletion message
        return Response({"detail": "Activity deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
