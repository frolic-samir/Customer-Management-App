from django.contrib import admin
from .models import Customer,Product,Tag, Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
  list_display =['customer','status']

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order,OrderAdmin)