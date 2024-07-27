from django.contrib import admin
from django.utils.html import format_html

from . models import *

# Register your models here.
class productMasteradmin(admin.ModelAdmin):
    list_display=('product_id' , 'product_name', 'product_price')

class productDetailadmin(admin.ModelAdmin):

    def myphoto(self, object):
        return format_html('<img src="{}" width="40" />'.format(object.product_image_1.url ))

    list_display=('product', 'myphoto' , 'prod_category', 'prod_size', 'prod_colour', 'product_stock')

class customerAddressadmin(admin.ModelAdmin):
    list_display=('id','first_name' , 'last_name', 'mobile_number', 'address_line_1', 'address_line_2', 'landmark', 'city', 'state', 'pin_code')

class subOrderadmin(admin.ModelAdmin):
    list_display=('sub_order_id' , 'order', 'product', 'quantity', 'sub_total')

class orderAdmin(admin.ModelAdmin):
    list_display=('order_id' , 'customer' ,'quantity', 'total_amount', 'shipping_address', 'order_date')    

class sizeAdmin(admin.ModelAdmin):
    list_display=('size_id','product_size')

class SubCategoryadmin(admin.ModelAdmin):
    list_display=('sub_category_id','category_name','sub_category_name')

admin.site.register(Product_master,productMasteradmin)
admin.site.register(product_detail,productDetailadmin)
admin.site.register(size,sizeAdmin)
admin.site.register(colour)
admin.site.register(payment)
admin.site.register(category)
admin.site.register(sub_category,SubCategoryadmin)
admin.site.register(customer_address,customerAddressadmin)
admin.site.register(rating)
admin.site.register(cart_items)
admin.site.register(Orders,orderAdmin)
admin.site.register(sub_order,subOrderadmin)
admin.site.register(slider)


