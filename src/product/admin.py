from django.contrib import admin
from .models import (
    Variant,
    Product,
    ProductImage,
    ProductVariant,
    ProductVariantPrice,
)
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

# admin.site.register(Variant, Product, ProductImage, ProductVariant, ProductVariantPrice)

admin.site.register(Variant)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)