from django.core.validators import RegexValidator
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f'{self.name}: {self.phone_number}, {self.email}'


class Order(models.Model):
    _STATUS = (('Created', 'Created'),
               ('Assembling', 'Assembling'),
               ('Delivering', 'Delivering'),
               ('Delivered', 'Delivered'),
               ('Issued', 'Issued'),
               ('Canceled', 'Canceled'))
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.TextField()
    status = models.CharField(max_length=100, choices=_STATUS, default="Created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer_id.name} {self.address}: {self.status}'


class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}: {self.description}'


class OrderItem(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.ForeignKey(
        to=Order,
        related_name="item_prices",
        null=True,
        on_delete=models.SET_NULL,
    )
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f' {str(self.quantity)} {self.product_id.title}: {str(self.price)}rub'
