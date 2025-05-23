from django.db import models

class Car(models.Model):
    car = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='car_images/', null=True, blank=True)
    is_reserved = models.BooleanField(default=False)  # <-- dodane pole

    def __str__(self):
        return self.car



