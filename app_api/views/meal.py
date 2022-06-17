"""View module for handling requests about meals"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from app_api.models import Meal, Order
from app_api.models.order_meal import OrderMeal


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
 
    @action(methods=['post'], detail=True)
    def add_to_order(self, request, pk):
        """Add a meal to the current users open order"""
        try:
            meal = Meal.objects.get(pk=pk)
            order, _ = Order.objects.get_or_create(
                customer=request.auth.user, completed_on=None, payment_type=None)
            OrderMeal.objects.create(meal=meal, order=order)
            return Response({'message': 'meal added'}, status=status.HTTP_201_CREATED)
        except Meal.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    @action(methods=['delete'], detail=True)
    def remove_from_order(self, request, pk):
        """Remove a meal from the customers open order"""
        try:
            meal = Meal.objects.get(pk=pk)
            order = Order.objects.get(
                customer=request.auth.user, completed_on=None)
            order.meals.remove(meal)
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except (Meal.DoesNotExist, Order.DoesNotExist) as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class MealSerializer(serializers.ModelSerializer):
    """JSON serializer for meals  """
    class Meta:
        model = Meal
        fields = ('id', 'name', 'price', 'nutrition',
                  'quantity', 'category', 'imageURL')
        depth = 1


class CreateMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'name', 'price', 'nutrition', 'category', 'imageURL']
