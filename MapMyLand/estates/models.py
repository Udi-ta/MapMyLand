from django.db import models

class Broker(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MicroMarket(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Property(models.Model):
    google_location = models.CharField(max_length=255)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    parcel_size_acres = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_acre = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    micro_market = models.ForeignKey(MicroMarket, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.google_location} - {self.city.name}"
