from django.db import models

# Create your models here.

class AmazonProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    ratings = models.CharField(max_length=50, blank=True, null=True)
    stars = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'amazon_products'