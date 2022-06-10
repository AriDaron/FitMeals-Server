"""View module for handling requests about meals"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from app_api.models import Meal


class MealView(ViewSet):
    """FitMeals view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single meal 

        Returns:
            Response -- JSON serialized meal 
        """
        try:
            meal = Meal.objects.get(pk=pk)
            serializer = MealSerializer(meal)
            return Response(serializer.data)
        except Meal.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all meals

        Returns:
            Response -- JSON serialized list of meals
        """
        meals = Meal.objects.all()
        category = request.query_params.get('category', None)
        if category is not None:
            meals = meals.filter(category_id=category)
        serializer = MealSerializer(meals,many=True)
        return Response(serializer.data)
    
    # @action(methods=['post'], detail=True)
    # def favorite(self, request, pk):
    #     """Add stores to favorites list """
    #     meal= Meal.objects.get(pk=pk)
    #     user = request.auth.user
    #     meal.__fav= True 
    #     meal.favorites.add(user)
    #     return Response ({'message':'Favorite added'},status=status.HTTP_201_CREATED)


class MealSerializer(serializers.ModelSerializer):
    """JSON serializer for meals 
    """
    class Meta:
        model = Meal
        fields = ('id', 'name', 'price', 'nutrition',
                  'quantity', 'category', 'imageURL')
        depth = 1


class CreateMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'name', 'price', 'nutrition', 'category', 'imageURL']
