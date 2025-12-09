from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User

class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        user = User.objects.create(
            full_name=data["full_name"],
            email=data["email"],
            password=data["password"],  # Hash later
            role=data["role"]
        )
        return Response({"message": "User created", "id": user.id})
