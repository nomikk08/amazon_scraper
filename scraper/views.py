from django.shortcuts import render
from .models import Product
from django.db.models import Q

def home(request):
    """
    View for the homepage, where users can search and filter products.
    Supports search by product name, ASIN, SKU, and brand name.
    """
    query = request.GET.get('q')  # Get the search query from the URL
    products = Product.objects.all()  # Get all products initially
    
    # If there's a search query, filter the products by name, ASIN, SKU, or brand name
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(asin__icontains=query) |
            Q(sku__icontains=query) |
            Q(brand__name__icontains=query)
        )
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'scraper/home.html', context)
