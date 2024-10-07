from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, RegexValidator
from furniture.models import Furniture
from .base_model import BaseModel

class Customer(BaseModel, AbstractUser):
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$', 
                message='Phone number must be in the format +999999999. Up to 15 digits allowed.'
            )
        ]
    )
    email = models.EmailField(max_length=225, blank=True, null=True)
    profile_pic = models.URLField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customer_user_set', 
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customer_user_permissions_set', 
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        db_table = 'customers'


class ShippingAddress(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.address_line1}, {self.city}, {self.state}'

    class Meta:
        verbose_name = 'Shipping Address'
        verbose_name_plural = 'Shipping Addresses'
        db_table = 'shipping_addresses'


class Cart(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Cart for {self.customer}'

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        db_table = 'carts'


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Cart Item for {self.cart} - {self.furniture}'

    def get_total_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        db_table = 'cart_items'


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('shipped', 'Shipped'), ('delivered', 'Delivered')])
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f'Order #{self.id} - {self.customer}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        db_table = 'orders'


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order Item for {self.order} - {self.furniture}'

    def get_total_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        db_table = 'order_items'


class Review(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5, message='Rating must be between 1 and 5')])
    comment = models.TextField()

    def __str__(self):
        return f'Review for {self.customer} - {self.furniture}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        db_table = 'reviews'
