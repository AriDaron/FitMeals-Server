from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    payment_type = models.ForeignKey("PaymentType",on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    meals = models.ManyToManyField(
        "Meal", through="OrderMeal", related_name='orders')


    @property
    def total(self):
        """Calculate the order total

        Returns:
            float: The sum of the product prices on the order
        """
        return sum([m.price for m in self.meals.all()], 0)

    def __str__(self):
        is_open = 'Completed' if self.completed_on else 'Open'
        return f'{is_open} order for {self.customer.get_full_name()}'