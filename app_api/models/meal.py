from django.db import models


class Meal(models.Model):
    name= models.CharField(max_length=55)
    price= models.DecimalField(max_digits=7, decimal_places=2)
    nutrition= models.TextField()
    quantity= models.IntegerField()
    category= models.ForeignKey("Category",on_delete=models.CASCADE)
    imageURL= models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    
    def __str__(self):
        return self.name

    @property
    def fav(self):
        return self.__fav

    @fav.setter
    def fav(self, value):
        self.__fav = value