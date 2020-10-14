from django.contrib import admin
from .models import Language, Category, CategoryDescription, Conditioning, ProductDescription, Product, Tax, ProductTaxation, Pricing, ProductDetail, ProductIllustration

# Register your models here.

admin.site.register(Language)
admin.site.register(Category)
admin.site.register(CategoryDescription)
admin.site.register(Conditioning)
admin.site.register(ProductDescription)
admin.site.register(Product)
admin.site.register(Tax)
admin.site.register(ProductTaxation)
admin.site.register(Pricing)
admin.site.register(ProductDetail)
admin.site.register(ProductIllustration)
