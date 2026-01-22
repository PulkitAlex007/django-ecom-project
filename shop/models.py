from django.db import models
CATEGORY_CHOICES = (
    ('men', 'Men'),
    ('women', 'Women'),
    ('child', 'Child'),
    ('accessories', 'Accessories'),
)

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    short_description = models.CharField(max_length=300)
    long_description = models.TextField()
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to="products/")
    stock = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    listed_by=models.CharField(blank=True,default="")
    listed_date=models.DateField(blank=True,auto_now_add="",null=True)

    def __str__(self):
        return self.title
    
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    user_image = models.ImageField(upload_to='profile_images/', default='https://www.pngall.com/wp-content/uploads/5/Profile-Avatar-PNG-Picture.png', blank=True)

    address_line = models.CharField(max_length=255, blank=True, default="Not provided")
    pin_code = models.CharField(max_length=10, blank=True, default="000000")
    state = models.CharField(max_length=100, blank=True, default="Not provided")
    country = models.CharField(max_length=100, blank=True, default="Not provided")

    phone_number = models.CharField(max_length=15, blank=True, default="Not provided")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True,default="N/A")
    age = models.CharField(blank=True,default="Not provided")

    def __str__(self):
        return self.user.username


class Order(models.Model):

    # Dropdown for order status
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Placed", "Placed"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


# OrderItem Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"