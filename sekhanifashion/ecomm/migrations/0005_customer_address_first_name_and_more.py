# Generated by Django 4.1.4 on 2023-02-04 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0004_remove_order_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_address',
            name='first_name',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customer_address',
            name='last_name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecomm.customer_address'),
        ),
        migrations.CreateModel(
            name='sub_order',
            fields=[
                ('sub_order_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('sub_total', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.product_master')),
            ],
        ),
    ]
