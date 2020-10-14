from django.contrib import admin
from .models import Currency, BusinessTransactionOrigin, BusinessTransaction, BusinessTransactionDetail

# Register your models here.

admin.site.register(Currency)
admin.site.register(BusinessTransactionOrigin)
admin.site.register(BusinessTransaction)
admin.site.register(BusinessTransactionDetail)
