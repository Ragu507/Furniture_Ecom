from django.db import models
from customer.base_model import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now 

class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'furniture_categories'

class Furniture(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='furniture')
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    sku = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
    image = models.URLField(blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def get_effective_price(self):
        current_time = now()  
        discount = self.discounts.filter(start_date__lte=current_time, end_date__gte=current_time).first()

        if discount:
            discounted_price = self.price - (self.price * (discount.discount_percentage / 100))
            return round(discounted_price, 2) 
        return self.price

    class Meta:
        verbose_name = 'Furniture'
        verbose_name_plural = 'Furniture'
        db_table = 'furniture_items'

class FurnitureAttribute(BaseModel):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name='attributes')
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.attribute_name}: {self.attribute_value}'

    class Meta:
        verbose_name = 'Furniture Attribute'
        verbose_name_plural = 'Furniture Attributes'
        db_table = 'furniture_attributes'

class Discount(BaseModel):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name='discounts')
    discount_percentage = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.discount_percentage}% on {self.furniture}'

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'
        db_table = 'furniture_discounts'

class FurnitureVariant(BaseModel):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name='variants')
    variant_name = models.CharField(max_length=100)
    variant_value = models.CharField(max_length=100) 

    def __str__(self):
        return f'{self.variant_name}: {self.variant_value}'

    class Meta:
        verbose_name = 'Furniture Variant'
        verbose_name_plural = 'Furniture Variants'
        db_table = 'furniture_variants'
