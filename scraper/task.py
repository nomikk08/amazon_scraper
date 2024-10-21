# scraper/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Brand, Product
from .scraping_logic import scrape_amazon  # The scraping logic you already created

@shared_task
def scrape_all_brands():
    """
    Celery task that scrapes products for all brands in the database.
    Runs every 6 hours and updates the database with the latest product information.
    """
    brands = Brand.objects.all()
    for brand in brands:
        try:
            products_data = scrape_amazon(brand.name)  # Scrape products for the brand
            
            # Add or update products in the database
            for product_data in products_data:
                product, created = Product.objects.update_or_create(
                    asin=product_data['ASIN'],  # Unique identifier
                    defaults={
                        'name': product_data['name'],
                        'sku': product_data['SKU'],
                        'image': product_data['image_url'],
                        'brand': brand
                    }
                )
                if created:
                    print(f"Created new product: {product.name}")
                else:
                    print(f"Updated product: {product.name}")
            
            # Update the last_scraped field
            brand.last_scraped = timezone.now()
            brand.save()
            
        except Exception as e:
            # Handle scraping errors (e.g., log the exception)
            print(f"Failed to scrape products for brand {brand.name}: {str(e)}")

    return f"Scraped products for {brands.count()} brands."
