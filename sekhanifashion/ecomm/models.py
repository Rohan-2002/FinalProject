from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class slider(models.Model):
    slider_image_1 = models.ImageField(upload_to='media/slider')
    slider_image_2 = models.ImageField(upload_to='media/slider')




class Product_master(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=30)
    product_description = models.TextField()
    product_price = models.IntegerField(null=True)
    product_rating_avg = models.IntegerField(default=5)

    def __str__(self):
        return self.product_name

class size(models.Model):
    
    size_id = models.BigAutoField(primary_key=True,null=False,blank=True)
    product_size = models.CharField(max_length=10)

    def __str__(self):
        return self.product_size

class colour(models.Model):
    colour_id = models.BigAutoField(primary_key=True)
    product_colour = models.CharField(max_length=20)
    colour_image = models.ImageField(upload_to='media/colour_image',null=True)

    
    def __str__(self):
        return self.product_colour

class category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    
    def __str__(self):
        return self.category_name

class sub_category(models.Model):
    sub_category_id = models.BigAutoField(primary_key=True)
    category_name = models.ForeignKey(category, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=50, null=True)


class product_detail(models.Model):
    product = models.ForeignKey(Product_master, on_delete=models.CASCADE)
    prod_category = models.ForeignKey(category, on_delete=models.CASCADE)
    prod_size = models.ForeignKey(size, on_delete=models.CASCADE)
    prod_colour = models.ForeignKey(colour, on_delete=models.CASCADE)
    product_stock = models.IntegerField()
    product_image_1 = models.ImageField(upload_to='media/products',null=True)
    product_image_2 = models.ImageField(upload_to='media/products',null=True)
    product_image_3 = models.ImageField(upload_to='media/products',null=True)

     

class customer_address(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15, null=True)
    last_name = models.CharField(max_length=20,  null=True)
    mobile_number = models.BigIntegerField()
    address_line_1 = models.CharField(max_length=200,blank=True)
    address_line_2 = models.CharField(max_length=200,blank=True)
    landmark = models.CharField(max_length=150,blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=25)
    pin_code = models.IntegerField()


class payment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

class Orders(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product_master, on_delete=models.CASCADE,null=True,blank=True)
    total_amount = models.FloatField()
    quantity = models.IntegerField()
    shipping_address = models.ForeignKey(customer_address, on_delete=models.CASCADE, null=True)
    order_date = models.DateTimeField(auto_now_add=True)

class sub_order(models.Model):
    sub_order_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_master, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sub_total = models.IntegerField()
    payment_detail = models.ForeignKey(payment, on_delete=models.CASCADE,null=True)


class cart_items(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_master, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.product_price

class rating(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_master, on_delete=models.CASCADE)
    rating_star = models.IntegerField(default=5)
    feedback = models.TextField()






