from django.core.management.base import BaseCommand
from scraper.models import Brand, Product
from scraper.scraping_logic import scrape_amazon  # Import your scraping function

class Command(BaseCommand):
    help = "Scrape Amazon products for all brands in the database"

    def handle(self, *args, **kwargs):
        brands = Brand.objects.all()
        for brand in brands:
            self.stdout.write(f"Scraping products for brand: {brand.name}")
            products_data = scrape_amazon(brand.name)  # Use the scraper function from your scraper code
            
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
                    self.stdout.write(f"Created new product: {product.name}")
                else:
                    self.stdout.write(f"Updated product: {product.name}")
