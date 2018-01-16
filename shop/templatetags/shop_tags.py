from django import template

register = template.Library()

from ..models import Product

@register.simple_tag
def total_posts():
 return Product.objects.all().count()

@register.inclusion_tag('shop/products/latest_product.html')
def latest_product(count=5):
    latest_product = Product.objects.filter(available=True).order_by('-created')[:count]
    return {'latest_product':latest_product}