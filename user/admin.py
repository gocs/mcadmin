from django.contrib import admin
from .models import Player, AbstractPayment, Payment

# show hidden timestamps as readonly fields
class UserPlayerAdmin(admin.ModelAdmin):
    readonly_fields = ('joined',)
class UserPaymentAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)


admin.site.register(Player, UserPlayerAdmin)
admin.site.register(Payment, UserPaymentAdmin)
