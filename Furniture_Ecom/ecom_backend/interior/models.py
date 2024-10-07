from django.db import models
from customer.base_model import BaseModel
from django.core.validators import MinValueValidator , MaxValueValidator
from customer.models import Customer

class DesignCategory(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Design Category'
        verbose_name_plural = 'Design Categories'
        db_table = 'design_categories'


class InteriorDesignProject(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(DesignCategory, on_delete=models.SET_NULL, null=True, related_name='projects')
    budget = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.name} - {self.client_name}'

    class Meta:
        verbose_name = 'Interior Design Project'
        verbose_name_plural = 'Interior Design Projects'
        db_table = 'interior_design_projects'


class DesignImage(BaseModel):
    project = models.ForeignKey(InteriorDesignProject, on_delete=models.CASCADE, related_name='images')
    image = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Image for {self.project.name}'

    class Meta:
        verbose_name = 'Design Image'
        verbose_name_plural = 'Design Images'
        db_table = 'design_images'


class RoomType(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Room Type'
        verbose_name_plural = 'Room Types'
        db_table = 'room_types'


class InteriorRoom(BaseModel):
    project = models.ForeignKey(InteriorDesignProject, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, related_name='rooms')
    dimensions = models.CharField(max_length=100, blank=True, null=True)  # e.g., "10x12 ft"
    design_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.room_type.name} for {self.project.name}'

    class Meta:
        verbose_name = 'Interior Room'
        verbose_name_plural = 'Interior Rooms'
        db_table = 'interior_rooms'


class ServicePackage(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service Package'
        verbose_name_plural = 'Service Packages'
        db_table = 'service_packages'


class Booking(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    service_package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, related_name='bookings')
    project = models.OneToOneField(InteriorDesignProject, on_delete=models.SET_NULL, null=True, related_name='booking')
    booking_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed')])

    def __str__(self):
        return f'Booking for {self.customer.username} - {self.service_package.name}'

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        db_table = 'bookings'
