from django.db import models
from django.contrib.auth.models import User

class PaymentType(models.Model):
    card_type = models.CharField(max_length=25)
    card_number = models.CharField(max_length=16)
    customer =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_types')


    @property
    def obscured_num(self):
        """Obscure the card number

        Returns:
            string: ex. **********1234
        """
        return '*'*(len(self.card_number) - 4)+self.card_number[-4:]
