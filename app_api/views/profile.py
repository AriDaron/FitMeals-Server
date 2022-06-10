from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .meal import MealSerializer


class ProfileView(ViewSet):
    @action(methods=['GET'], detail=False, url_path="myprofile")
    def my_profile(self, request):
        """Get the current user's profile"""
        try:
            serializer = UserSerializer(request.auth.user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['PUT'], detail=False)
    def edit(self, request):
        """Edit the current user's profile"""
        user = request.auth.user
        user.username = request.data['username']
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        if request.data.get('password', None):
            user.set_password(request.data['password'])
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'orders'
                  )
        depth = 2


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()