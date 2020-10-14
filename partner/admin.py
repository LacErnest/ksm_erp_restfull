from django.contrib import admin
from .models import PartnerType, TypeAdresse, PartnerAdresse, Partner, Contact, Price, EligiblePrice, ExemptTaxe, PartnerTax, PaymentMethod, PartnerPaymentMethod

# Register your models here.

admin.site.register(PartnerType)
admin.site.register(TypeAdresse)
admin.site.register(PartnerAdresse)
admin.site.register(Partner)
admin.site.register(Contact)
admin.site.register(Price)
admin.site.register(EligiblePrice)
admin.site.register(ExemptTaxe)
admin.site.register(PartnerTax)
admin.site.register(PaymentMethod)
admin.site.register(PartnerPaymentMethod)