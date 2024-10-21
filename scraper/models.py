from django.db import models

# Create your models here.


# Brand model to store Amazon brand details
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="The name of the Amazon brand")
    last_scraped = models.DateTimeField(null=True, blank=True, help_text="The last time products were scraped for this brand")
    scrape_frequency = models.IntegerField(default=6, help_text="Frequency of scraping in hours")


    def __str__(self):
        return self.name

# Product model to store Amazon product details
class Product(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the product")
    asin = models.CharField(max_length=10, unique=True, help_text="Amazon Standard Identification Number (ASIN)")
    sku = models.CharField(max_length=50, blank=True, null=True, help_text="Stock Keeping Unit (SKU)")
    image = models.URLField(max_length=500, help_text="URL of the product image")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products", help_text="Brand to which the product belongs")

    def __str__(self):
        return self.name