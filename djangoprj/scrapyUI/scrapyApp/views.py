from django.shortcuts import render
from .models import AmazonProduct
from django.db.models import Max, Min, Avg, FloatField
from django.db.models.functions import Cast

def scrapydata(request):
   

    prices = []
    products = AmazonProduct.objects.all()

    for product in products:

        if product.price:
            try:
                cleaned_price = product.price.replace('$', '').replace(',', '').strip()
                price = float(cleaned_price)
                prices.append(price)
            except (ValueError, TypeError):
                continue  # Skip invalid entries

    if prices:
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)
        avg_price = round(avg_price, 2)
    else:
        min_price = max_price = avg_price = 0.00

    summary = {
        'min_price': min_price,
        'max_price': max_price,
        'avg_price': avg_price,
    }



    products = AmazonProduct.objects.all()

    context = {
        'summary' : summary,
        'products' : products
    }

    return render(request, 'tabledemo.html', context)
