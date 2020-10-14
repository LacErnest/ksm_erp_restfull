from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(InventoryMotif)
admin.site.register(InventoryType)
admin.site.register(SourceMovement)
admin.site.register(ArticleStore)
admin.site.register(StockMovement)
admin.site.register(MovementDetail)
admin.site.register(Inventory)
admin.site.register(InventoryDetail)