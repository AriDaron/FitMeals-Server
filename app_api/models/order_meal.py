from django.db import models

class OrderMeal(models.Model):
    order = models.ForeignKey("Order",on_delete=models.CASCADE)
    meal = models.ForeignKey("Meal",on_delete=models.CASCADE)