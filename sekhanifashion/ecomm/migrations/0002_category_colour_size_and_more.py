# Generated by Django 4.1.4 on 2023-02-03 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecomm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('category_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='colour',
            fields=[
                ('colour_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('product_colour', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='size',
            fields=[
                ('size_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('product_size', models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')], max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='product_master',
            name='product_rating_avg',
            field=models.IntegerField(default=5),
        ),
        migrations.CreateModel(
            name='sub_category',
            fields=[
                ('sub_category_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sub_category_name', models.CharField(max_length=50, null=True)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.category')),
            ],
        ),
        migrations.CreateModel(
            name='rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_star', models.IntegerField(default=5)),
                ('feedback', models.TextField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.product_master')),
            ],
        ),
        migrations.CreateModel(
            name='product_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_price', models.IntegerField()),
                ('product_stock', models.IntegerField()),
                ('prod_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.category')),
                ('prod_colour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.colour')),
                ('prod_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.size')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.product_master')),
            ],
        ),
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.FloatField()),
                ('razorpay_order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razorpay_payment_status', models.CharField(blank=True, max_length=100, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.FloatField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.product_master')),
            ],
        ),
        migrations.CreateModel(
            name='customer_address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.BigIntegerField()),
                ('address_line_1', models.CharField(max_length=200)),
                ('address_line_2', models.CharField(max_length=200)),
                ('landmark', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=25)),
                ('district', models.CharField(max_length=20)),
                ('pin_code', models.IntegerField(max_length=6)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='cart_items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.product_master')),
            ],
        ),
    ]
